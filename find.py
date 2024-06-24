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

def capture_top_left_screen_region():
    scale_factor=0.3
    # Get the screen resolution
    screen_width, screen_height = get_screen_resolution()

    # Calculate the coordinates of the top right region
    region_width = int(screen_width * scale_factor)
    region_height = int(screen_height * scale_factor)
    region_left = 0  # Leftmost side
    region_top = 0  # Topmost side

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
            if character in title:
                win32gui.SetForegroundWindow(hwnd)
                return
        return
        
    except Exception as e:
        print(f"Error switching to the window character of '{character}': {e}")
        return

################################################ --------- Main ####################################################

def main(characters_set):
    print(f"Fight Turn detection for the characters {characters_set}")
    try:    
        while True:
            screen_image = capture_top_left_screen_region()
            extracted_text = process_image(screen_image)
            for character in characters_set:
                if character.lower() in extracted_text.lower():
                    switch_to_window(character)
                    break            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Looking for a set of characters and switch to their windows')
    parser.add_argument('characters_set', nargs='+', help='List of characters')
    args = parser.parse_args()

    main(args.characters_set)