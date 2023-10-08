import os
import subprocess
import openai
from pytube import YouTube

openai.api_key = os.environ.get('OPENAI_API_KEY')


def download_audio_from_youtube(youtube_url, output_path="./files"):
    """Downloads audio from a given YouTube URL."""
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(file_extension="mp4").first()
    return audio_stream.download(output_path)


def transcribe_audio(file_path):
    """Transcribes audio using OpenAI."""
    with open(file_path, "rb") as file:
        return openai.Audio.transcribe("whisper-1", file, response_format="srt", language="ar")


def translate_arabic_to_english(transcription):
    """Translates Arabic transcription to English using OpenAI."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a proficient AI trained in Islamic Arabic translation. Translate the Arabic text into English."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response["choices"][0]["message"]["content"]


def embed_subtitles_to_video(input_file, subtitle_file, output_file):
    """Embeds subtitles into a video using ffmpeg."""
    subtitle_filter = f"subtitles='{subtitle_file}':force_style='Fontname=Sukhumvit Set,FontSize=24,MarginV=30'"
    drawtext_filter = "drawtext=text='By Ilyas Lertsuksakda':x=10:y=h-text_h-10:fontsize=24:fontcolor=white:fontfile='/System/Library/Fonts/Supplemental/SukhumvitSet.ttc'"
    
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"{subtitle_filter},{drawtext_filter}",
        "-c:v", "libx264",
        "-c:a", "copy",
        output_file
    ]
    
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        print(f"Error: {process.stderr.decode()}")
        return False
    return True

def write_to_file(data, file_path):
    """Writes given data to a file."""
    with open(file_path, "w") as file:
        file.write(data)


def process_video(youtube_url):
    """Processes the given video URL by downloading, transcribing, translating, and embedding subtitles."""
    print(f"Downloading {youtube_url}")
    mp4_file_path = download_audio_from_youtube(youtube_url)
    print(f"Downloaded to {mp4_file_path}")

    print("Transcribing the video")
    arabic_transcription = transcribe_audio(mp4_file_path)
    arabic_transcription_file_path = mp4_file_path.replace(".mp4", "_ar.srt")
    write_to_file(arabic_transcription, arabic_transcription_file_path)

    print("Translating the video to English")
    english_translation = translate_arabic_to_english(arabic_transcription)
    english_translation_file_path = mp4_file_path.replace(".mp4", "_en.srt")
    write_to_file(english_translation, english_translation_file_path)

    print("Embedding English subtitle to the video")
    if embed_subtitles_to_video(mp4_file_path, english_translation_file_path, mp4_file_path.replace(".mp4", "_en.mp4")):
        print("Embedding English subtitles completed!")


if __name__ == "__main__":
    process_video("https://www.youtube.com/watch?v=7z161Mn0wwI")
