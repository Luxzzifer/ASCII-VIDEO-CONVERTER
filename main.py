import sys
import time
import os

from config import gpu
from config.gpu import detect_gpu
from utils.ffmpeg import check_ffmpeg
from cli.prompts import get_video_path
from cli.menu import configure_conversion
from converter.pipeline import create_ascii_video

def main():
    print("=" * 70)
    print("🚀 ASCII VIDEO CONVERTER")
    print("   NVIDIA CUDA / CPU auto-detect, vectorized rendering")
    print("=" * 70)

    detect_gpu()

    if not check_ffmpeg():
        print("\n❌ FFmpeg not found!\n   Install using: winget install ffmpeg")
        input("\nPress Enter to exit...")
        sys.exit(1)

    if len(sys.argv) > 1:
        input_video = sys.argv[1].strip('"').strip("'")
        if not os.path.exists(input_video):
            print(f"\n❌ File from argument not found: {input_video}")
            input_video = get_video_path()
    else:
        input_video = get_video_path()

    config = configure_conversion(input_video)

    print("\n" + "=" * 70)
    print("📋 CONFIRMATION")
    print("=" * 70)
    print(f"   Input:    {input_video}")
    print(f"   FPS:      {config['target_fps']}")
    print(f"   Columns:  {config['cols']}")
    print(f"   Output:   {config['output_width']}x{config['output_height']}")
    print(f"   Color:    {config['color_name']}")
    print(f"   Audio:    {'Yes' if config['include_audio'] else 'No'}")
    print(f"   Folder:   {config['output_dir']}")
    print(f"   Backend:  {gpu.GPU_DEVICE}")

    if input("\nStart conversion? (y/n): ").strip().lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    start_time = time.time()
    try:
        create_ascii_video(input_video, config)
    except KeyboardInterrupt:
        print("\n\n⚠ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print(f"\n⏱️  Total time: {(time.time() - start_time) / 60:.1f} minutes")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()