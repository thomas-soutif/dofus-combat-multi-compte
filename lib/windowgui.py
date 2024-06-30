import win32gui
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


# Function to save the image to a file
def save_image(image, filename):
    win32gui.cv2_imwrite(filename, image)