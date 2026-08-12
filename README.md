# 🎬 ASCII Video Converter

> Convert any video into stunning ASCII art video with GPU acceleration support.
> Ubah video apa pun menjadi video seni ASCII yang memukau dengan dukungan akselerasi GPU.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/FFmpeg-Required-green?logo=ffmpeg&logoColor=white" alt="FFmpeg">
  <img src="https://img.shields.io/badge/GPU-CUDA%20%7C%20CPU-76B900?logo=nvidia&logoColor=white" alt="GPU Support">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform">
</p>

<p align="center">
  <a href="#-features--fitur">Features</a> •
  <a href="#-installation--instalasi">Installation</a> •
  <a href="#-usage--penggunaan">Usage</a> •
  <a href="#-configuration-options--opsi-konfigurasi">Configuration</a> •
  <a href="#-troubleshooting">Troubleshooting</a>
</p>

---

## 🎥 Demo Video

> **Watch the full demonstration / Tonton video demonstrasi lengkap:**
>
> [![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
>
> *Replace `YOUR_VIDEO_ID` with your actual YouTube video ID / Ganti `YOUR_VIDEO_ID` dengan ID video YouTube Anda.*

---

## ✨ Features / Fitur

| English | Indonesia |
|---------|-----------|
| 🎨 Multiple color presets (Matrix, Cyber, Fire, etc.) | 🎨 Berbagai preset warna (Matrix, Cyber, Fire, dll.) |
| 🖥️ NVIDIA CUDA GPU acceleration (auto-detect) | 🖥️ Akselerasi GPU NVIDIA CUDA (deteksi otomatis) |
| ⚡ Fully vectorized rendering (no per-cell loops) | ⚡ Rendering ter-vektorisasi penuh (tanpa loop per-sel) |
| 🔊 Audio extraction & merging with FFmpeg | 🔊 Ekstraksi & penggabungan audio dengan FFmpeg |
| 📐 Custom resolution, FPS, and column count | 📐 Resolusi, FPS, dan jumlah kolom kustom |
| 📁 Choose output folder (same as input or custom) | 📁 Pilih folder output (sama dengan input atau kustom) |
| 📊 Real-time progress bar | 📊 Progress bar real-time |
| 🖱️ Drag-and-drop or CLI argument support | 🖱️ Dukungan drag-and-drop atau argumen CLI |

---

## 📸 Preview / Pratinjau

```text
Original Video Frame             ASCII Art Output
┌────────────────────┐           ┌────────────────────┐
│                    │           │ @#%*+=-:. °±¼½¾¡¿  │
│      (Image)       │   ===►    │ #*+=-:. °±¼½¾¡¿ @# │
│                    │           │ %*+=-:. °±¼½¾¡¿ @# │
└────────────────────┘           └────────────────────┘
```

<details>
<summary>🎨 Available color presets / Preset warna yang tersedia</summary>

| # | Name | Preview |
|---|------|---------|
| 1 | Hijau (Matrix) | 🟢 `#00FF46` |
| 2 | Putih (Classic) | ⚪ `#FFFFFF` |
| 3 | Biru (Cyber) | 🔵 `#0096FF` |
| 4 | Merah (Fire) | 🔴 `#FF3232` |
| 5 | Kuning (Amber) | 🟡 `#FFC800` |
| 6 | Ungu (Neon) | 🟣 `#C832FF` |
| 7 | Cyan (Aqua) | 🩵 `#00FFFF` |

</details>

---

## 🛠️ Requirements / Prasyarat

- **Python** 3.8 or newer
- **FFmpeg** installed and available on your `PATH`
- (Optional) **NVIDIA GPU + CUDA** for accelerated rendering — falls back to CPU automatically if unavailable

**Python dependencies:**

```text
opencv-python
numpy
Pillow
tqdm
cupy-cudaXXx   # optional, only for GPU acceleration
```

---

## 📦 Installation / Instalasi

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ascii-video-converter.git
cd ascii-video-converter

# 2. Install Python dependencies
pip install opencv-python numpy Pillow tqdm

# 3. (Optional) Install CuPy for GPU acceleration — match your CUDA version
pip install cupy-cuda12x

# 4. Install FFmpeg
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux (Debian/Ubuntu)
sudo apt install ffmpeg
```

---

## 🚀 Usage / Penggunaan

### Interactive mode

```bash
python ascii_video_converter.py
```

You'll be guided through an interactive setup:

1. 📁 Provide the video path (or drag-and-drop the file into the terminal)
2. 🎬 Choose FPS (24 / 30 / 60 / custom)
3. 🔤 Choose ASCII width in columns (80 / 120 / 160 / 200 / custom)
4. 📺 Choose output resolution (HD / Full HD / 2K / 4K / custom)
5. 🎨 Pick a color preset
6. 🔊 Decide whether to keep the original audio
7. 💾 Choose where the output file is saved

### CLI / drag-and-drop mode

```bash
python ascii_video_converter.py "path/to/your/video.mp4"
```

Drag a video file directly onto the script (Windows) to skip the manual path prompt.

---

## ⚙️ Configuration Options / Opsi Konfigurasi

| Option | Choices | Description |
|--------|---------|--------------|
| **FPS** | 24 / 30 / 60 / Custom (10–120) | Output frame rate |
| **Columns** | 80 / 120 / 160 / 200 / Custom (40–300) | ASCII grid width — higher = more detail, slower render |
| **Resolution** | HD / Full HD / 2K / 4K / Custom | Output video resolution |
| **Color** | 7 presets | ASCII character color |
| **Audio** | Yes / No | Keep original audio track |
| **Output folder** | Same as input / Custom | Where the final `.mp4` is saved |

---

## 🧠 How It Works / Cara Kerja

```
Video Input → Frame Extraction (OpenCV) → Grayscale Conversion
     → Pixel-to-Character Mapping → Sprite Sheet Lookup (vectorized)
     → Canvas Composition → FFmpeg Encode → Audio Merge → Final MP4
```

Rendering is fully vectorized with NumPy (CPU) or CuPy (GPU) — every character cell for a frame is resolved in a single array operation instead of a per-pixel Python loop, which keeps large grids and 4K output responsive.

---

## 📁 Project Structure / Struktur Proyek

```
ascii-video-converter/
├── ascii_video_converter.py   # Main script
├── logs/                      # Auto-generated runtime logs
└── README.md
```

---

## 🐛 Troubleshooting

<details>
<summary><b>❌ "FFmpeg tidak ditemukan"</b></summary>

Make sure FFmpeg is installed and available on your system `PATH`. Test with:
```bash
ffmpeg -version
```
</details>

<details>
<summary><b>🐢 Rendering is slow</b></summary>

- Lower the column count (e.g. 80–120) for faster renders
- Lower the target FPS
- If you have an NVIDIA GPU, install CuPy matching your CUDA version to enable GPU rendering
</details>

<details>
<summary><b>🔇 Audio missing from output</b></summary>

Audio merging requires FFmpeg. If extraction or merging fails, the tool automatically falls back to a video-only output and prints a warning — check the console log for details.
</details>

<details>
<summary><b>🖼️ Characters look garbled or missing</b></summary>

The default character ramp uses extended Latin-1 symbols (`°±¼½¾¡¿`). Make sure a monospace font supporting these glyphs is available (Consolas, Courier New, or DejaVu Sans Mono are auto-detected).
</details>

---

## 🤝 Contributing / Kontribusi

Contributions, issues, and feature requests are welcome!
Kontribusi, laporan bug, dan permintaan fitur sangat diterima!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
    GAK TAU MALES PENGEN JADI PNS
</p>