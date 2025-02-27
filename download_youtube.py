from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

DOWNLOAD_FOLDER = os.path.expanduser(r'C:\Users\kumar\Downloads')  # Save videos in Downloads
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"message": "Invalid URL"}), 400

    try:
        # Generate a timestamped filename to ensure uniqueness
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_path = os.path.join(DOWNLOAD_FOLDER, f"YouTube_Video_{current_date}.mp4")

        # yt-dlp command to download video
        command = [
            r'C:\Users\kumar\AppData\Roaming\Python\Python313\Scripts\yt-dlp.exe',
            '-o', video_path,  
            '-f', 'best',  # Download best quality format
            video_url
        ]

        # Run download command
        subprocess.run(command, check=True)

        # Return file to the frontend for browser download history
        return send_file(video_path, as_attachment=True)

    except subprocess.CalledProcessError:
        return jsonify({"message": "Download failed"}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run on port 5000
