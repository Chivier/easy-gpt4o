# easy-gpt4o

Blog Link: [Easy-GPT4o - reproduce GPT-4o in less than 200 lines](https://blog.chivier.site/2024-05-14/2024/Easy-GPT4o---reproduce-GPT-4o-in-less-than-200-lines-of-code/)

Easy-GPT4O opensource version: use OpenAI older API implements GPT-4o in less than 200 lines of code.

## Motivation

Why I start this project? This is just a toy project and a simple demo. I want to prove some ideas in this project:

- Developers can build their own GPT-4o using existing APIs. By leveraging available tools, developers can easily access the capabilities of advanced models.
- End-to-end models provide low latency but limited customization. This project explores the trade-off between latency and customization, highlighting the benefits and limitations of each approach.
- The combined power of multiple models can outperform a single multimodal model. This project demonstrates the effectiveness of a collaborative approach, leveraging the collective intelligence of various models to achieve superior results.

## Prerequisites

- Python 3.6 or higher
- OpenAI Python package (`openai`)
- FFmpeg (for audio extraction)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Chivier/easy-gpt4o
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Download and install FFmpeg from the official website: https://ffmpeg.org/

## Usage

```bash

# Set your own openai api
export OPENAI_API_KEY=xxxxxxx
python main.py input_video.mp4 output_audio.mp3
```

Replace `input_video.mp4` with the path to your input video file, and `output_audio.mp3` with the desired path to save the output audio file.

## How to make it happen

<img width="1048" alt="image" src="https://github.com/Chivier/easy-gpt4o/assets/41494877/06fa49b0-f70f-48b8-9c84-51841882fe75">


- Extracts audio from a video file
- Transcribes the audio using OpenAI Whisper API
- Generates image descriptions for key frames in the video using OpenAI GPT-4 Turbo API
- Combines the audio transcription and image descriptions into a comprehensive response
- Converts the response to speech using OpenAI TTS API



## Demo

### Demo 1



https://github.com/Chivier/easy-gpt4o/assets/41494877/b67b3264-d941-4cab-9f57-69f2b08959b3



https://github.com/Chivier/easy-gpt4o/assets/41494877/abd88e4b-618d-469f-a10c-9e80f79f06ee



https://github.com/Chivier/easy-gpt4o/assets/41494877/12e3ef65-99ed-4c0b-a935-1b3ebffb3984



### Demo 2



https://github.com/Chivier/easy-gpt4o/assets/41494877/4d004d42-473b-4450-8737-20cefdf967a1


https://github.com/Chivier/easy-gpt4o/assets/41494877/7b026c69-d6ec-4545-b9cd-aee73befd647




## TODO

- [ ] Open-source Model Replace OpenAI API
- [ ] Streaming video processing
- [ ] Use RAG store long period memory
      

