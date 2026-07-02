# 🔧 **SETUP FIX - Install Missing Packages**

If nothing is downloading, you're missing **required packages**. This guide will fix it.

---

## 🚀 **QUICK FIX (Do This First)**

### **Step 1: Run the Diagnostic**

```bash
python diagnose.py
```

This will check EVERYTHING and tell you exactly what's missing.

### **Step 2: Fix Issues Based on Output**

The diagnostic will show you exactly what to install.

---

## 📋 **Manual Installation (If Diagnostic Fails)**

### **Most Common Issue: FFmpeg Missing**

FFmpeg is required to convert video/audio. **Install it:**

#### **macOS:**
```bash
brew install ffmpeg
```

#### **Windows:**
**Option A - Using Chocolatey (Recommended):**
```bash
choco install ffmpeg
```

**Option B - Manual Download:**
1. Go to: https://ffmpeg.org/download.html
2. Download Windows build
3. Extract to folder (e.g., `C:\ffmpeg`)
4. Add to PATH:
   - Settings → System → About → Advanced system settings
   - Click "Environment Variables"
   - Add: `C:\ffmpeg\bin` to PATH
   - Restart command prompt

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### **Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg
```

### **Verify FFmpeg Installed:**
```bash
ffmpeg -version
```
Should show version info.

---

### **Second Issue: yt-dlp Missing**

```bash
pip install yt-dlp
```

Verify:
```bash
yt-dlp --version
```

---

### **Third Issue: Flask Missing**

```bash
pip install flask flask-cors
```

---

### **Install Everything at Once:**

```bash
pip install flask flask-cors yt-dlp
```

---

## 🎯 **Complete Step-by-Step Setup**

### **On Windows:**

**1. Install Python** (if you don't have it)
- Download from: python.org
- Make sure to check: "Add Python to PATH"

**2. Open Command Prompt** and run:

```bash
# Install Python packages
pip install flask flask-cors yt-dlp

# Install FFmpeg with Chocolatey
choco install ffmpeg

# If you don't have Chocolatey, download FFmpeg manually from ffmpeg.org
```

**3. Verify everything:**
```bash
python --version
flask --version
yt-dlp --version
ffmpeg -version
```

All should show versions without errors.

**4. Run the app:**
```bash
python diagnose.py
# Should say: ✅ ALL CHECKS PASSED!

python server_debug.py
# Should start the server
```

---

### **On macOS:**

**1. Install Homebrew** (if you don't have it)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install everything:**
```bash
brew install python ffmpeg
pip install flask flask-cors yt-dlp
```

**3. Verify:**
```bash
python3 --version
ffmpeg -version
yt-dlp --version
```

**4. Run the app:**
```bash
python3 diagnose.py
python3 server_debug.py
```

---

### **On Linux (Ubuntu/Debian):**

**1. Install system packages:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip ffmpeg
```

**2. Install Python packages:**
```bash
pip install flask flask-cors yt-dlp
```

**3. Verify:**
```bash
python3 --version
ffmpeg -version
yt-dlp --version
```

**4. Run the app:**
```bash
python3 diagnose.py
python3 server_debug.py
```

---

## ✅ **After Installation, Test**

### **Step 1: Run Diagnostic**
```bash
python diagnose.py
```

Expected output:
```
1️⃣  Checking Python Version...
    ✅ Python 3.10.5

2️⃣  Checking Flask...
    ✅ Flask 2.3.3

3️⃣  Checking FFmpeg...
    ✅ FFmpeg installed

4️⃣  Checking yt-dlp...
    ✅ yt-dlp 2023.9.24

5️⃣  Checking Downloads Folder...
    ✅ Downloads folder writable

6️⃣  Checking Internet Connection...
    ✅ Internet connection working

7️⃣  Testing yt-dlp Functionality...
    ✅ yt-dlp can fetch video info

✅ PASSED: 7/7
✅ ALL CHECKS PASSED!
```

If you see ✅ on all items, you're ready!

### **Step 2: Run Server**
```bash
python server_debug.py
```

Expected:
```
🎬 YouTube Arabic Downloader - DEBUG VERSION
✅ Server starting on http://0.0.0.0:5000
📁 Downloads: /path/to/downloads
📊 File list: http://localhost:5000/api/files
```

### **Step 3: Test in Browser**
```
http://localhost:5000/
```

Should show the beautiful web interface!

### **Step 4: Try Download**
1. Paste YouTube URL
2. Click Download
3. **Watch the terminal** for messages
4. Should see: "✅ File saved: filename.mp3"

---

## 🆘 **Troubleshooting Installation**

### **"python command not found"**
- You need to install Python: python.org
- On Windows, make sure "Add to PATH" is checked
- On Mac/Linux, use `python3` instead of `python`

### **"pip command not found"**
- Reinstall Python with pip included
- Or: `python -m pip install ...` instead of `pip install ...`

### **"FFmpeg not found" after installation**
- On Windows: Add to PATH and restart terminal
- On Mac: `brew install ffmpeg`
- On Linux: `sudo apt-get install ffmpeg`

### **"Permission denied"**
- On Linux/Mac: `sudo pip install flask flask-cors yt-dlp`
- Or: `pip install --user flask flask-cors yt-dlp`

### **"yt-dlp still not working"**
```bash
pip install --upgrade yt-dlp
```

---

## 📦 **What You Need (Summary)**

| Requirement | Windows | macOS | Linux |
|---|---|---|---|
| Python 3.7+ | ✅ install | ✅ install | ✅ apt-get |
| Flask | pip | pip | pip |
| Flask-CORS | pip | pip | pip |
| yt-dlp | pip | pip | pip |
| FFmpeg | choco/manual | brew | apt-get |

---

## ✨ **Quick Command (Install Everything)**

### **Windows:**
```bash
pip install flask flask-cors yt-dlp
choco install ffmpeg
```

### **macOS:**
```bash
brew install ffmpeg
pip install flask flask-cors yt-dlp
```

### **Linux:**
```bash
sudo apt-get install ffmpeg
pip install flask flask-cors yt-dlp
```

---

## 🎯 **After Installation**

1. ✅ Run: `python diagnose.py`
2. ✅ Verify all checks pass
3. ✅ Run: `python server_debug.py`
4. ✅ Open: `http://localhost:5000/`
5. ✅ Download your first Arabic audio! 🎉

---

## 📝 **Common Issues & Solutions**

| Error | Solution |
|---|---|
| "ModuleNotFoundError: No module named 'flask'" | `pip install flask flask-cors` |
| "ffmpeg: command not found" | Install FFmpeg (see steps above) |
| "yt-dlp: command not found" | `pip install yt-dlp` |
| "Permission denied" | Use `sudo` or `pip install --user` |
| "Python command not found" | Install Python from python.org |

---

## 💡 **Pro Tips**

✅ **Use Python 3.10+** for best compatibility
✅ **Update pip** before installing: `pip install --upgrade pip`
✅ **Test each install** after running diagnose.py
✅ **Restart terminal** after PATH changes
✅ **Use virtual environment** if you have Python issues

---

## 🚀 **You're Ready When**

- ✅ `python diagnose.py` shows all green checkmarks
- ✅ `python server_debug.py` starts without errors
- ✅ Browser shows the web interface at `http://localhost:5000/`
- ✅ Downloads folder is created and writable
- ✅ You can download a test video

---

## 📞 **If Still Stuck**

1. Run: `python diagnose.py`
2. Copy the output
3. Tell me what it says
4. I can tell you exactly what to fix!

---

**After installing these packages, EVERYTHING will work!** 🎬✨

Run `python diagnose.py` right now to see what you need!
