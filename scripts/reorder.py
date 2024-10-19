import os
import shutil
import json


def rename_and_copy_files(folder_path):
    # Create the 'new' folder inside the target directory
    new_folder_path = os.path.join(folder_path, 'new')
    os.makedirs(new_folder_path, exist_ok=True)

    # Get all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))]

    # Sort files by last modified time first, then by filename alphabetically
    files.sort(key=lambda f: (os.path.getmtime(
        os.path.join(folder_path, f)), f))

    # Create a list to store the old-to-new name mapping
    file_mapping = []

    # Copy and rename each file
    for i, filename in enumerate(files, start=1):
        # Build the new file name
        new_name = f"{i}.png"

        # Define full paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(new_folder_path, new_name)

        # Copy and rename the file
        shutil.copy2(old_file, new_file)

        # Append the old and new file names to the mapping
        file_mapping.append({"old_name": filename, "new_name": new_name})

    # Save the mapping to a JSON file inside the 'new' folder
    mapping_file_path = os.path.join(new_folder_path, "file_mapping.json")
    with open(mapping_file_path, "w") as json_file:
        json.dump(file_mapping, json_file, indent=4)

    print(
        f"Renaming complete. Files copied to {new_folder_path}. Mapping saved to file_mapping.json.")


def reorder_files(target_directory):
    # Get all .png files in the target directory
    files = [f for f in os.listdir(target_directory) if f.endswith(
        '.png') and os.path.isfile(os.path.join(target_directory, f))]

    # Extract numeric part of the filenames and sort by that number
    files_with_index = []
    for filename in files:
        try:
            # Extract the numeric part before '.png'
            index = int(filename.split('.')[0])
            files_with_index.append((index, filename))
        except ValueError:
            # Skip files that do not have a valid integer index
            continue

    # Sort the files by their numeric index
    files_with_index.sort()

    # Reorder files to remove gaps in the numbering
    for new_index, (_, filename) in enumerate(files_with_index, start=1):
        old_file = os.path.join(target_directory, filename)
        new_filename = f"{new_index}.png"
        new_file = os.path.join(target_directory, new_filename)

        # Rename the file only if the name has changed
        if filename != new_filename:
            shutil.move(old_file, new_file)
            print(f"Renamed: {filename} -> {new_filename}")
        else:
            print(f"File {filename} stays the same")


# Example usage
folder_path = '/Users/tommyyu/Desktop/projects/seaglass-sprites/sprites/front_shiny'
reorder_files(folder_path)
