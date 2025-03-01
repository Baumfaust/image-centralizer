import sys

from PIL import Image, ImageDraw


def auto_crop_and_draw_border(image_path, background_color=(255, 255, 255), border_color=(255, 0, 0),
                              tolerance=10):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    def is_background_pixel(pixel, bg_color, tol):
        r, g, b = pixel
        br, bg, bb = bg_color
        return abs(r - br) <= tol and abs(g - bg) <= tol and abs(b - bb) <= tol

    top = 0
    for y in range(height):
        row_is_background = True
        for x in range(width):
            if not is_background_pixel(img.getpixel((x, y)), background_color, tolerance):
                row_is_background = False
                print(f"Found top non-background pixel at ({x}, {y}), color is: {img.getpixel((x, y))}")
                top_pos = (x+1, y)
                break
        if not row_is_background:
            top = y
            break

    bottom = height - 1
    for y in range(height - 1, -1, -1):
        row_is_background = True
        for x in range(width):
            if not is_background_pixel(img.getpixel((x, y)), background_color, tolerance):
                row_is_background = False
                print(f"Found bottom non-background pixel at ({x}, {y}), color is: {img.getpixel((x, y))}")
                bottom_pos = (x+1, y)
                break
        if not row_is_background:
            bottom = y
            break

    left = 0
    for x in range(width):
        col_is_background = True
        for y in range(height):
            if not is_background_pixel(img.getpixel((x, y)), background_color, tolerance):
                col_is_background = False
                print(f"Found left non-background pixel at ({x}, {y}), color is: {img.getpixel((x, y))}")
                left_pos = (x+1, y)
                break
        if not col_is_background:
            left = x
            break

    right = width - 1
    for x in range(width - 1, -1, -1):
        col_is_background = True
        for y in range(height):
            if not is_background_pixel(img.getpixel((x, y)), background_color, tolerance):
                col_is_background = False
                print(f"Found right non-background pixel at ({x}, {y}), color is: {img.getpixel((x, y))}")
                right_pos = (x+1, y)
                break
        if not col_is_background:
            right = x
            break

    lined_image = img.copy()
    cropped_img = img.crop((left, top, right + 1, bottom + 1))

    # Draw border (after cropping)
    cropped_width, cropped_height = cropped_img.size
    draw = ImageDraw.Draw(lined_image)
    def draw_border(draw, width, height, top, bottom, left, right, border_color):
            # Horizontal lines
            draw.line([(0, top), (width, top)], fill=border_color, width=1)  # Top
            draw.line([(0, bottom), (width, bottom)], fill=border_color, width=1)  # Bottom
            # Vertical lines
            draw.line([(left, 0), (left, height)], fill=border_color, width=1)  # Left
            draw.line([(right, 0), (right, height)], fill=border_color, width=1)  # Right


    draw_border(draw, width, height, top, bottom, left, right, border_color)
    draw.point(top_pos, fill=(0, 0, 0))
    draw.point(bottom_pos, fill=(0, 0, 0))
    draw.point(right_pos, fill=(0, 0, 0))
    draw.point(left_pos, fill=(0, 0, 0))
    lined_image.save("lined_image.png")
    return cropped_img


def main():
    if len(sys.argv) != 2:
        print("Usage: python crop_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        cropped_with_border = auto_crop_and_draw_border(image_path)
        output_path = "cropped_with_border.png"  # Or make this a command-line argument too
        cropped_with_border.save(output_path)
        print(f"Cropped image saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)
    except Exception as e:  # Catching a more general exception
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
