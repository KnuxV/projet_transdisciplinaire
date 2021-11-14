import pyautogui as pgui
import time

# pgui.PAUSE = 2.5
pgui.FAILSAFE = True

# positional variables // TO BE CHANGED IF REUSED, using mouse_pos.py
export_position = 1250, 540
tab_delimited_file_position = 1304, 785
records_from_button_position = 1092, 724
records_from_button_position_first_box = 1207, 724
records_from_button_position_second_box = 1290, 724
record_content = 1373, 850
full_record = 1251, 918
export = 1077, 914
above_save_button = 935, 915
ok = 935, 950
text_box = 1470, 252
save_button = 1859, 264

# To be changed if we don't start downloading from 1
record_from = 1
record_to = 1000
# text_file_name
root_file_name = 1
end_file_name = ".txt"

if __name__ == "__main__":
    while record_from <= 52915:  # To be updated every chunk
        # 1st step : click export + tab delimited file
        time.sleep(1)
        pgui.click(export_position, interval=0.5)
        # time.sleep(2)
        pgui.click(tab_delimited_file_position, interval=0.5, button='left')
        # time.sleep(2)
        pgui.click(records_from_button_position)
        time.sleep(0.1)
        # First box
        pgui.click(records_from_button_position_first_box)
        # First, we need to empty the box from text
        for i in range(10):
            pgui.press("backspace", interval=0.1)
            # time.sleep(0.1)
        # Then, we write the number
        pgui.keyDown('shift')
        pgui.write(str(record_from))
        pgui.keyUp('shift')

        # Second box
        pgui.click(records_from_button_position_second_box)
        for i in range(10):
            pgui.press("backspace", interval=0.1)
            # time.sleep(0.1)
        pgui.keyDown('shift')
        pgui.write(str(record_to))
        pgui.keyUp('shift')

        time.sleep(1)
        pgui.click(record_content)
        time.sleep(1)
        pgui.click(full_record)
        time.sleep(1)
        pgui.click(export)
        time.sleep(15)

        # need to click above the save button and wait a bit
        pgui.click(above_save_button)
        time.sleep(1)
        pgui.click(ok)

        # click on the text box, erase, and write new file name
        pgui.click(text_box)
        pgui.hotkey('ctrl', 'a')
        pgui.press('backspace')
        pgui.keyDown('shift')
        pgui.write(str(root_file_name))
        pgui.write(end_file_name)
        pgui.keyUp('shift')
        pgui.click(save_button)

        # Update variable
        record_from += 1000
        record_to += 1000
        # Update this to handle the last thousand elements
        if record_to > 52915:
            record_to = 52915
        root_file_name += 1
