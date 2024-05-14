# easy-gpt4o

Easy-GPT4O opensource version: use OpenAI older API implements GPT-4o in less than 200 lines of code.

This is a Python script that extracts audio from a video file, transcribes the audio using OpenAI Whisper API, generates image descriptions for key frames in the video using OpenAI GPT-4 Turbo API, and combines the results into a comprehensive response. The script also provides an option to convert the response to speech using the OpenAI TTS API.

## Features

- Extracts audio from a video file
- Transcribes the audio using OpenAI Whisper API
- Generates image descriptions for key frames in the video using OpenAI GPT-4 Turbo API
- Combines the audio transcription and image descriptions into a comprehensive response
- Converts the response to speech using OpenAI TTS API

## Prerequisites

- Python 3.6 or higher
- OpenAI Python package (`openai`)
- FFmpeg (for audio extraction)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/video-to-audio-transcription.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Download and install FFmpeg from the official website: https://ffmpeg.org/

## Usage

```bash
python script.py input_video.mp4 output_audio.mp3
```

Replace `input_video.mp4` with the path to your input video file, and `output_audio.mp3` with the desired path to save the output audio file.

## Demo

![demo_video](./demo/b.mp4)

![demo_audio](./demo/b.mp3)
