from flask import Flask, request, jsonify
import whisper
from translatepy import Translator
import ffmpeg
import os
from coqui_tts import TTS

app = Flask(__name__)

# Setup models
whisper_model = whisper.load_model("base")
translator = Translator()
tts = TTS("tts_models/hi/your_model_here")

@app.route('/upload', methods=['POST'])
def upload_video():
    video_file = request.files['file']
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)

    # Step 1: Transcribe the video to text
    transcription = whisper_model.transcribe(video_path)
    translated_text = translate_text(transcription['text'])

    # Step 2: Generate Hindi speech from text
    hindi_audio = generate_hindi_audio(translated_text)

    # Step 3: Merge Hindi audio with video
    dubbed_video = merge_audio_video(video_path, hindi_audio)

    return jsonify({"message": "Video processed successfully", "video_url": dubbed_video})

def translate_text(text):
    return translator.translate(text, "Hindi").result

def generate_hindi_audio(text):
    tts.save_wav(text, "output_audio.wav")
    return "output_audio.wav"

def merge_audio_video(video_path, audio_path):
    output_video = "dubbed_" + video_path
    ffmpeg.input(video_path).output(audio_path, output_video, shortest=None, vcodec='copy', acodec='aac').run()
    return output_video

if __name__ == '__main__':
    app.run(debug=True)
