import os
import shutil
import subprocess

def check_ffmpeg():
    return shutil.which('ffmpeg') is not None


def extract_audio(video_path, audio_path):
    if not check_ffmpeg():
        print("  ⚠ FFmpeg not found")
        return False
    try:
        print(f"  → Extracting audio from: {os.path.basename(video_path)}")
        cmd = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame',
               '-ab', '192k', '-ar', '44100', '-y', audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"  ⚠ FFmpeg extract error:\n     {result.stderr[:300]}")
            return False
        if os.path.exists(audio_path):
            print(f"  ✓ Audio extracted: {os.path.getsize(audio_path) / (1024*1024):.2f} MB")
            return True
        return False
    except Exception as e:
        print(f"  ⚠ Failed to extract audio: {e}")
        return False


def _run_merge(cmd, temp_output, timeout, label):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode == 0 and os.path.exists(temp_output):
        print(f"  ✓ Merge successful ({label}): {os.path.getsize(temp_output) / (1024*1024):.2f} MB")
        return True
    return False


def merge_audio_video(video_path, audio_path, output_path):
    if not check_ffmpeg():
        shutil.copy2(video_path, output_path)
        return os.path.exists(output_path)

    temp_output = output_path + ".merged.mp4"
    try:
        print("  → Merging video + audio...")
        cmd1 = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac',
                '-b:a', '192k', '-map', '0:v:0', '-map', '1:a:0', '-shortest',
                '-movflags', '+faststart', '-y', temp_output]
        ok = _run_merge(cmd1, temp_output, 300, "method 1")

        if not ok:
            print("  ⚠ Method 1 failed, trying method 2 (re-encode)...")
            cmd2 = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'libx264',
                    '-preset', 'ultrafast', '-crf', '23', '-c:a', 'aac', '-b:a', '192k',
                    '-map', '0:v:0', '-map', '1:a:0', '-shortest', '-movflags', '+faststart',
                    '-y', temp_output]
            ok = _run_merge(cmd2, temp_output, 600, "method 2")

        if not ok:
            print("  ⚠ Both methods failed")
            return False

        if os.path.exists(output_path):
            os.remove(output_path)
        try:
            os.rename(temp_output, output_path)
        except OSError:
            shutil.copy2(temp_output, output_path)
            os.remove(temp_output)
        return True
    except Exception as e:
        print(f"  ⚠ Merge failed: {e}")
        return False


def _finalize_video(temp_video, output_video):
    if not os.path.exists(temp_video):
        return
    try:
        os.rename(temp_video, output_video)
    except OSError:
        shutil.copy2(temp_video, output_video)
        os.remove(temp_video)