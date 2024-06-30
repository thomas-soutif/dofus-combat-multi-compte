import numpy as np
import mss

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
