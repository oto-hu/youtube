from pytube import YouTube
from moviepy.editor import *
import speech_recognition as sr
import deepl

API_KEY = '' # 自身の API キーを指定
# イニシャライズ
translator = deepl.Translator(API_KEY)

def download_video_from_youtube(url, save_path='.'):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    filename = stream.default_filename
    stream.download(output_path=save_path)
    return os.path.join(save_path, filename)

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            # CMU Sphinxエンジンを使用して音声をテキストに変換
            text = recognizer.recognize_sphinx(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sphinx could not understand audio"
        except sr.RequestError as e:
            return "Sphinx error; {0}".format(e)


def transcribe_from_youtube_url(url, save_path='.'):
    video_path = download_video_from_youtube(url, save_path)
    audio_path = video_path.replace(".mp4", ".wav")
    extract_audio_from_video(video_path, audio_path)
    text = convert_audio_to_text(audio_path)
    return text

def save_transcription_to_file(transcription, filename="transcription.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(transcription.text)


if __name__ == '__main__':
    # YouTubeのURLを指定
    youtube_url = ""
    
    # 関数を呼び出して、文字起こしを実行
    transcription = transcribe_from_youtube_url(youtube_url)
    translated_text = translator.translate_text(transcription, target_lang="JA")
    # 結果をファイルに保存
    save_transcription_to_file(translated_text, "output_transcription.txt")
    
    # 結果を出力
    print(translated_text)
