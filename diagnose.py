#!/usr/bin/env python3
"""
YouTube Arabic Downloader - Diagnostic Tool
Checks all dependencies and identifies what's missing
"""

import subprocess
import sys
import os
from pathlib import Path

print("\n" + "="*70)
print("🔍 YouTube Arabic Downloader - Diagnostic Check")
print("="*70 + "\n")

issues = []
success_count = 0

# 1. Check Python Version
print("1️⃣  Checking Python Version...")
python_version = sys.version_info
if python_version >= (3, 7):
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    success_count += 1
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor} (need 3.7+)")
    issues.append("Upgrade Python to 3.7 or higher")

# 2. Check Flask
print("\n2️⃣  Checking Flask...")
try:
    import flask
    print(f"   ✅ Flask {flask.__version__}")
    success_count += 1
except ImportError:
    print("   ❌ Flask not installed")
    issues.append("Run: pip install flask flask-cors")

# 3. Check FFmpeg
print("\n3️⃣  Checking FFmpeg...")
try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.decode().split('\n')[0]
        print(f"   ✅ FFmpeg installed")
        print(f"      {version_line}")
        success_count += 1
    else:
        raise Exception("FFmpeg error")
except:
    print("   ❌ FFmpeg not installed")
    issues.append("Install FFmpeg:")
    issues.append("   macOS: brew install ffmpeg")
    issues.append("   Windows: choco install ffmpeg (or download from ffmpeg.org)")
    issues.append("   Linux: sudo apt-get install ffmpeg")

# 4. Check yt-dlp
print("\n4️⃣  Checking yt-dlp...")
try:
    result = subprocess.run(["yt-dlp", "--version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        version = result.stdout.decode().strip()
        print(f"   ✅ yt-dlp {version}")
        success_count += 1
    else:
        raise Exception("yt-dlp error")
except:
    print("   ❌ yt-dlp not installed")
    issues.append("Run: pip install yt-dlp")

# 5. Check Downloads Folder
print("\n5️⃣  Checking Downloads Folder...")
downloads_dir = Path("downloads")
try:
    downloads_dir.mkdir(exist_ok=True)
    test_file = downloads_dir / "test.txt"
    test_file.write_text("test")
    test_file.unlink()
    print(f"   ✅ Downloads folder writable")
    print(f"      Path: {downloads_dir.absolute()}")
    success_count += 1
except Exception as e:
    print(f"   ❌ Cannot write to downloads folder: {e}")
    issues.append(f"Fix permissions: chmod 755 {downloads_dir}/")

# 6. Check Internet Connection
print("\n6️⃣  Checking Internet Connection...")
try:
    result = subprocess.run(
        ["python", "-c", "import urllib.request; urllib.request.urlopen('https://www.youtube.com', timeout=5)"],
        capture_output=True,
        timeout=10
    )
    print("   ✅ Internet connection working")
    success_count += 1
except:
    print("   ⚠️  Cannot reach youtube.com")
    issues.append("Check your internet connection")

# 7. Test yt-dlp with a simple command
print("\n7️⃣  Testing yt-dlp Functionality...")
try:
    result = subprocess.run(
        ["yt-dlp", "-j", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
        capture_output=True,
        timeout=30,
        text=True
    )
    if result.returncode == 0:
        print("   ✅ yt-dlp can fetch video info")
        success_count += 1
    else:
        print(f"   ❌ yt-dlp error: {result.stderr[:100]}")
        issues.append("yt-dlp is installed but not working properly")
        issues.append("Try: pip install --upgrade yt-dlp")
except subprocess.TimeoutExpired:
    print("   ⏱️  yt-dlp test timed out (internet might be slow)")
except Exception as e:
    print(f"   ❌ yt-dlp test failed: {e}")
    issues.append("yt-dlp test failed - check installation")

# Summary
print("\n" + "="*70)
print(f"✅ PASSED: {success_count}/7")
print("="*70)

if issues:
    print("\n🚨 ISSUES FOUND:\n")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
    
    print("\n" + "="*70)
    print("📝 FIX ALL ISSUES ABOVE THEN RUN AGAIN")
    print("="*70 + "\n")
    sys.exit(1)
else:
    print("\n✅ ALL CHECKS PASSED!")
    print("\n🚀 You can now run:")
    print("   python server_debug.py")
    print("\nThen open: http://localhost:5000/")
    print("\n" + "="*70 + "\n")
    sys.exit(0)
