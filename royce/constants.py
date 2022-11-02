class Constants:
    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 800
    HEAD_BLUE: tuple[int, int, int] = (0, 128, 255)
    BODY_BLUE: tuple[int, int, int] = (51, 153, 255)
    APPLE_RED: tuple[int, int, int] = (255, 153, 153)
    BORDER_GREEN: tuple[int, int, int] = (0, 153, 0)
    DARK_GREEN: tuple[int, int, int] = (128, 255, 0)
    LIGHT_GREEN: tuple[int, int, int] = (153, 255, 51)
    PORTAL_ORANGE: tuple[int, int] = (255, 165, 0)
    PORTAL_BLUE: tuple[int, int] = (0, 0, 255)
    DEATH_COLORS_HEAD: list[tuple[int, int, int]] = [(0, 153, 0), (76, 148, 0), (114, 141, 0), (146, 131, 0), 
                                                     (177, 117, 0), (206, 98, 0), (232, 70, 0), (255, 0, 0)]
    DEATH_COLORS_BODY: list[tuple[int, int, int]] = [(0, 204, 0), (101, 190, 0), (142, 174, 0), (174, 156, 0),
                                                     (202, 134, 0), (225, 108, 0), (243, 74, 0), (255, 0, 0)]
    DEATH_RED: tuple[int, int, int] = (255, 0, 0)