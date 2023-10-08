# Auto Subs Embedder

Auto Subs Embedder is a tool specifically designed for Arabic videos. It automates the process of downloading audio from a YouTube video, transcribing the Arabic audio, translating the transcription, and embedding the resulting subtitles back into the video.

## Features

- **Download Audio from YouTube**: Extracts the audio track from a given YouTube video URL.
- **Transcribe Arabic Audio**: Utilizes OpenAI to transcribe the downloaded Arabic audio.
- **Translate Arabic Transcription**: Translates the Arabic transcription into English using OpenAI's GPT-4 model.
- **Embed Subtitles**: Embeds the generated subtitles into the original video using `ffmpeg`.

## Installation

1. Ensure you have `ffmpeg` installed:
    ```bash
    # For macOS using Homebrew
    brew install ffmpeg
    ```

2. Install the required Python packages:
    ```bash
    pip install openai pytube
    ```

3. Clone this repository:
    ```bash
    git clone https://github.com/rathawut/auto-subs-embedder
    cd auto-subs-embedder
    ```

4. Export your OpenAI API key directly in your terminal:
    ```bash
    export OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

Run the `main.py` script with Python:

```bash
python main.py
