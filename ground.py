from game_platform import Platform

def criarsolo():
    y = 0
    h = 100

    return [
        Platform(0, y, 320, h),
        Platform(420, y, 280, h),
        Platform(820, y, 300, h),
        Platform(1240, y, 260, h),
        Platform(1620, y, 320, h),
    ]