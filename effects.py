import argparse
import threading
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--interval", type=int, default=1)
parser.add_argument("--file", type=str, default="/sys/devices/platform/tuxedo_keyboard/leds/rgb:kbd_backlight/multi_intensity")
parser.add_argument("--delay", type=float, default=0.05)
args = parser.parse_args()

class AsyncColorWriter:
    def __init__(self, filepath : str,  verbose: bool):
        self.filepath = filepath
        self.verbose = verbose
        self.currentcolor = None
        self.lock = threading.Lock()
        self.running= True

        try:
            self.colorfile = open(self.filepath, 'w')
        except Exception as e:
            print(f"Error opening File {self.filepath}:{e}", file= sys.stderr)
            sys.exit(1)
        
        self.thread = threading.Thread(target=self._write_loop, daemon=True)
        self.thread.start()

    def set_color(self, color: list[int]):
        with self.lock:
            self.currentcolor = list(color)
    
    def _write_loop(self):
        last_written = None
        while self.running:
            color_to_write = None
            with self.lock:
                if self.currentcolor != last_written:
                    color_to_write = self.currentcolor

            if color_to_write:
                try:
                    color_str = ' '.join(map(str, color_to_write)) + '\n'
                    if self.verbose:
                        print(f"Writing physically: {color_str.strip()}")
                    
                    self.colorfile.write(color_str)
                    self.colorfile.flush()
                    self.colorfile.seek(0)
                    last_written = color_to_write
                except Exception as  e:
                    if self.verbose:
                        print(f"Write Error: {e}", file = sys.stderr)
            
            time.sleep(0.005)
    
    def close(self):
        self.running = False
        try:
            self.thread.join(timeout=1.0)
        except Exception:
            pass
        self.colorfile.close()


def update_color(color: list[int], writer: AsyncColorWriter, verbose: bool, delay: float) -> None:
    if verbose:
        print(f"Generated color: {color}")
    writer.set_color(color)
    
    if delay > 0:
        time.sleep(delay)

def increase_color(color: list[int], index: int, interval: int, writer: AsyncColorWriter, verbose: bool, delay: float) -> None:
    for value in range(0, 256, abs(interval)):
        color[index] = value
        update_color(color, writer, verbose, delay)

def decrease_color(color: list[int], index: int, interval: int, writer: AsyncColorWriter, verbose: bool, delay: float) -> None:
    for value in range(255, -1, -abs(interval)):
        color[index] = value
        update_color(color, writer, verbose, delay)

def rainbow_effect(interval: int, file: str, verbose: bool, delay: float) -> None:
    color = [255, 0, 0]
    decreasing_color_index = 0
    
    writer = AsyncColorWriter(file, verbose)

    try:
        while True:
            if decreasing_color_index + 1 >= len(color):
                increase_color(color, decreasing_color_index + 1 - len(color), interval, writer, verbose, delay)
            else:
                increase_color(color, decreasing_color_index + 1, interval, writer, verbose, delay)

            decrease_color(color, decreasing_color_index, interval, writer, verbose, delay)

            decreasing_color_index += 1
            if decreasing_color_index >= len(color):
                decreasing_color_index -= len(color)

    except KeyboardInterrupt:
        writer.close()
        sys.exit(0)

if __name__ == "__main__":
    rainbow_effect(args.interval, args.file, args.verbose, args.delay)
