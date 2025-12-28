from PIL import Image
import os
import json

def gif_to_json_frames(gif_path, output_dir="frames", max_size=None):
    os.makedirs(output_dir, exist_ok=True)
    gif = Image.open(gif_path)

    frame_index = 0
    while True:
        frame = gif.convert("RGB")

        if max_size:
            frame.thumbnail(max_size)

        width, height = frame.size
        pixels = []

        for y in range(height):
            for x in range(width):
                r, g, b = frame.getpixel((x, y))
                pixels.append({
                    "x": x,
                    "y": y,
                    "c": {"r": r, "g": g, "b": b}
                })

        data = {
            "height": height,
            "width": width,
            "pixels": pixels
        }

        json_path = os.path.join(output_dir, f"frame_{frame_index}.json")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        print(f"Saved frame {frame_index} ({width}x{height})")

        frame_index += 1

        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break

    json_path = os.path.join(output_dir, f"config.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"x": width, "y": height, "frames": frame_index - 1}, f, ensure_ascii=False)
    print(f"Total frames: {frame_index}")

gif_to_json_frames("badaple.gif", "frames_json", max_size=(64, 36))