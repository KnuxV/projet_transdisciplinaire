import pyautogui as pgui


def print_position():
    """
    print mouse position,
    :return: nothing
    """
    try:
        while True:
            x, y = pgui.position()

            print(x, y)
            pgui.PAUSE = 2.5
    except KeyboardInterrupt:
        print('\n')


if __name__ == "__main__":
    print_position()
