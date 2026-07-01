#!/usr/bin/env python3
"""
YouTube Arabic Audio Downloader
Downloads videos with Arabic audio track extraction
Requires: yt-dlp, ffmpeg
"""

import subprocess
import json
import os
import sys
from pathlib import Path


class YouTubeArabicDownloader:
    def __init__(self):
        self.output_dir = Path("downloads")
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)

    def check_dependencies(self):
        """Check if yt-dlp and ffmpeg are installed"""
        dependencies = {
            "yt-dlp": "pip install yt-dlp",
            "ffmpeg": "brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
        }
        
        for dep, install_cmd in dependencies.items():
            result = subprocess.run(
                ["which" if sys.platform != "win32" else "where", dep],
                capture_output=True
            )
            if result.returncode != 0:
                print(f"❌ {dep} not found. Install with: {install_cmd}")
                return False
        return True

    def get_available_audio_tracks(self, url):
        """Get all available audio tracks for a video"""
        try:
            cmd = [
                "yt-dlp",
                "-j",  # JSON output
                "--dump-json",
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            audio_tracks = []
            if "formats" in data:
                for fmt in data["formats"]:
                    if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":
                        lang = fmt.get("language", "unknown")
                        lang_name = fmt.get("language_verbose", lang)
                        bitrate = fmt.get("abr", fmt.get("tbr", "unknown"))
                        
                        audio_tracks.append({
                            "format_id": fmt["format_id"],
                            "language": lang,
                            "language_name": lang_name,
                            "bitrate": bitrate,
                            "codec": fmt.get("acodec"),
                            "size": fmt.get("filesize", "unknown")
                        })
            
            return data.get("title", "Unknown"), audio_tracks
            
        except json.JSONDecodeError:
            print("Error parsing video information")
            return None, []

    def find_arabic_track(self, tracks):
        """Find Arabic audio track from available tracks"""
        arabic_keywords = ["ar", "ara", "arabic", "العربية"]
        
        for track in tracks:
            lang = track["language"].lower() if track["language"] else ""
            lang_name = track["language_name"].lower() if track["language_name"] else ""
            
            if any(keyword in lang or keyword in lang_name for keyword in arabic_keywords):
                return track
        
        return None

    def download_arabic_audio(self, url, audio_only=True):
        """Download video with Arabic audio track"""
        print("\n🎬 YouTube Arabic Audio Downloader")
        print("=" * 50)
        
        print("\n📝 Getting video information...")
        title, tracks = self.get_available_audio_tracks(url)
        
        if not title:
            print("❌ Failed to get video information. Check the URL.")
            return False
        
        print(f"✅ Title: {title}")
        print(f"📊 Found {len(tracks)} audio track(s)")
        
        if not tracks:
            print("❌ No audio tracks found")
            return False
        
        # Display all available tracks
        print("\n📋 Available Audio Tracks:")
        print("-" * 50)
        for i, track in enumerate(tracks):
            marker = "🇸🇦" if "ar" in track["language"].lower() else "  "
            print(f"{marker} {i+1}. {track['language_name']} - {track['codec']} - {track['bitrate']} kbps")
        
        # Find Arabic track
        print("\n🔍 Looking for Arabic audio track...")
        arabic_track = self.find_arabic_track(tracks)
        
        if not arabic_track:
            print("❌ No Arabic audio track found")
            print("Available tracks:")
            for track in tracks:
                print(f"  - {track['language_name']}")
            return False
        
        print(f"✅ Found Arabic track: {arabic_track['language_name']}")
        
        # Download
        print("\n⬇️  Downloading...")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        if audio_only:
            output_template = str(self.output_dir / f"{safe_title}.%(ext)s")
            cmd = [
                "yt-dlp",
                "-f", f"{arabic_track['format_id']}",
                "-x",  # Extract audio
                "--audio-format", "mp3",
                "--audio-quality", "192",
                "-o", output_template,
                url
            ]
            print("Downloading Arabic audio as MP3...")
        else:
            output_template = str(self.output_dir / f"{safe_title}.%(ext)s")
            cmd = [
                "yt-dlp",
                "-f", f"best[language={arabic_track['language']}]",
                "-o", output_template,
                url
            ]
            print("Downloading video with Arabic audio...")
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("\n✅ Download complete!")
            return True
        else:
            print("\n❌ Download failed")
            return False

    def download_video_with_all_audio(self, url):
        """Download video keeping all audio tracks"""
        print("\n🎬 YouTube Video Downloader (All Audio Tracks)")
        print("=" * 50)
        
        print("\n📝 Getting video information...")
        title, tracks = self.get_available_audio_tracks(url)
        
        if not title:
            print("❌ Failed to get video information")
            return False
        
        print(f"✅ Title: {title}")
        print(f"📊 Found {len(tracks)} audio track(s)")
        
        print("\n⬇️  Downloading video with all audio tracks...")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        output_template = str(self.output_dir / f"{safe_title}.%(ext)s")
        
        cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mkv",
            "-o", output_template,
            url
        ]
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("\n✅ Download complete!")
            return True
        else:
            print("\n❌ Download failed")
            return False


def main():
    downloader = YouTubeArabicDownloader()
    
    # Check dependencies
    if not downloader.check_dependencies():
        print("\n⚠️  Please install missing dependencies first")
        return
    
    print("\n🌍 YouTube Arabic Audio Downloader")
    print("=" * 50)
    print("\nOptions:")
    print("1. Download Arabic audio only (as MP3)")
    print("2. Download video with Arabic audio")
    print("3. Download video with all audio tracks (MKV)")
    print("4. List audio tracks for a video")
    
    choice = input("\nSelect option (1-4): ").strip()
    url = input("Enter YouTube URL: ").strip()
    
    if not url:
        print("❌ URL required")
        return
    
    if choice == "1":
        downloader.download_arabic_audio(url, audio_only=True)
    elif choice == "2":
        downloader.download_arabic_audio(url, audio_only=False)
    elif choice == "3":
        downloader.download_video_with_all_audio(url)
    elif choice == "4":
        title, tracks = downloader.get_available_audio_tracks(url)
        if tracks:
            print(f"\n📺 {title}\n")
            for track in tracks:
                print(f"  🔊 {track['language_name']} ({track['language']})")
                print(f"     Codec: {track['codec']}, Bitrate: {track['bitrate']} kbps\n")
        else:
            print("No audio tracks found")
    else:
        print("❌ Invalid option")


if __name__ == "__main__":
    main()
