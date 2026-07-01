#!/usr/bin/env python3
"""
YouTube Arabic Downloader - Standalone Server
Everything in one file - no file dependencies!
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
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .header p {
            color: #666;
            font-size: 14px;
        }

        .emoji {
            font-size: 32px;
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
            transition: all 0.3s;
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
            transition: all 0.3s;
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

        .option-card input[type="radio"]:checked + .option-label {
            color: #667eea;
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
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: #666;
            cursor: pointer;
        }

        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
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
            grid-column: 1 / -1;
        }

        .btn-primary:hover:not(:disabled) {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }

        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }

        .btn-secondary:hover:not(:disabled) {
            background: #e0e0e0;
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .info-box {
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 13px;
            color: #444;
            line-height: 1.6;
        }

        .error-box {
            background: #ffebee;
            border-left: 4px solid #f44336;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 13px;
            color: #c62828;
        }

        .success-box {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 13px;
            color: #2e7d32;
        }

        .features {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }

        .features h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 14px;
        }

        .feature-list {
            display: grid;
            gap: 10px;
        }

        .feature-item {
            display: flex;
            gap: 10px;
            font-size: 13px;
            color: #666;
        }

        .feature-item::before {
            content: "✓";
            color: #4caf50;
            font-weight: bold;
            min-width: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="emoji">🎬</span> YouTube Arabic Downloader</h1>
            <p>Download Arabic audio tracks from any YouTube video</p>
        </div>

        <div class="info-box">
            <strong>✅ Server Status:</strong> Connected and ready!
        </div>

        <div id="message"></div>

        <div class="form-group">
            <label>YouTube URL</label>
            <input 
                type="text" 
                id="url" 
                placeholder="https://www.youtube.com/watch?v=..." 
                value=""
            >
        </div>

        <div class="form-group">
            <label>Download Format</label>
            <div class="options">
                <div class="option-card" onclick="selectOption('arabic-audio')">
                    <input type="radio" name="format" id="arabic-audio" value="audio" checked>
                    <div class="option-icon">🎧</div>
                    <label for="arabic-audio" class="option-label">Arabic Audio Only (MP3)</label>
                </div>
                <div class="option-card" onclick="selectOption('video-arabic')">
                    <input type="radio" name="format" id="video-arabic" value="video">
                    <div class="option-icon">📹</div>
                    <label for="video-arabic" class="option-label">Video + Arabic Audio</label>
                </div>
            </div>
        </div>

        <div class="button-group">
            <button class="btn-secondary" onclick="listTracks()">📋 Check Tracks</button>
            <button class="btn-primary" onclick="download()">⬇️ Download</button>
        </div>

        <div class="features">
            <h3>✨ Features</h3>
            <div class="feature-list">
                <div class="feature-item">Auto-detect Arabic audio tracks</div>
                <div class="feature-item">Download audio-only in MP3 format</div>
                <div class="feature-item">Support for videos with multiple languages</div>
                <div class="feature-item">High-quality audio extraction</div>
            </div>
        </div>
    </div>

    <script>
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
            messageDiv.innerHTML = `<div class="${classMap[type]}">${message}</div>`;
        }

        function listTracks() {
            const url = document.getElementById('url').value.trim();
            if (!url) {
                showMessage('❌ Please enter a YouTube URL', 'error');
                return;
            }

            showMessage('⏳ Fetching track information...', 'info');
            
            fetch('/api/tracks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    showMessage('❌ Error: ' + data.error, 'error');
                } else {
                    showMessage(`✅ Found ${data.tracks.length} audio track(s)!`, 'success');
                }
            })
            .catch(err => showMessage('❌ Error: ' + err.message, 'error'));
        }

        function download() {
            const url = document.getElementById('url').value.trim();
            const format = document.querySelector('input[name="format"]:checked').value;

            if (!url) {
                showMessage('❌ Please enter a YouTube URL', 'error');
                return;
            }

            showMessage('⏳ Starting download... Please wait (this may take a few minutes)', 'info');
            
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
                    showMessage('✅ Download started! Downloading in background...', 'success');
                    // Check status every 5 seconds
                    checkDownloadStatus(data.download_id);
                }
            })
            .catch(err => showMessage('❌ Error: ' + err.message, 'error'));
        }

        function checkDownloadStatus(downloadId) {
            setTimeout(() => {
                fetch(`/api/download/${downloadId}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === 'completed') {
                            showMessage('✅ Download completed! File ready.', 'success');
                        } else if (data.status === 'error') {
                            showMessage('❌ Error: ' + data.message, 'error');
                        } else if (data.status === 'downloading') {
                            showMessage(`⏳ ${data.message}`, 'info');
                            checkDownloadStatus(downloadId);
                        }
                    });
            }, 5000);
        }

        // Set initial selection
        document.addEventListener('DOMContentLoaded', () => {
            selectOption('arabic-audio');
            showMessage('✅ Connected to server and ready to download!', 'success');
        });
    </script>
</body>
</html>
'''


def get_available_audio_tracks(url):
    """Get all available audio tracks for a video"""
    try:
        cmd = [
            "yt-dlp",
            "-j",
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
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
        
        return title, audio_tracks
        
    except Exception as e:
        print(f"Error: {e}")
        return None, []


def download_audio_background(download_id, url, format_choice):
    """Run download in background thread"""
    try:
        title, tracks = get_available_audio_tracks(url)
        
        if not title:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = "Failed to fetch video information"
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
        
        downloads[download_id]["message"] = "Starting download..."
        downloads[download_id]["status"] = "downloading"
        
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
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
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            downloads[download_id]["status"] = "completed"
            downloads[download_id]["message"] = f"✅ Download completed! Saved as: {safe_title}.{output_ext}"
            downloads[download_id]["filename"] = f"{safe_title}.{output_ext}"
        else:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = f"Download failed: {result.stderr[:200]}"
            
    except Exception as e:
        downloads[download_id]["status"] = "error"
        downloads[download_id]["message"] = f"Error: {str(e)[:200]}"


# Routes
@app.route('/', methods=['GET'])
def index():
    """Serve the main page with embedded HTML"""
    return HTML_CONTENT


@app.route('/youtube_downloader_ui.html', methods=['GET'])
def serve_ui():
    """Serve the UI (same as index)"""
    return HTML_CONTENT


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Server is running"})


@app.route('/api/tracks', methods=['POST'])
def get_tracks():
    """Get available audio tracks for a video"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"error": "URL required"}), 400
        
        title, tracks = get_available_audio_tracks(url)
        
        if not title:
            return jsonify({"error": "Failed to fetch video information"}), 400
        
        return jsonify({
            "title": title,
            "tracks": tracks,
            "has_arabic": any(t["is_arabic"] for t in tracks)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/download', methods=['POST'])
def start_download():
    """Start a download in the background"""
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
            "message": "Initializing download...",
            "progress": 0,
            "video_title": None,
            "filename": None,
            "started_at": datetime.now().isoformat()
        }
        
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
        return jsonify({"error": str(e)}), 500


@app.route('/api/download/<download_id>', methods=['GET'])
def check_download_status(download_id):
    """Check the status of a download"""
    if download_id not in downloads:
        return jsonify({"error": "Download not found"}), 404
    
    return jsonify(downloads[download_id])


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status and directory info"""
    files = list(DOWNLOAD_DIR.glob("*"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    
    return jsonify({
        "server_status": "running",
        "downloads_dir": str(DOWNLOAD_DIR.absolute()),
        "files_count": len([f for f in files if f.is_file()]),
        "total_size_mb": round(total_size / (1024*1024), 2),
        "active_downloads": len([d for d in downloads.values() if d["status"] == "downloading"])
    })


@app.route('/api/diagnostics', methods=['GET'])
def diagnostics():
    """Diagnostic information"""
    return jsonify({
        "status": "ok",
        "message": "Server is running correctly",
        "html_embedded": True,
        "endpoints": {
            "home": "/",
            "api_tracks": "/api/tracks",
            "api_download": "/api/download",
            "api_status": "/api/status",
            "api_health": "/api/health"
        }
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found. Try: / or /api/health"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    import sys
    
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    
    print("\n" + "="*70)
    print("🎬 YouTube Arabic Downloader - Standalone Server")
    print("="*70)
    print(f"\n✅ Server starting on http://0.0.0.0:{port}")
    print(f"📁 Downloads folder: {DOWNLOAD_DIR.absolute()}")
    print(f"\n🌐 Open your browser at:")
    print(f"   http://localhost:{port}/")
    print(f"   or")
    print(f"   http://localhost:{port}/youtube_downloader_ui.html")
    print(f"\n✅ HTML is embedded in server - no file dependencies!")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=False
    )
