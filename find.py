import cv2
import pytesseract
import numpy as np
import mss
import time
import argparse
import win32gui

def get_screen_resolution():
    with mss.mss() as sct:
        # Get monitor 1, as mss uses 1-based indexing for monitors
        monitor = sct.monitors[1]
        return monitor["width"], monitor["height"]

# Function to capture the entire screen
def capture_screen():

    screen_width, screen_height = get_screen_resolution()
    
    region_width = int(screen_width)
    region_height = int(screen_height)
    region_left = 0  # Leftmost side
    region_top = 0  # Topmost side

    with mss.mss() as sct:
        region = {'left': region_left, 'top': region_top, 'width': region_width, 'height': region_height}
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        return img

# Function to capture a specific region of the screen
def capture_screen_region(left, top, width, height):
    with mss.mss() as sct:
        region = {'left': left, 'top': top, 'width': width, 'height': height}
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        return img

def capture_top_left_screen_region(height_bar):
    scale_factor=0.3
    # Get the screen resolution
    screen_width, screen_height = get_screen_resolution()

    # Calculate the coordinates of the top right region
    region_width = int(screen_width * scale_factor)
    region_height = int(screen_height * scale_factor)
    region_left = 0  # Leftmost side
    region_top = height_bar  # Topmost side (height size of the windows title)

    # Capture the region using mss
    with mss.mss() as sct:
        region = {'left': region_left, 'top': region_top, 'width': region_width, 'height': region_height}
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        return img

# Function to process the image and extract text
def process_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to preprocess the image
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # Perform OCR
    text = pytesseract.image_to_string(binary_img)
    return text

def get_title_bar_height(characters_set):
    # Get the handle of a dofus character
    windows = []
    hwnd_find = None
    
    win32gui.EnumWindows(get_window_titles, windows)
    for character in characters_set:
        if hwnd_find:
            break
        for hwnd, title in windows:
            if character in title and "Dofus" in title:
                hwnd_find = hwnd
                break
    
    if not hwnd_find:
        return 20 #default
    
    hwnd = hwnd_find
    window_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    title_bar_height = (window_rect[3] - window_rect[1]) - (client_rect[3] - client_rect[1])
    return title_bar_height

# Callback function to retrieve window titles
def get_window_titles(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        windows.append((hwnd, win32gui.GetWindowText(hwnd)))

# Function to save the image to a file
def save_image(image, filename):
    win32gui.cv2_imwrite(filename, image)


def switch_to_window(character):
    try:
        windows = []
        # Enumerate through all windows and retrieve their titles
        win32gui.EnumWindows(get_window_titles, windows)
        for hwnd, title in windows:
            if character in title and "Dofus" in title:
                win32gui.SetForegroundWindow(hwnd)
                return
        return
        
    except Exception as e:
        print(f"Error switching to the window character of '{character}': {e}")
        return


def is_dofus_window_focused():
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd).lower()
    return any(keyword in window_title for keyword in ["dofus", "ocre companion"])

################################################ --------- Main ####################################################

def main(characters_set):
    print(f"Fight Turn detection for the characters {characters_set}")
    height_bar = get_title_bar_height(characters_set)
    try:    
        while True:
            if not is_dofus_window_focused():
                time.sleep(1)
                continue
            screen_image = capture_top_left_screen_region(height_bar)
            extracted_text = process_image(screen_image)
            
            lines = extracted_text.lower().split('\n')
            if not any(line.strip().startswith("niveau") for line in lines):
                continue
            
            for character in characters_set:
                extracted_text = extracted_text.lower()
                if character.lower() in extracted_text:
                    switch_to_window(character)
                    break            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Looking for a set of characters and switch to their windows')
    parser.add_argument('characters_set', nargs='+', help='List of characters')
    args = parser.parse_args()

    main(args.characters_set)