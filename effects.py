import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--interval", type=int, default=1)
parser.add_argument("--file", type=str, default="/sys/devices/platform/tuxedo_keyboard/leds/rgb:kbd_backlight/multi_intensity")

args = parser.parse_args()

def update_color(color:list[int], colorfile:object, verbose:bool) -> None:
    if verbose:
        print(color)
    colorfile.write(' '.join(map(str, color)) + '\n')
    colorfile.seek(0)

def increase_color(color:list[int], index:int, interval:int, file:object, verbose:bool) -> None:
    for value in range(0,256,abs(interval)):
        color[index] = value
        update_color(color, file, verbose)

def decrease_color(color:list[int], index:int, interval:int, file:object, verbose:bool) -> None:
    for value in range(255,-1,-abs(interval)):
        color[index] = value
        update_color(color, file, verbose)

def rainbow_effect(interval:int, file:str, verbose:bool) -> None:
    color = [255, 0, 0]
    decreasing_color_index = 0
    colorfile = open(file, 'w')

    try:
        while 1:

            if decreasing_color_index + 1 >= len(color):
                increase_color(color, decreasing_color_index + 1 - len(color), interval, colorfile, verbose)
            else:
                increase_color(color, decreasing_color_index + 1, interval, colorfile, verbose)

            decrease_color(color, decreasing_color_index, interval, colorfile, verbose)

            decreasing_color_index += 1
            if decreasing_color_index >= len(color):
                decreasing_color_index -= len(color)

    except KeyboardInterrupt:
        colorfile.close()
        exit(1)

rainbow_effect(args.interval, args.file, args.verbose)