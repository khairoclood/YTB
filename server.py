#!/usr/bin/env python3
"""
Flask Backend Server for YouTube Arabic Downloader
Connects the web UI to the actual downloader functionality
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
                # Get audio only formats
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
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None, []
    except subprocess.TimeoutExpired:
        return None, []
    except Exception as e:
        print(f"Error: {e}")
        return None, []


def download_audio_background(download_id, url, audio_only, format_choice):
    """Run download in background thread"""
    try:
        title, tracks = get_available_audio_tracks(url)
        
        if not title:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = "Failed to fetch video information"
            return
        
        downloads[download_id]["video_title"] = title
        downloads[download_id]["message"] = f"Found: {title}"
        
        # Find Arabic track
        arabic_track = None
        for track in tracks:
            if track["is_arabic"]:
                arabic_track = track
                break
        
        if not audio_only and not arabic_track:
            downloads[download_id]["status"] = "warning"
            downloads[download_id]["message"] = "No Arabic audio found, downloading best available audio"
            arabic_track = tracks[0] if tracks else None
        
        if not tracks:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = "No audio tracks found"
            return
        
        downloads[download_id]["message"] = "Starting download..."
        downloads[download_id]["status"] = "downloading"
        
        # Clean title for filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        if format_choice == "arabic-audio":
            # Download audio only
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
            
        elif format_choice == "video-arabic":
            # Download video with Arabic audio
            output_template = str(DOWNLOAD_DIR / f"{safe_title}.%(ext)s")
            cmd = [
                "yt-dlp",
                "-f", "best",
                "-o", output_template,
                url
            ]
            output_ext = "mp4"
            
        elif format_choice == "all-audio":
            # Download with all audio tracks
            output_template = str(DOWNLOAD_DIR / f"{safe_title}.%(ext)s")
            cmd = [
                "yt-dlp",
                "-f", "bestvideo+bestaudio/best",
                "--merge-output-format", "mkv",
                "-o", output_template,
                url
            ]
            output_ext = "mkv"
        
        # Execute download
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            downloads[download_id]["status"] = "completed"
            downloads[download_id]["message"] = f"✅ Download completed! Saved as: {safe_title}.{output_ext}"
            downloads[download_id]["filename"] = f"{safe_title}.{output_ext}"
        else:
            downloads[download_id]["status"] = "error"
            downloads[download_id]["message"] = f"Download failed: {result.stderr}"
            
    except Exception as e:
        downloads[download_id]["status"] = "error"
        downloads[download_id]["message"] = f"Error: {str(e)}"
        print(f"Download error: {traceback.format_exc()}")


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
        format_choice = data.get('format', 'arabic-audio')
        
        if not url:
            return jsonify({"error": "URL required"}), 400
        
        # Create download ID
        download_id = f"download_{int(datetime.now().timestamp() * 1000)}"
        
        # Initialize download status
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
        
        # Start download in background thread
        thread = threading.Thread(
            target=download_audio_background,
            args=(download_id, url, format_choice == "arabic-audio", format_choice)
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


@app.route('/api/download/<download_id>/file', methods=['GET'])
def download_file(download_id):
    """Download the completed file"""
    if download_id not in downloads:
        return jsonify({"error": "Download not found"}), 404
    
    download_info = downloads[download_id]
    
    if download_info["status"] != "completed":
        return jsonify({"error": "Download not completed"}), 400
    
    filename = download_info.get("filename")
    if not filename:
        return jsonify({"error": "Filename not found"}), 400
    
    filepath = DOWNLOAD_DIR / filename
    
    if not filepath.exists():
        return jsonify({"error": "File not found"}), 404
    
    try:
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    """List all downloads"""
    return jsonify({
        "downloads": list(downloads.values())
    })


@app.route('/api/download/<download_id>/cancel', methods=['POST'])
def cancel_download(download_id):
    """Cancel a download"""
    if download_id not in downloads:
        return jsonify({"error": "Download not found"}), 404
    
    if downloads[download_id]["status"] in ["completed", "error"]:
        return jsonify({"error": "Cannot cancel completed or failed download"}), 400
    
    downloads[download_id]["status"] = "cancelled"
    downloads[download_id]["message"] = "Download cancelled by user"
    
    return jsonify({"status": "cancelled"})


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status and directory info"""
    files = list(DOWNLOAD_DIR.glob("*"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    
    return jsonify({
        "server_status": "running",
        "downloads_dir": str(DOWNLOAD_DIR),
        "files_count": len([f for f in files if f.is_file()]),
        "total_size_mb": round(total_size / (1024*1024), 2),
        "active_downloads": len([d for d in downloads.values() if d["status"] == "downloading"])
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    import os
    
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"  # Listen on all interfaces for Railway
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    
    print("\n" + "="*70)
    print("🎬 YouTube Arabic Downloader - Backend Server")
    print("="*70)
    print(f"\n✅ Server starting on http://0.0.0.0:{port}")
    print("📁 Downloads folder: ", DOWNLOAD_DIR.absolute())
    print(f"\n🌐 Environment: {'Development' if debug else 'Production'}")
    print("⚠️  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=False
    )
