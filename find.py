import time
import argparse

from lib.odr import process_image
from lib.screen import capture_top_left_screen_region
from lib.windowgui import get_title_bar_height, is_dofus_window_focused, switch_to_window

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