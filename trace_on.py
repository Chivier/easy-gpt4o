import cv2
import os
import uuid
import json
import base64
from mimetypes import guess_type
from pathlib import Path
from openai import OpenAI
import subprocess
import argparse


# Global OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_video_thumbnails(video_path):
    # Create a directory to store the thumbnails
    thumbnails_dir = "thumbnails"
    os.makedirs(thumbnails_dir, exist_ok=True)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the frame interval for generating thumbnails (1 second)
    frame_interval = int(fps)

    # Generate thumbnails
    thumbnails = []
    for frame_index in range(0, total_frames, frame_interval):
        # Set the frame index
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        # Read the frame
        ret, frame = video.read()

        if ret:
            # Generate a unique filename for the thumbnail
            thumbnail_filename = f"{uuid.uuid4()}.jpg"
            thumbnail_path = os.path.join(thumbnails_dir, thumbnail_filename)

            # Resize the image if necessary
            width, height = frame.shape[1], frame.shape[0]
            if width > 1024 or height > 1024:
                scale = min(1024 / width, 1024 / height)
                new_width, new_height = int(width * scale), int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height))

            # Save the thumbnail image
            cv2.imwrite(thumbnail_path, frame)

            # Create a dictionary entry for the thumbnail
            thumbnail = {"index": frame_index, "image_path": thumbnail_path}
            thumbnails.append(thumbnail)

    # Release the video object
    video.release()

    return thumbnails


def generate_image_description(image_path):
    # Read the image and convert it to a data URL
    image_data_url = local_image_to_data_url(image_path)

    # Generate description using the GPT-4 Vision Preview API
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What do you think is happening in this image?"},
                    {"type": "image_url", "image_url": {"url": local_image_to_data_url(image_path)}},
                ],
            }
        ],
        max_tokens=150,
    )

    # Extract the generated description from the response
    description = response.choices[0].message.content
    return description


# Function to encode a local image into a data URL
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"


def extract_audio_transcription(video_path):
    # Extract audio from the video using FFmpeg
    audio_path = "temp_audio.wav"
    subprocess.run(["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Read the audio file
    with open(audio_path, "rb") as audio_file:
        # Transcribe the audio using the OpenAI Whisper API
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    # Get the transcription text from the response
    text = transcription.text

    # Delete the temporary audio file
    os.remove(audio_path)

    return text


def generate_response(video_path):
    # Extract audio transcription
    audio_transcription = extract_audio_transcription(video_path)

    video_name = video_path.split(".")[0]

    # Generate image description
    # if thumbnails.json exists, load it
    if os.path.exists(f"{video_name}_thumbnails.json"):
        with open(f"{video_name}_thumbnails.json", "r") as f:
            thumbnails = json.load(f)
    else:
        thumbnails = generate_video_thumbnails(video_path)
        # store thumbnails to "video_name_thumbnails.json"
        with open(f"{video_name}_thumbnails.json", "w") as f:
            json.dump(thumbnails, f)

    video_description = ""
    for thumbnail in thumbnails:
        frame_index, image_path = thumbnail["index"], thumbnail["image_path"]
        image_description = generate_image_description(image_path)
        video_description += (
            f"On second {frame_index}: {image_description}\n\n"
        )

    video_description += f"My question is: {audio_transcription}"
    # Generate response with GPT-4-Turbo
    # Question: f"{video content} my question is: {audio_transcription}"
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{video_description} my question is: From the video, {audio_transcription}",
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content


def convert_text_to_speech(sentence, output_path):
    # Convert text to speech using the OpenAI TTS API
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=sentence
    )

    # Save the speech as an audio file
    speech_file_path = Path(output_path)
    response.stream_to_file(speech_file_path)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Video to Audio Transcription")
    parser.add_argument("video_path", type=str, help="Path to the input video file")
    parser.add_argument("audio_path", type=str, help="Path to save the output audio file")
    args = parser.parse_args()

    # Generate response
    response = generate_response(args.video_path)
    print(response)

    # Convert response to speech
    convert_text_to_speech(response, args.audio_path)
    print(f"Audio saved to: {args.audio_path}")
