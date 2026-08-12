import numpy as np
from PIL import Image, ImageDraw
from core.fonts import get_font
from config.constants import CHAR_RAMP, BG_COLOR
def build_sprite_sheet(font, char_width, char_height, color_rgb):
    """Render every ramp character once into a small RGB array. Shared by both renderers."""
    n = len(CHAR_RAMP)
    sheet = np.zeros((n, char_height, char_width, 3), dtype=np.uint8)
    for i, char in enumerate(CHAR_RAMP):
        img = Image.new('RGB', (char_width, char_height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), char, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (char_width - text_width) // 2
        y = (char_height - text_height) // 2
        draw.text((x, y), char, fill=color_rgb, font=font)
        sheet[i] = np.array(img)
    return sheet


class ASCIIRenderer:
    """
    Fully vectorized ASCII renderer. Works on CPU (NumPy) or GPU (CuPy)
    depending on backend — no per-cell Python loops, so GPU actually helps.
    """

    def __init__(self, cols, rows, output_width, output_height, font_size, color_rgb, backend='cpu'):
        self.cols = cols
        self.rows = rows
        self.output_width = output_width
        self.output_height = output_height
        self.backend = backend

        self.char_width = output_width // cols
        self.char_height = output_height // rows

        font = get_font(font_size)
        sheet_cpu = build_sprite_sheet(font, self.char_width, self.char_height, color_rgb)

        if backend == 'cuda':
            import cupy as cp
            self.xp = cp
            self.sprite_sheet = cp.array(sheet_cpu)
        else:
            self.xp = np
            self.sprite_sheet = sheet_cpu

        art_w = cols * self.char_width
        art_h = rows * self.char_height
        self.offset_x = (output_width - art_w) // 2
        self.offset_y = (output_height - art_h) // 2

    def render_frame(self, gray_frame):
        """gray_frame: (rows, cols) uint8 numpy array -> (H, W, 3) uint8 array (numpy)."""
        xp = self.xp
        n_chars = len(CHAR_RAMP)

        gray = gray_frame if self.backend == 'cpu' else xp.array(gray_frame)
        idx = (gray.astype(xp.float32) / 256.0 * n_chars).astype(xp.int32)
        idx = xp.clip(idx, 0, n_chars - 1)  # (rows, cols)

        # Gather sprites for every cell in one shot: (rows, cols, ch, cw, 3)
        tiles = self.sprite_sheet[idx]

        # Rearrange into a single canvas-sized image without any Python loop
        tiles = xp.transpose(tiles, (0, 2, 1, 3, 4))  # (rows, ch, cols, cw, 3)
        art = tiles.reshape(self.rows * self.char_height, self.cols * self.char_width, 3)

        canvas = xp.zeros((self.output_height, self.output_width, 3), dtype=xp.uint8)
        canvas[self.offset_y:self.offset_y + art.shape[0],
               self.offset_x:self.offset_x + art.shape[1]] = art

        return canvas if self.backend == 'cpu' else xp.asnumpy(canvas)