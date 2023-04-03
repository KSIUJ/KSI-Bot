from __future__ import annotations
from typing import Tuple

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from PIL.Image import Image
from io import BytesIO


def get_text_size(text: str, image: Image, font: ImageFont.FreeTypeFont) -> Tuple[float, float]:
    im = PILImage.new("RGB", (image.width, image.height))
    draw = ImageDraw.Draw(im)
    _, _, text_width, text_height = draw.textbbox(text=text, font=font, xy=(0, 0))
    return (text_width, text_height)


def find_font_size(
    text: str, image: Image, font: ImageFont.FreeTypeFont, target_width_ratio: float
) -> int:
    observed_width, _ = get_text_size(text, image, font)
    estimated_font_size = font.size / (observed_width / image.width) * target_width_ratio

    return round(estimated_font_size)


class ResponseImageBuilder:
    def __init__(
        self,
        text: str,
        image: bytes,
        font_filepath: str = "fonts/Roboto/Roboto-Regular.ttf",
        stroke_width: int = 3,
        stroke_color: Tuple[int, int, int] = (0, 0, 0),
        text_color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self._text = text
        self._image = PILImage.open(BytesIO(image))
        self._font = ImageFont.truetype(font=font_filepath, encoding="unic", size=100)
        self._stroke_width = stroke_width
        self._text_color = text_color
        self._stroke_color = stroke_color

    def build(self) -> Image:
        draw = ImageDraw.Draw(self._image)
        adjusted_font_size = find_font_size(
            text=self._text, image=self._image, font=self._font, target_width_ratio=0.5
        )
        self._font.size = adjusted_font_size
        text_width, text_height = get_text_size(
            text=self._text, image=self._image, font=self._font
        )

        draw.text(
            text=self._text,
            xy=((self._image.width - text_width) / 2, (self._image.height - text_height) / 2),
            fill=self._text_color,
            stroke_fill=self._stroke_color,
            stroke_width=self._stroke_width,
            font=self._font,
        )
        return self._image
