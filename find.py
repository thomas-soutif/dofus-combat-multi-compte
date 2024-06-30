import time
import argparse

from lib.odr import find_word_and_get_position, process_image
from lib.screen import capture_around_position, capture_top_left_screen_region, save_image
from lib.windowgui import get_title_bar_height, is_dofus_window_focused, switch_to_window

def verify_save_position(screen_image,character):
    position = find_word_and_get_position(screen_image,character)
    if position:
        time.sleep(1)
        return position
    
    return None

def main(characters_set):
    SAVE_POSITION_X = None
    SAVE_POSITION_Y = None
    print(f"Fight Turn detection for the characters {characters_set}")
    height_bar = get_title_bar_height(characters_set)
    start_time = time.time() - 41
    try:    
        while True:
            if not is_dofus_window_focused(characters_set):
                time.sleep(2)
                print("not")
                continue
            print("in")
            if time.time() - start_time > 40:
                time.sleep(1) #Processor reduction, if the user is not fight, don't need to capture immediatly

            if SAVE_POSITION_X and SAVE_POSITION_Y:
                screen_image = capture_around_position(SAVE_POSITION_X,SAVE_POSITION_Y + height_bar,200,100)
            else:
                 screen_image = capture_top_left_screen_region(height_bar)
            extracted_text = process_image(screen_image)
            lines = extracted_text.lower().split('\n')
            if not any(line.strip().startswith("niveau") for line in lines):
                continue
            
            for character in characters_set:
                extracted_text = extracted_text.lower()
                if character.lower() in extracted_text:
                    switch_to_window(character)
                    if not SAVE_POSITION_X or not SAVE_POSITION_Y:
                        position = verify_save_position(screen_image,character)
                        if position:
                            SAVE_POSITION_X, SAVE_POSITION_Y = position
                    start_time = time.time()
                    break
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Looking for a set of characters and switch to their windows')
    parser.add_argument('characters_set', nargs='+', help='List of characters')
    args = parser.parse_args()

    main(args.characters_set)