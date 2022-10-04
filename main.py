import os
import cv2
import time
import re
from PIL import Image
import numpy as np
import numpy.typing as npt

MIN_GRAYSCALE = 0
MAX_GRAYSCALE = 255


@np.vectorize
def grayscale_to_ascii(grayscale: np.uint8, widen: int) -> str:
    """
    Transform grayscale value to ASCII character.
    """
    char: str = ...
    grayscale_levels: str = " .:-=+*#%@"

    if MAX_GRAYSCALE >= grayscale >= MIN_GRAYSCALE:
        index: int = int(grayscale // (MAX_GRAYSCALE / (len(grayscale_levels) - 1)))
        # char is multiplied by 3 to widen image
        char = grayscale_levels[index] * widen
    else:
        raise ValueError(
            f"ERROR: Invalid value for grayscale {grayscale}. Value should be an integer between {MIN_GRAYSCALE}-{MAX_GRAYSCALE}."
        )

    return char


def print_ascii_string(ascii_string: str) -> None:
    """
    Clear terminal and print ASCII string on it.
    """
    # os-way to clear terminal
    # see: https://stackoverflow.com/a/2084628
    os.system("cls" if os.name == "nt" else "clear")
    print(ascii_string)


def camera(fps: int = 30, height: int = 30, widen: int = 3) -> None:
    """
    Handle camera video capturing.
    """
    camera = cv2.VideoCapture(0)

    width = int(height * (4 / 3))

    while True:
        start: float = time.time()

        success: bool
        frame: npt.NDArray[np.uint8]
        success, frame = camera.read()

        if not success:
            break

        gray_image: Image = Image.fromarray(frame).convert("L").resize((width, height))
        gray_frame: npt.NDArray[np.string_] = grayscale_to_ascii(
            np.array(gray_image), widen
        )

        ascii_frame: str = gray_frame.tobytes().decode("utf32")

        # add newline every height * widen chars
        ascii_string: str = re.sub(
            "(.{%d})" % (width * widen), "\\1\n", ascii_frame, 0, re.DOTALL
        )

        print_ascii_string(ascii_string)

        diff: float = start - time.time()

        time.sleep(max(1 / fps - diff, 0))

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera()
