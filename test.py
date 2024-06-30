import time
import argparse

from lib.odr import find_word_and_get_position
from lib.screen import capture_around_position, capture_screen, save_image


def main(words):
    print(f"Looking up for  {words}")
    try:    
        while True:
            img = capture_screen()
            position = find_word_and_get_position(img, words[0])
            if position:
                (x,y) = position
                print(x,y)
                capture = capture_around_position(x,y,100,100)
                save_image(filename="img_save.png",image=capture)
            else:
                print("None")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='for test')
    parser.add_argument('words', nargs='+', help='word to find')
    args = parser.parse_args()

    main(args.words)