import os
import pyautogui
import pygetwindow as gw

pyautogui.PAUSE = 0.5

rom_path = r"C:\Users\zitao\Downloads\1986 - Pokemon Emerald (U)(TrashMan) (patched).gba"
current_directory = os.getcwd()
back_folder_path = os.path.join(current_directory, "back")
back_shiny_folder_path = os.path.join(current_directory, "back_shiny")
front_folder_path = os.path.join(current_directory, "front")
front_shiny_folder_path = os.path.join(current_directory, "front_shiny")

open_file_button_coord = (61, 67)
next_button_coord = (446, 139)
next_pal_coord = (513, 138)
prev_pal_coord = (522, 164)
index_input_coord = (420, 242)
goto_button_coord = (515, 242)
save_button_coord = (453, 191)

def move_window_to_top_left():
    window_title = "unLZ-GBA"
    # Search for the window by its title
    window = gw.getWindowsWithTitle(window_title)[0]
    
    if window:
        window.moveTo(0, 0)
        window.activate()
        print(f"Moved window '{window_title}' to (0, 0).")
    else:
        print(f"Window with title '{window_title}' not found.")

def click(coord):
    # Move the mouse and click at the specified coordinates
    pyautogui.click(coord)
    print(f"Clicked at coordinates ({coord}).")

def double_click(coord):
    pyautogui.doubleClick(coord)
    print(f"Double clicked at coordinates ({coord}).")

def type_string(text):
    # Type the given string
    pyautogui.write(text)
    print(f"Typed the string: {text}")

def press_enter():
    # Press the Enter key
    pyautogui.press('enter')
    print("Pressed Enter key.")

def save_sprite(file_path):
    click(save_button_coord)
    type_string(file_path)
    press_enter()

def delete_sprites_with_id_greater_than(sprite_id, folder_paths):
    for folder in folder_paths:
        for filename in os.listdir(folder):
            # Ensure the file name has the right structure and ends with .png
            if filename.endswith(".png"):
                try:
                    # Extract the ID from the filename
                    file_id = int(filename.split(".")[0])
                    # Delete file if its ID is greater than the given sprite_id
                    if file_id >= sprite_id:
                        file_path = os.path.join(folder, filename)
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                except ValueError:
                    # Skip files that do not match the expected naming pattern
                    pass

if __name__ == "__main__":
    sprite_id = 1
    start_index = 1768
    end_index = 3379

    # customize
    sprite_id = 448
    start_index = 3355

    # # Create directories if they don't exist
    # for folder in [back_folder_path, back_shiny_folder_path, front_folder_path, front_shiny_folder_path]:
    #     if not os.path.exists(folder):
    #         os.makedirs(folder)


    # Delete all sprites with ID greater than sprite_id
    delete_sprites_with_id_greater_than(sprite_id, [
        front_folder_path, front_shiny_folder_path, back_folder_path, back_shiny_folder_path
    ])

    # # reset window
    # move_window_to_top_left()

    # # load rom file
    # click(open_file_button_coord)
    # type_string(rom_path)
    # press_enter()

    # go to index
    double_click(index_input_coord)
    type_string(str(start_index - 1))
    click(goto_button_coord)
    click(next_button_coord)

    # main loop
    while start_index < end_index:
        # save sprite named ./front/{sprite_index}.png
        save_sprite(front_folder_path + "\\" + str(sprite_id) + ".png")

        click(next_pal_coord)

        # save sprite named ./font_shiny/{sprite_index}.png
        save_sprite(front_shiny_folder_path + "\\" + str(sprite_id) + ".png")

        click(next_button_coord)
        start_index += 1


        # save sprite named ./back_shiny/{sprite_index}.png
        save_sprite(back_shiny_folder_path + "\\" + str(sprite_id) + ".png")

        click(prev_pal_coord)

        # save sprite named ./back/{sprite_index}.png
        save_sprite(back_folder_path + "\\" + str(sprite_id) + ".png")

        click(next_button_coord)
        click(next_button_coord)
        start_index += 1
        start_index += 1

        sprite_id += 1
