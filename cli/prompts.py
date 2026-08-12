import os
import sys

def get_video_path():
    print("\n" + "=" * 70)
    print("📹 INPUT VIDEO")
    print("=" * 70)
    print("Enter the video file path (you can drag and drop the file into this window):")
    print("  Example: C:\\Videos\\movie.mp4")
    print()

    while True:
        try:
            path = input("📁 Video path: ").strip().strip('"').strip("'")
            if not path:
                print("  ⚠ ⚠ Path cannot be empty")
                continue
            if not os.path.exists(path):
                print(f"  ❌ File not found: {path}")
                if input("  Try again? (y/n): ").strip().lower() != 'y':
                    sys.exit(0)
                continue

            valid_ext = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            if os.path.splitext(path)[1].lower() not in valid_ext:
                print("  ⚠ Extension might not be a video file, but we'll try to process it...")

            return os.path.abspath(path)
        except KeyboardInterrupt:
            print("\n\Cancelled.")
            sys.exit(0)


def get_user_choice(prompt, options, default=None):
    print(f"\n{prompt}")
    for key, value in options.items():
        label = value.get('name', value) if isinstance(value, dict) else value
        print(f"  [{key}] {label}")
    if default:
        print(f"  Default: [{default}]")

    while True:
        try:
            choice = input("\nChoice: ").strip()
            if not choice and default:
                return default
            if choice in options:
                return choice
            print("  ⚠ ⚠ Invalid choice, please try again")
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            sys.exit(0)


def get_custom_int(prompt, min_val, max_val, default):
    while True:
        try:
            value = input(f"{prompt} [{min_val}-{max_val}, default={default}]: ").strip()
            if not value:
                return default
            value = int(value)
            if min_val <= value <= max_val:
                return value
            print(f" ⚠ Must be between {min_val} and {max_val}")
        except ValueError:
            print("  ⚠ Must be a number")
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            sys.exit(0)


def get_output_folder(default_folder):
    while True:
        path = input("  Output folder path: ").strip().strip('"').strip("'")
        if not path:
            print(f"  ⚠ ⚠ Empty, using default: {default_folder}")
            return default_folder
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            create = input(f"  Folder not found, create '{path}'? (y/n): ").strip().lower()
            if create == 'y':
                os.makedirs(path, exist_ok=True)
                return path
            continue
        return path