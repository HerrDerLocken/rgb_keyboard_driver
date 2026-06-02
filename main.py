from json import loads

with open("config.json", "r") as f:
    config = loads(f.read())

color = [255, 0, 0]

def update_color(color:list[int]) -> None:
    print(color)
    with open(config["filepath"], "w") as f:
        f.write(' '.join(map(str, color)))

def increase_color(color:list[int], index:int) -> None:
    for value in range(256):
        color[index] = value
        update_color(color)

def decrease_color(color:list[int], index:int) -> None:
    for value in range(255,-1,-1):
        color[index] = value
        update_color(color)

while 1:
    decreasing_color_index = 0

    if decreasing_color_index + 1 >= len(color):
        increase_color(color, decreasing_color_index + 1 - len(color))
    else:
        increase_color(color, decreasing_color_index + 1)

    decrease_color(color, decreasing_color_index)

    decreasing_color_index += 1
    if decreasing_color_index >= len(color):
        decreasing_color_index -= len(color)