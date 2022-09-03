from PIL import Image, ImageDraw, ImageChops
import random
import colorsys


def random_color():
    h = random.random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb( h , s , v)
    rgb = [int(x*255) for x in float_rgb]

    return tuple(rgb)


def interpolate(start_color, end_color, factor: float):
    recip = 1 - factor
    return (int(start_color[0] * recip + end_color[0] * factor), int(start_color[1] * recip + end_color[1] * factor),
            int(start_color[2] * recip + end_color[2] * factor))


def generate_art(path: str):
    global p1, p2, i, Overlay_draw, Overlay_image
    print("Generating Art")
    target_size_px = 256
    scale_factor = 2

    image_size_box = target_size_px*scale_factor
    padding_px = 16 *scale_factor
    image_bg_color = (0, 0, 0)
    start_color = random_color()
    end_color = random_color()
    image = Image.new("RGB", size=(image_size_box, image_size_box), color=image_bg_color)
    # Draw lines
    draw = ImageDraw.Draw(image)
    points = []

    # generate points

    for _ in range(10):
        random_point = (random.randint(padding_px, image_size_box - padding_px),
                        random.randint(padding_px, image_size_box - padding_px))
        points.append(random_point)

    # Draw bounding box

    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    # center the image.

    delta_x = min_x - (image_size_box - max_x)
    delta_y = min_y - (image_size_box - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    # draw the point
    thickness = 0
    n_points = len(points) - 1
    for i, point in enumerate(points):

        # overlay canvas

        Overlay_image = Image.new("RGB", size=(image_size_box, image_size_box), color=image_bg_color)
        Overlay_draw = ImageDraw.Draw(Overlay_image)
        p1 = point

        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i + 1]
    line_xy = (p1, p2)
    colr_factor = i / n_points
    line_color = interpolate(start_color, end_color, colr_factor)
    thickness += 1*scale_factor
    Overlay_draw.line(line_xy, fill=line_color, width=thickness)
    image = ImageChops.add(image, Overlay_image)

    image = image.resize((target_size_px ,target_size_px),resample=Image.ANTIALIAS)
    image.save(path)

    if __name__ == "__main__":

        for i in range(10):
            generate_art(f"test_image_{i}.png")
