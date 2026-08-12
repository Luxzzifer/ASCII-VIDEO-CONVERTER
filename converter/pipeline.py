import os
import cv2
import numpy as np
import subprocess
import time
from tqdm import tqdm

import config.gpu as gpu
from utils.ffmpeg import check_ffmpeg, extract_audio, merge_audio_video, _finalize_video
from core.renderer import ASCIIRenderer

def create_ascii_video(input_video, config):
    input_video = os.path.abspath(input_video)
    output_dir = config['output_dir']
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_video))[0]
    color_short = config['color_name'].split()[0].lower()
    output_video = os.path.join(output_dir, f"{base_name}_ASCII_{color_short}_{config['cols']}col.mp4")

    print(f"\n📂 Output directory: {output_dir}")
    print(f"📹 Input: {input_video}")
    print(f"💾 Output: {output_video}")

    if not check_ffmpeg():
        print("❌ FFmpeg not found! Please install it first:\n   winget install ffmpeg")
        return

    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"❌ Failed to open video: {input_video}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    if fps <= 0:
        print("  ⚠ Video did not report a valid FPS, assuming 30 FPS")
        fps = 30.0

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    target_fps = config['target_fps']
    cols = config['cols']
    output_width = config['output_width']
    output_height = config['output_height']
    color_rgb = config['color_rgb']

    rows = max(1, int(cols * (output_height / output_width) * 2))
    char_width = output_width // cols
    char_height = output_height // rows
    font_size = max(4, min(char_width, char_height) - 2)

    print("\n📊 Video Info:")
    print(f"   • Resolution: {orig_width}x{orig_height}")
    print(f"   • FPS: {fps:.2f} → {target_fps}")
    print(f"   • Duration: {total_frames / fps:.2f}s")
    print("\n🎨 ASCII Config:")
    print(f"   • Grid: {cols}x{rows}")
    print(f"   • Output: {output_width}x{output_height}")
    print(f"   • Color: {config['color_name']} {color_rgb}")
    print(f"   • Font: {font_size}px")
    print(f"   • Backend: {gpu.GPU_DEVICE}")

    try:
        renderer = ASCIIRenderer(cols, rows, output_width, output_height, font_size, color_rgb,
                                 backend=gpu.GPU_BACKEND if gpu.GPU_BACKEND == 'cuda' else 'cpu')
    except Exception as e:
        print(f"  ⚠ {gpu.GPU_BACKEND} renderer failed ({e}), falling back to CPU")
        renderer = ASCIIRenderer(cols, rows, output_width, output_height, font_size, color_rgb, backend='cpu')

    temp_video = output_video + ".temp.mp4"
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f'{output_width}x{output_height}', '-pix_fmt', 'rgb24',
        '-r', str(target_fps), '-i', '-',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-pix_fmt', 'yuv420p', temp_video,
    ]

    print("\n🎬 Rendering...")
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    frame_skip = max(1, int(round(fps / target_fps)))
    expected_frames = max(1, total_frames // frame_skip)

    frame_count = 0
    processed_frames = 0
    pbar = tqdm(total=expected_frames, desc="Progress", ncols=100)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_skip != 0:
                frame_count += 1
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_resized = cv2.resize(gray, (cols, rows))
            frame_rgb = renderer.render_frame(gray_resized)

            ffmpeg_process.stdin.write(np.ascontiguousarray(frame_rgb).tobytes())
            processed_frames += 1
            pbar.update(1)
            frame_count += 1
    except Exception as e:
        print(f"\n❌ Error during rendering: {e}")
    finally:
        pbar.close()
        cap.release()
        ffmpeg_process.stdin.close()
        _, stderr = ffmpeg_process.communicate()
        if ffmpeg_process.returncode != 0:
            print(f"\n❌ FFmpeg error (code {ffmpeg_process.returncode}):")
            print(stderr.decode('utf-8', errors='ignore')[:500])

    print(f"\n✓ Rendered {processed_frames} frames")

    if not os.path.exists(temp_video):
        print("\n❌ ERROR: Temporary file was not created!")
        return
    print(f"   Temporary video: {os.path.getsize(temp_video) / (1024*1024):.2f} MB")

    audio_file = os.path.join(output_dir, "temp_audio_extract.mp3")
    try:
        if config['include_audio']:
            print("\n🔊 Processing audio...")
            if extract_audio(input_video, audio_file) and merge_audio_video(temp_video, audio_file, output_video):
                print("\n  ✓✓✓ FINAL VIDEO CREATED WITH AUDIO! ✓✓✓")
                time.sleep(0.5)
                if os.path.exists(temp_video):
                    try:
                        os.remove(temp_video)
                    except OSError:
                        pass
            else:
                print("\n  ⚠ Audio failed, saving video WITHOUT audio")
                _finalize_video(temp_video, output_video)
        else:
            _finalize_video(temp_video, output_video)
    finally:
        if os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except OSError:
                pass

    if os.path.exists(output_video):
        print("\n" + "=" * 70)
        print("🎉 SUCCESS!")
        print(f"📁 File saved at:\n   {output_video}")
        print(f"📦 Size: {os.path.getsize(output_video) / (1024*1024):.2f} MB")
        print(f"🎨 Color: {config['color_name']}")
        print(f"🔤 Grid: {cols}x{rows} characters")
        print(f"📺 Resolution: {output_width}x{output_height}")
        print(f"{'🔊 Audio: INCLUDED' if config['include_audio'] else '🔇 Audio: NOT INCLUDED'}")
        print("=" * 70)
    else:
        print("\n❌ ERROR: Output file was not created!")