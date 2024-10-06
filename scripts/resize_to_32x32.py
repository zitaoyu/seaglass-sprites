import os
import shutil
import argparse
from PIL import Image


def resize_image(image_path):
    """Crops the image to 64x64 starting from the top-left corner if it is larger than 64x64."""
    img = Image.open(image_path)

    # Check if the image size is larger than 64x64
    if img.width > 64 or img.height > 64:
        # Crop the image to 64x64 starting from the top-left corner
        img = img.crop((0, 0, 64, 64))
        print(f"Cropped {image_path} to {img.size}")
    else:
        print(f"Image {image_path} is already within 64x64 size.")

    return img


def process_images_in_directory(src_dir, dest_dir):
    """Clones directory structure, finds image files, and resizes them to 64x64 if larger."""

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

                # Resize the image if larger than 64x64
                resized_img = resize_image(src_file_path)

                # Save resized image in destination directory
                resized_img.save(dest_file_path)
                print(f"Saved {dest_file_path}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Resize images in a directory to 64x64 if they are larger, and save them to an output directory.")
    parser.add_argument('-p', '--path', required=True,
                        help="Path to the source directory containing images.")
    parser.add_argument(
        '-o', '--output', help="Path to the destination directory where processed images will be saved. Defaults to '*target_directory_name*_resized' if not specified.")

    args = parser.parse_args()

    # If output directory is not specified, create one with the name "*target_directory_name*_resized"
    if not args.output:
        target_directory_name = os.path.basename(os.path.normpath(args.path))
        parent_directory = os.path.dirname(os.path.normpath(args.path))
        output_dir = os.path.join(
            parent_directory, f"{target_directory_name}_resized")
    else:
        output_dir = args.output

    # Process the images in the specified directories
    process_images_in_directory(args.path, output_dir)


if __name__ == '__main__':
    main()
