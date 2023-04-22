import os

from PIL import Image, ImageDraw, ImageFont


square_width = 70
font = ImageFont.truetype("fonts/Montserrat-LightItalic.ttf", 10)


# [["x", ".", "o"], [".", "x", "."], ["o", ".", "o"]]
def create_field(path_to_file, extension, matrix):
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return

    width, height = square_width * len(matrix[0]), square_width * len(matrix)
    img = Image.new("RGB", (width, height), (255, 204, 229))
    drawer = ImageDraw.Draw(img)

    for x in range(square_width, width, square_width):
        drawer.line((x, 0, x, height), fill=(51, 0, 25), width=1)

    for y in range(square_width, height, square_width):
        drawer.line((0, y, width, y), fill=(51, 0, 25), width=1)

    i = 1
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            col_space, row_space = col * square_width, row * square_width

            drawer.text((col_space + 0.03 * square_width,
                         row_space + 0.005 * square_width),
                        f"{i}", (0, 0, 0),
                        font=font)
            i += 1
            if matrix[row][col] == ".":
                continue
            if matrix[row][col] == "x":
                drawer.line((col_space + 0.2 * square_width, row_space + 0.2 * square_width,
                             col_space + 0.8 * square_width, row_space + 0.8 * square_width),
                            fill=(51, 0, 25), width=1)

                drawer.line((col_space + 0.2 * square_width, row_space + 0.8 * square_width,
                             col_space + 0.8 * square_width, row_space + 0.2 * square_width),
                            fill=(51, 0, 25), width=1)
            else:
                drawer.ellipse((col_space + 0.15 * square_width, row_space + 0.15 * square_width,
                                col_space + 0.85 * square_width, row_space + 0.85 * square_width),
                               outline=(51, 0, 25), width=1)

    img.save(path_to_file, extension)
    return img


def delete_file(path_to_file):
    os.remove(path_to_file)
