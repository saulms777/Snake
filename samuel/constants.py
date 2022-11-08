from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Constants:
    TICKS: int = 10

    # key directions
    KEY_DIRECTIONS: dict[int, tuple[int, int]] = {
        K_w: (0, -25),
        K_s: (0, 25),
        K_a: (-25, 0),
        K_d: (25, 0),
        K_UP: (0, -25),
        K_DOWN: (0, 25),
        K_LEFT: (-25, 0),
        K_RIGHT: (25, 0)
    }

    # colours
    HEAD_BLUE: tuple[int, int, int] = (0, 128, 255)
    BODY_BLUE: tuple[int, int, int] = (51, 153, 255)
    DARK_GREEN: tuple[int, int, int] = (128, 255, 0)
    LIGHT_GREEN: tuple[int, int, int] = (153, 255, 51)
    BLACK: tuple[int, int, int] = (0, 0, 0)
