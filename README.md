# 🎬 YouTube Arabic Audio Downloader

Download Arabic audio tracks from any YouTube video - powered by Python, Flask, and yt-dlp.

**Live Demo:** [Deploy on Railway](#-deploy-on-railway---1-click-deployment)

## ✨ Features

- 🇸🇦 **Auto-detect Arabic Audio** - Automatically finds Arabic dubbed/dubbed audio tracks
- 🎧 **Audio-Only Download** - Extract just the audio as MP3 (perfect for learning)
- 📹 **Video + Arabic Audio** - Download full video with Arabic audio merged
- 🌍 **Multi-Language Support** - Download videos with all available audio tracks in MKV format
- 📊 **Track Preview** - List all available audio tracks before downloading
- 💻 **Web Interface** - Beautiful, easy-to-use UI (no command line needed)
- ⚡ **Fast Processing** - Uses ffmpeg for optimal quality
- 🚀 **Cloud Ready** - Deployable on Railway, Render, or your VPS

## 📸 Screenshots

```
Web Interface:
┌─────────────────────────────────────┐
│   🎬 YouTube Arabic Downloader     │
│                                     │
│  📝 Paste YouTube URL              │
│  🎧 Select: Arabic Audio Only      │
│  ⬇️  Click Download                 │
│                                     │
│  ✅ Done! Get your file            │
└─────────────────────────────────────┘
```

## 🚀 Deploy on Railway - 1-Click Deployment

### Fastest Way (5 minutes)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

**Step-by-step:**

1. **Create GitHub Account** (if needed)
   - Go to github.com → Sign up

2. **Upload to GitHub**
   - Create new repo: `youtube-arabic-downloader`
   - Upload all files from this project
   - Make repository PUBLIC

3. **Deploy on Railway**
   - Go to railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose your repository
   - Click "Deploy"

4. **Wait 2-3 minutes** for deployment

5. **Get Your URL**
   - Railway shows: `https://youtube-arabic-downloader-xxx.up.railway.app`
   - Open: `https://your-url/youtube_downloader_ui.html`

**Your YouTube downloader is now LIVE!** 🎉

---

## 🏠 Run Locally

### Prerequisites
- Python 3.7+
- FFmpeg
- yt-dlp

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run server
python server.py

# 3. Open browser
# Go to: http://localhost:5000/youtube_downloader_ui.html
```

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
choco install ffmpeg
```
Or download from: https://ffmpeg.org/download.html

**Linux:**
```bash
sudo apt-get install ffmpeg
```

---

## 📁 Project Structure

```
youtube-arabic-downloader/
├── server.py                      # Flask backend server
├── youtube_arabic_downloader.py   # Main downloader logic
├── youtube_downloader_ui.html     # Web interface
├── requirements.txt               # Python dependencies
├── Procfile                       # Railway deployment config
├── .gitignore                     # Git ignore rules
├── README.md                      # Documentation
└── downloads/                     # Output folder (created on first run)
```

---

## 🎯 How to Use

### Via Web Interface

1. **Open the web app** (local or Railway URL)
2. **Paste YouTube URL**
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```
3. **Choose format:**
   - 🎧 Arabic Audio Only (MP3)
   - 📹 Video + Arabic Audio
   - 🌍 All Audio Tracks (MKV)
   - 📋 List Tracks (preview)

4. **Click Download**
5. **Wait for completion** (time depends on video length)
6. **Download your file**

### Examples

| Video | Format | Result |
|-------|--------|--------|
| MrBeast (English) | Arabic Audio Only | Get Arabic audio as MP3 |
| Educational Video | Video + Arabic | Full video in Arabic |
| Multilingual Content | All Tracks | MKV with all languages |

---

## 🔧 API Endpoints

If you want to integrate with your app:

```bash
# Get available tracks
POST /api/tracks
Body: {"url": "https://youtube.com/watch?v=..."}
Response: {"title": "...", "tracks": [...], "has_arabic": true}

# Start download
POST /api/download
Body: {"url": "...", "format": "arabic-audio"}
Response: {"download_id": "...", "status": "started"}

# Check status
GET /api/download/{download_id}
Response: {"status": "downloading", "message": "...", "progress": 45}

# Get all downloads
GET /api/downloads
Response: {"downloads": [...]}

# Server health
GET /api/health
Response: {"status": "ok"}
```

---

## ⚙️ Configuration

### Environment Variables

On Railway, these are auto-configured:
- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Environment (production)

### Customize Output

Edit `server.py` to change:
```python
DOWNLOAD_DIR = Path("downloads")  # Change output folder
TEMP_DIR = Path("temp")           # Change temp folder
```

---

## 📊 Performance

| Feature | Local | Railway |
|---------|-------|---------|
| Speed | ⚡⚡⚡ | ⚡⚡ |
| Storage | Unlimited | 512MB+ |
| Uptime | Depends | 99.9% |
| FFmpeg | Manual install | Built-in ✅ |
| Cost | Free | Free (after $5 credit) |

### Timeout

- **Local:** No limit
- **Railway:** No limit ✅ (unlike Vercel/AWS Lambda)

---

## 🐛 Troubleshooting

### "No Arabic track found"
- Video might not have Arabic audio
- Use "List Tracks" option to see what's available
- Some videos use different language codes

### "FFmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg
```

### Download fails
- Check internet connection
- Verify YouTube URL is valid
- Check if video is region-restricted
- Try again (YouTube sometimes blocks)

### Server won't start
```bash
# Make sure port 5000 is available
# Try: python server.py

# If still fails, check logs for errors
```

### Railway deployment fails
- Check requirements.txt syntax
- Verify Procfile is correct
- Check GitHub repository is PUBLIC
- View deployment logs in Railway dashboard

---

## 💾 File Management

### Downloaded Files
Files are saved in `downloads/` folder with clean names:
```
Song Title.mp3
Video Name.mp4
Movie Title.mkv
```

### Storage Limits
- **Local:** Unlimited (depends on your disk)
- **Railway:** ~512MB free storage
- **If you need more:** Upgrade Railway plan

### Delete Files
```bash
rm downloads/*  # Delete all downloads
```

---

## 🔐 Security & Legal

### ✅ Do's
- Download content for personal use
- Use for learning and education
- Preserve multilingual content
- Respect copyright laws

### ❌ Don'ts
- Don't distribute downloaded content
- Don't use for commercial purposes
- Don't circumvent DRM protections
- Don't violate YouTube ToS

### Legal Notice
This tool is for personal, non-commercial use only. Respect intellectual property rights and YouTube's Terms of Service.

---

## 🌟 Advanced Usage

### Batch Download

```python
from youtube_arabic_downloader import YouTubeArabicDownloader

downloader = YouTubeArabicDownloader()
urls = [
    "https://youtube.com/watch?v=...",
    "https://youtube.com/watch?v=...",
]

for url in urls:
    downloader.download_arabic_audio(url, audio_only=True)
```

### Check Available Tracks

```python
title, tracks = downloader.get_available_audio_tracks(url)
for track in tracks:
    print(f"{track['language_name']}: {track['bitrate']} kbps")
```

---

## 📚 Dependencies

- **Flask** - Web framework
- **flask-cors** - CORS support
- **yt-dlp** - YouTube downloader
- **FFmpeg** - Media processing

All automatically installed with `pip install -r requirements.txt`

---

## 🚀 Deploy on Other Platforms

### Render (Similar to Railway)
1. Push to GitHub
2. Go to render.com
3. Connect GitHub repository
4. Deploy

### Replit (Browser-based)
1. Go to replit.com
2. Create new project from GitHub
3. Click "Run"

### DigitalOcean (VPS - $5/month)
1. Create droplet
2. SSH in
3. `git clone your-repo`
4. `pip install -r requirements.txt`
5. `python server.py`

### Heroku (Paid - $7+)
```bash
heroku login
git push heroku main
```

---

## 📈 Roadmap

- [ ] Subtitle downloading
- [ ] Playlist support
- [ ] Advanced audio filtering
- [ ] Cloud storage integration (S3)
- [ ] Database for download history
- [ ] Progress indicators
- [ ] Mobile app
- [ ] Desktop application

---

## 🤝 Contributing

Want to improve this project?

1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

Contributions welcome! 🎉

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🆘 Support

- **Issues?** Check troubleshooting section above
- **Questions?** Open an issue on GitHub
- **Feature requests?** Create a GitHub discussion
- **Deployment help?** Check DEPLOY_RAILWAY_QUICK.md

---

## 🙏 Credits

Built with:
- **yt-dlp** - Modern YouTube downloader
- **FFmpeg** - Multimedia framework
- **Flask** - Python web framework
- **Railway** - Cloud deployment platform

---

## 📊 Stats

- ⭐ Downloads: Arabic audio automatically
- 🎧 Formats: MP3, MP4, MKV
- 🌍 Languages: Any available on YouTube
- ⚡ Speed: Depends on video length
- 💰 Cost: Free to $5-20/month

---

## 🎉 Ready to Deploy?

### Quick Checklist

- [ ] Files downloaded locally
- [ ] GitHub account created
- [ ] Repository created
- [ ] Files uploaded to GitHub
- [ ] Railway account created
- [ ] Deployed on Railway
- [ ] Testing with YouTube URL
- [ ] Sharing with friends

**Follow DEPLOY_RAILWAY_QUICK.md for step-by-step instructions!**

---

## 📞 Contact

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Email: Check repository

---

**Enjoy downloading Arabic audio! الاستمتاع بالتحميل! 🚀**

Made with ❤️ for Arabic learners and content creators.
