from game_platform import Platform

def criarsolo():
    y = 0
    h = 100
    return [
        Platform(0, y, 400, h),
        Platform(550, y, 300, h),
        Platform(1000, y, 400, h),
        Platform(1600, y, 600, h),
        Platform(2400, y, 300, h),
        Platform(3000, y, 500, h),
        Platform(3800, y, 400, h),
        Platform(4500, y, 600, h), #Solo final da vitória
    ]