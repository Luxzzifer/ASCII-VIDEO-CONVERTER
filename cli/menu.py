import os
from cli.prompts import get_user_choice, get_custom_int, get_output_folder
from config.constants import RESOLUTION_PRESETS, COLOR_PRESETS
def configure_conversion(input_video):
    print("\n" + "=" * 70)
    print("⚙️ CONVERSION CONFIGURATION")
    print("=" * 70)

    fps_choice = get_user_choice(
        "🎬 Choose FPS (Frame per Second):",
        {'1': '24 FPS (Cinematic)', '2': '30 FPS (Standard)', '3': '60 FPS (Smooth)', '4': 'Custom'},
        default='2'
    )
    target_fps = {'1': 24, '2': 30, '3': 60}.get(fps_choice) or get_custom_int("FPS custom", 10, 120, 30)

    cols_choice = get_user_choice(
        "\n🔤 Choose ASCII Width (number of character columns):",
        {
            '1': '80 columns (Fast, less detailed)',
            '2': '120 columns (Balanced)',
            '3': '160 columns (HD)',
            '4': '200 columns (Highly detailed, slow)',
            '5': 'Custom',
        },
        default='3'
    )
    cols = {'1': 80, '2': 120, '3': 160, '4': 200}.get(cols_choice) or get_custom_int("Jumlah kolom custom", 40, 300, 160)

    res_choice = get_user_choice("\n📺 Choose Output Video Resolution:", RESOLUTION_PRESETS, default='2')
    res = RESOLUTION_PRESETS[res_choice]
    if res['width'] is None:
        print("\n  Enter custom resolution:")
        output_width = get_custom_int("  Width (px)", 640, 7680, 1920)
        output_height = get_custom_int("  Height (px)", 360, 4320, 1080)
    else:
        output_width, output_height = res['width'], res['height']

    color_choice = get_user_choice("\n🎨 Choose  ASCII Color:", COLOR_PRESETS, default='1')
    color_rgb = COLOR_PRESETS[color_choice]['rgb']
    color_name = COLOR_PRESETS[color_choice]['name']

    audio_choice = get_user_choice(
        "\n🔊 Include audio from the original video?",
        {'1': 'Yes (merge audio)', '2': 'No (video only)'},
        default='1'
    )
    include_audio = (audio_choice == '1')

    print("\n💾 Output file location:")
    print("  [1] In the same folder as the input video")
    print("  [2] Custom location")
    loc_choice = input("Choice [1]: ").strip() or '1'

    if loc_choice == '2':
        default_folder = os.path.dirname(input_video)
        output_dir = get_output_folder(default_folder)
    else:
        output_dir = os.path.dirname(input_video)

    return {
        'target_fps': target_fps,
        'cols': cols,
        'output_width': output_width,
        'output_height': output_height,
        'color_rgb': color_rgb,
        'color_name': color_name,
        'include_audio': include_audio,
        'output_dir': output_dir,
    }