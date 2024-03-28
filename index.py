from flask import Flask, request, jsonify
from gtts import gTTS
import os
import subprocess

app = Flask(__name__)

@app.route('/text-to-lipsync', methods=['POST'])
def text_to_lipsync():
    data = request.get_json()
    text = data.get('text', '')
   
    # Convert text to audio using gTTS
    tts = gTTS(text=text, lang='en')
    audio_file = 'audio.mp3'
    tts.save(audio_file)
   
    # Run inference.py script with default parameters
    command = f'python inference.py --checkpoint_path checkpoints\wav2lip_gan.pth --face cr7.mp4 --audio audio.mp3pip'
    subprocess.call(command, shell=True)
   
    # Remove audio file after inference
    os.remove(audio_file)
   
    result_file = 'results/result_voice.mp4'
    if os.path.exists(result_file):
        return jsonify({'message': 'Lip-syncing completed successfully!', 'result_file': result_file}), 200
    else:
        return jsonify({'message': 'Error occurred during lip-syncing!'}), 500

if __name__ == '__main__':
    app.run(debug=True)