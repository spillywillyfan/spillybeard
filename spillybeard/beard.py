import glob
import math
import os
import face_recognition  # lol, of course python can do this

from PIL import Image
from spillybeard.styles import STYLES as styles


def output_path(output_directory, source_path):
    filename = os.path.splitext(os.path.basename(source_path))[0]
    expanded_directory = os.path.expanduser(output_directory)
    output_path = os.path.join(expanded_directory, f"{filename}_bearded.png")
    return output_path


def get_beard(stylename, beard_index=0):
    style = styles.get(stylename)
    here = os.path.dirname(__file__)
    beard_repository = os.path.join(here, "beards", style["beard_dir"])
    all_beards = sorted(glob.glob(os.path.join(beard_repository, "*.png")))
    this_friendos_unique_beard = all_beards[beard_index % len(all_beards)]
    beard = Image.open(this_friendos_unique_beard)
    return beard, style


def centroid(points):
    x, y = zip(*points)
    length = len(x)
    return int(sum(x) / length), int(sum(y) / length)


def distance(point1, point2):
    return math.hypot(point1[0] - point2[0], point1[1] - point2[1])


def angle(left, right):
    radians = math.atan2(right[1] - left[1], right[0] - left[0])
    return -1 * math.degrees(radians)


def embearden(filepath, style="real"):
    """Turn a pic of frens into SpillyWilly fans.

    Args:
        filepath: Path to friendos

    Returns:
        (PIL Image): A picture of frens with beards
    """
    if isinstance(filepath, str):
        filepath = os.path.expanduser(filepath)

    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(filepath)

    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)

    # If you find more than 50 faces, assume something has gone wrong
    if not face_landmarks_list or len(face_landmarks_list) > 50:
        return None

    pil_image = Image.fromarray(image)
    for index, face_landmarks in enumerate(face_landmarks_list):
        # Grab a personal beard
        beard, beard_style = get_beard(style, index)

        # Use the chin width to determine the beard size
        chin_left = face_landmarks["chin"][1]
        chin_right = face_landmarks["chin"][-2]
        beard_width = int(distance(chin_left, chin_right) * 1.1)
        beard_height = int((beard_width / float(beard.width)) * beard.height)
        beard = beard.resize((beard_width, beard_height))
        beard = beard.rotate(angle(chin_left, chin_right))

        # Center it around their pucker/chin
        center_points_list = [
            face_landmarks[feature] for feature in beard_style["center"]
        ]
        # Simple replacement for itertools.chain
        center_points = [
            item for sublist in center_points_list for item in sublist]
        center = centroid(center_points)
        attach_point = (
            int(center[0] - beard.width / 2),
            center[1] - int(beard_style["offset"] * beard.height),
        )
        # Add it to the image
        pil_image.paste(beard, attach_point, beard)
    return pil_image


def make_before_and_after(filepath, style, vertical=True):
    before = Image.open(filepath)
    after = embearden(filepath, style)
    if vertical:
        result = Image.new("RGB", (before.width, before.height + after.height))
        result.paste(before, (0, 0))
        result.paste(after, (0, before.height))
    else:
        result = Image.new("RGB", (before.width + after.width, before.height))
        result.paste(before, (0, 0))
        result.paste(after, (before.width, 0))
    return result
