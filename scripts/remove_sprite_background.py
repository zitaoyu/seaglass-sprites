import os
import shutil
import argparse
from PIL import Image


def remove_background(image_path):
    """Removes the background color from a sprite image."""
    img = Image.open(image_path)
    img = img.convert("RGBA")

    data = img.getdata()

    # Note: background color is the top-left corner pixel
    bg_color = data[0][0:3]

    new_data = []
    for item in data:
        if item[0:3] == bg_color:  # Check if pixel matches the background color
            new_data.append((255, 255, 255, 0))  # Make it transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img


def process_images_in_directory(src_dir, dest_dir):
    """Clones directory structure, finds image files, and removes their background."""

    # Clone the directory structure
    if not os.path.exists(dest_dir):
        shutil.copytree(src_dir, dest_dir, ignore=shutil.ignore_patterns(
            "*.png", "*.jpg", "*.jpeg"))

    # Walk through the source directory
    for root, dirs, files in os.walk(src_dir):
        # Clone the subdirectory path
        relative_path = os.path.relpath(root, src_dir)
        dest_subdir = os.path.join(dest_dir, relative_path)

        # Ensure the destination subdirectory exists
        if not os.path.exists(dest_subdir):
            os.makedirs(dest_subdir)

        # Process each file
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_subdir, file)

                # Remove background from image
                modified_img = remove_background(src_file_path)

                # Save modified image in destination directory
                modified_img.save(dest_file_path)
                print(f"Saved {dest_file_path}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Remove background from images in a directory and save them to an output directory.")
    parser.add_argument('-p', '--path', required=True,
                        help="Path to the source directory containing images.")
    parser.add_argument(
        '-o', '--output', help="Path to the destination directory where processed images will be saved. Defaults to '*target_directory_name*_removed_bg' if not specified.")

    args = parser.parse_args()

    # If output directory is not specified, create one with the name "*target_directory_name*_removed_bg"
    if not args.output:
        target_directory_name = os.path.basename(os.path.normpath(args.path))
        parent_directory = os.path.dirname(os.path.normpath(args.path))
        output_dir = os.path.join(
            parent_directory, f"{target_directory_name}_removed_bg")
    else:
        output_dir = args.output

    # Process the images in the specified directories
    process_images_in_directory(args.path, output_dir)


if __name__ == '__main__':
    main()
