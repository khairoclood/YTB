#!/usr/bin/env python3
"""
YouTube Arabic Downloader - Debug Version with File Listing
This version shows all files on server and has better error handling
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import json
import os
import threading
from pathlib import Path
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Configuration
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

# Store download status
downloads = {}

print(f"✅ Download directory: {DOWNLOAD_DIR.absolute()}")
print(f"✅ Temp directory: {TEMP_DIR.absolute()}")

# HTML Content - Embedded directly
HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Arabic Downloader</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #667eea;
            font-size: 28px;
            margin-bottom: 10px;
        }

        .header p {
            color: #666;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }

        input[type="text"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
        }

        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 25px;
        }

        .option-card {
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            background: #f9f9f9;
        }

        .option-card:hover {
            border-color: #667eea;
            background: #f0f4ff;
        }

        .option-card input[type="radio"] {
            display: none;
        }

        .option-card.selected {
            border-color: #667eea;
            background: #f0f4ff;
        }

        .option-icon {
            font-size: 24px;
            margin-bottom: 5px;
        }

        .option-label {
            font-size: 12px;
            font-weight: 600;
            color: #666;
            cursor: pointer;
        }

        .button-group {
            display: grid;
            gap: 10px;
            margin-bottom: 20px;
        }

        button {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            font-family: inherit;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover:not(:disabled) {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }

        .btn-download {
            background: #4caf50;
            color: white;
            margin-top: 15px;
            width: 100%;
            font-size: 16px;
            padding: 15px;
        }

        .btn-download:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .message-box {
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 13px;
            line-height: 1.6;
        }

        .info-box {
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            color: #444;
        }

        .error-box {
            background: #ffebee;
            border-left: 4px solid #f44336;
            color: #c62828;
        }

        .success-box {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            color: #2e7d32;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: #667eea;
            width: 0%;
            transition: width 0.3s;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 YouTube Arabic Downloader</h1>
            <p>Download Arabic audio from any YouTube video</p>
        </div>

        <div id="message"></div>

        <div class="form-group">
            <label>YouTube URL</label>
            <input 
                type="text" 
                id="url" 
                placeholder="https://www.youtube.com/watch?v=..." 
            >
        </div>

        <div class="form-group">
            <label>Download Format</label>
            <div class="options">
                <div class="option-card" onclick="selectOption('arabic-audio')">
                    <input type="radio" name="format" id="arabic-audio" value="audio" checked>
                    <div class="option-icon">🎧</div>
                    <label for="arabic-audio" class="option-label">Arabic Audio (MP3)</label>
                </div>
                <div class="option-card" onclick="selectOption('video-arabic')">
                    <input type="radio" name="format" id="video-arabic" value="video">
                    <div class="option-icon">📹</div>
                    <label for="video-arabic" class="option-label">Video + Audio</label>
                </div>
            </div>
        </div>

        <div class="button-group">
            <button class="btn-primary" onclick="download()">⬇️ Download</button>
        </div>

        <div id="download-button-container" style="display: none;">
            <button class="btn-download" onclick="performDownload()" id="downloadBtn">
                📥 Download Your File Now
            </button>
        </div>
    </div>

    <script>
        let currentDownloadId = null;

        function selectOption(optionId) {
            document.getElementById(optionId).checked = true;
            document.querySelectorAll('.option-card').forEach(card => {
                card.classList.remove('selected');
            });
            document.getElementById(optionId).closest('.option-card').classList.add('selected');
        }

        function showMessage(message, type = 'info') {
            const messageDiv = document.getElementById('message');
            const classMap = {
                'error': 'error-box',
                'success': 'success-box',
                'info': 'info-box'
            };
            messageDiv.innerHTML = `<div class="message-box ${classMap[type]}">${message}</div>`;
            messageDiv.scrollIntoView({ behavior: 'smooth' });
        }

        function download() {
            const url = document.getElementById('url').value.trim();
            const format = document.querySelector('input[name="format"]:checked').value;

            if (!url) {
                showMessage('❌ Please enter a YouTube URL', 'error');
                return;
            }

            showMessage('⏳ Starting download... This will take 3-15 minutes', 'info');
            document.getElementById('download-button-container').style.display = 'none';
            
            fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url, format: format })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    showMessage('❌ Error: ' + data.error, 'error');
                } else {
                    currentDownloadId = data.download_id;
                    showMessage('⏳ Processing video... Please wait (this takes time)', 'info');
                    checkDownloadStatus(data.download_id, 0);
                }
            })
            .catch(err => {
                showMessage('❌ Connection error: ' + err.message, 'error');
            });
        }

        function checkDownloadStatus(downloadId, attempts = 0) {
            if (attempts > 120) { // Maximum 10 minutes of checking (120 * 5 seconds)
                showMessage('⚠️ Download is taking longer than expected. Please wait or try again.', 'error');
                return;
            }

            fetch(`/api/download/${downloadId}`)
                .then(res => res.json())
                .then(data => {
                    console.log('Download status:', data);
                    
                    if (data.status === 'completed') {
                        showMessage(`✅ SUCCESS! Your file "${data.video_title}" is ready!`, 'success');
                        document.getElementById('downloadBtn').textContent = `📥 Download: ${data.filename}`;
                        document.getElementById('download-button-container').style.display = 'block';
                    } else if (data.status === 'error') {
                        showMessage('❌ Error: ' + data.message, 'error');
                    } else {
                        showMessage(`⏳ Processing... ${data.message} (${attempts * 5} seconds elapsed)`, 'info');
                        setTimeout(() => checkDownloadStatus(downloadId, attempts + 1), 5000);
                    }
                })
                .catch(err => {
                    showMessage(`⏳ Checking status... ${attempts * 5}s`, 'info');
                    setTimeout(() => checkDownloadStatus(downloadId, attempts + 1), 5000);
                });
        }

        function performDownload() {
            if (!currentDownloadId) {
                showMessage('❌ No download ID found', 'error');
                return;
            }

            showMessage('⏳ Downloading file to your computer...', 'info');
            
            // Method 1: Direct link
            const link = document.createElement('a');
            link.href = `/api/download/${currentDownloadId}/file`;
            link.download = '';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            setTimeout(() => {
                showMessage('✅ File download started! Check your Downloads folder', 'success');
            }, 1000);
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            selectOption('arabic-audio');
            showMessage('✅ Ready! Paste a YouTube URL and click Download', 'info');
        });
    </script>
</body>
</html>
'''


def get_available_audio_tracks(url):
    """Get all available audio tracks for a video"""
    try:
        cmd = ["yt-dlp", "-j", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"❌ yt-dlp error: {result.stderr}")
            return None, []
        
        data = json.loads(result.stdout)
        audio_tracks = []
        title = data.get("title", "Unknown")
        
        if "formats" in data:
            for fmt in data["formats"]:
                if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":
                    lang = fmt.get("language", "unknown")
                    lang_name = fmt.get("language_verbose", lang)
                    
                    audio_tracks.append({
                        "format_id": fmt["format_id"],
                        "language": lang,
                        "language_name": lang_name,
                        "bitrate": fmt.get("abr", fmt.get("tbr", "unknown")),
                        "codec": fmt.get("acodec"),
                        "is_arabic": "ar" in lang.lower() or "arabic" in lang_name.lower()
                    })
        
        print(f"✅ Found {len(audio_tracks)} audio tracks for: {title}")
        return title, audio_tracks
        
    except Exception as e:
        print(f"❌ Error getting tracks: {e}")
        return None, []


def download_audio_background(download_id, url, format_choice):
    """Run download in background thread"""
    try:
        downloads[download_id]["message"] = "Fetching video information..."
        
        title, tracks = get_available_audio_tracks(url)
        
        if not title:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = "Failed to fetch video information"
            print(f"❌ Failed to get video: {url}")
            return
        
        downloads[download_id]["video_title"] = title
        downloads[download_id]["message"] = f"Found: {title}"
        
        if not tracks:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = "No audio tracks found"
            return
        
        # Find Arabic track
        arabic_track = None
        for track in tracks:
            if track["is_arabic"]:
                arabic_track = track
                break
        
        if not arabic_track:
            arabic_track = tracks[0]
        
        downloads[download_id]["message"] = "Starting download from YouTube..."
        downloads[download_id]["status"] = "downloading"
        
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:100]  # Limit filename length
        
        if format_choice == "audio":
            output_template = str(DOWNLOAD_DIR / f"{safe_title}.%(ext)s")
            cmd = [
                "yt-dlp",
                "-f", f"{arabic_track['format_id']}",
                "-x",
                "--audio-format", "mp3",
                "--audio-quality", "192",
                "-o", output_template,
                url
            ]
            output_ext = "mp3"
        else:
            output_template = str(DOWNLOAD_DIR / f"{safe_title}.%(ext)s")
            cmd = [
                "yt-dlp",
                "-f", "best",
                "-o", output_template,
                url
            ]
            output_ext = "mp4"
        
        print(f"🎬 Downloading: {title}")
        print(f"📁 Output: {output_template}")
        print(f"🔧 Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Verify file exists
            files = list(DOWNLOAD_DIR.glob(f"{safe_title}.*"))
            if files:
                actual_filename = files[0].name
                downloads[download_id]["status"] = "completed"
                downloads[download_id]["filename"] = actual_filename
                downloads[download_id]["message"] = f"✅ Download completed!"
                print(f"✅ File saved: {actual_filename}")
            else:
                downloads[download_id]["status"] = "error"
                downloads[download_id]["message"] = "File was not created"
                print(f"❌ File not found after download")
        else:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = f"Download failed: {result.stderr[:200]}"
            print(f"❌ yt-dlp error: {result.stderr}")
            
    except Exception as e:
        downloads[download_id]["status"] = "error"
        downloads[download_id]["message"] = f"Error: {str(e)[:200]}"
        print(f"❌ Exception: {traceback.format_exc()}")


# Routes
@app.route('/', methods=['GET'])
def index():
    """Serve the main page"""
    return HTML_CONTENT


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({"status": "ok", "message": "Server is running"})


@app.route('/api/download', methods=['POST'])
def start_download():
    """Start a download"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        format_choice = data.get('format', 'audio')
        
        if not url:
            return jsonify({"error": "URL required"}), 400
        
        download_id = f"download_{int(datetime.now().timestamp() * 1000)}"
        
        downloads[download_id] = {
            "id": download_id,
            "url": url,
            "format": format_choice,
            "status": "starting",
            "message": "Initializing...",
            "video_title": None,
            "filename": None,
            "started_at": datetime.now().isoformat()
        }
        
        print(f"\n📥 New download request: {download_id}")
        print(f"   URL: {url}")
        print(f"   Format: {format_choice}")
        
        thread = threading.Thread(
            target=download_audio_background,
            args=(download_id, url, format_choice)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "download_id": download_id,
            "status": "started",
            "message": "Download started in background"
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/download/<download_id>', methods=['GET'])
def check_download_status(download_id):
    """Check download status"""
    if download_id not in downloads:
        return jsonify({"error": "Download not found"}), 404
    
    return jsonify(downloads[download_id])


@app.route('/api/download/<download_id>/file', methods=['GET'])
def download_file(download_id):
    """Download the file"""
    try:
        if download_id not in downloads:
            return jsonify({"error": "Download not found"}), 404
        
        download_info = downloads[download_id]
        
        if download_info["status"] != "completed":
            return jsonify({"error": f"Download not ready. Status: {download_info['status']}"}), 400
        
        filename = download_info.get("filename")
        if not filename:
            return jsonify({"error": "No filename"}), 400
        
        filepath = DOWNLOAD_DIR / filename
        
        if not filepath.exists():
            return jsonify({"error": f"File not found: {filename}"}), 404
        
        print(f"📥 Sending file: {filename}")
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"❌ Error sending file: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/files', methods=['GET'])
def list_files():
    """List all downloaded files"""
    files = list(DOWNLOAD_DIR.glob("*"))
    file_list = []
    for f in files:
        if f.is_file():
            file_list.append({
                "name": f.name,
                "size_mb": round(f.stat().st_size / (1024*1024), 2),
                "created": datetime.fromtimestamp(f.stat().st_ctime).isoformat()
            })
    
    return jsonify({
        "files": file_list,
        "total_files": len(file_list),
        "directory": str(DOWNLOAD_DIR.absolute())
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Server error"}), 500


if __name__ == "__main__":
    import sys
    
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"
    
    print("\n" + "="*70)
    print("🎬 YouTube Arabic Downloader - DEBUG VERSION")
    print("="*70)
    print(f"✅ Server starting on http://0.0.0.0:{port}")
    print(f"🌐 Open browser: http://localhost:{port}/")
    print(f"📁 Downloads: {DOWNLOAD_DIR.absolute()}")
    print(f"📊 File list: http://localhost:{port}/api/files")
    print("="*70 + "\n")
    
    app.run(host=host, port=port, debug=False, use_reloader=False)
