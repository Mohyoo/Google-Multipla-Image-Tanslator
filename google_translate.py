# Language choices

import os
import sys
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep


# Prepare the functions.
def show_instructions():
    """Display instructions & commands."""
    message = ("*) First thing first:\n"
               "   -Put your images in a folder, then copy the folder's path.\n"
               "   -Go to 'languages_list.txt' and find your language's shortcut.\n\n"
               "*) Required arguments:\n"
               "   -i        Path to the images folder.\n"
               "   -l        Languages, e.g: '-l en_ar', this means from english to arabic;\n"
               "             don't forget the underscore.\n\n"
               "*) Optional arguments:\n"
               "   -o        Path of the output text file, default is: current directory.\n"
               "   -c        Waiting time for an image to be translated before trying to copy its\n"
               "             text (in seconds), default is 5.\n"
               "   -q        After finishing, time to wait before closing the browser (in seconds),\n"
               "             default is 60.\n"
               "   -k        Keep the same connection for every server request (it may speed up the\n"
               "             process), default is false.\n\n"
               "*) Tips:\n"
               "   -Compress your files before uploading, thus you can use less waiting time argument (-c);\n"
               "    you can use 'Curtail' for Linux, or 'MassCompressor' for Windows.\n"
               "   -Use waiting time (-c) according to image size & internet speed, if it's too low\n"
               "    you may get an error.\n"
               "   -Not all languages are supported for image translating.")

    print(message)


def get_arguments():
    """Organize the command line arguments."""
    global images_path, lang_1, lang_2, output_path, time_to_copy, time_to_quit, keep_alive
    for index, arg in enumerate(sys.argv):
        if (arg == '-h') or (arg == 'help') or (arg == '--help'):
            show_instructions()
            quit()

        # Required arguments.
        elif arg == '-i':
            images_path = sys.argv[index + 1]
            if not os.path.exists(images_path):
                print("Path doesn't exist, try absolute path instead!")
                quit()

        elif arg == '-l':
            try:
                lang_1, lang_2 = sys.argv[index + 1].split('_')
            except:
                print('Enter two languages shortcuts separated with an underscore (_)!')
                quit()

        # Optional arguments.
        elif arg == '-o':
            output_path = sys.argv[index + 1]
            try:
                output = open(output_path, 'w')
                output.write('')
                output.close()
            except:
                print("Couldn't create the output file, try another path!")
                quit()

        elif arg == '-c':
            try:
                time_to_copy = int(sys.argv[index + 1])
            except:
                print("Waiting time must be a number!")
                quit()

        elif arg == '-q':
            try:
                time_to_quit = int(sys.argv[index + 1])
            except:
                print("Waiting time must be a number!")
                quit()

        elif arg == '-k':
            try:
                keep_alive = eval(sys.argv[index + 1].title())
            except:
                print("Keep connection option must be either true or false!")
                quit()


# Program options.
translated_text = ''
output_path = 'Translated Text.txt'
time_to_copy = 5
time_to_quit = 60
keep_alive = False

get_arguments()

# Prepare the images.
directory = os.listdir(images_path)
for index, image in enumerate(directory):
    index = int(index)
    image = images_path + '/' + str(image)
    directory[index] = os.path.abspath(image)

# Set up the driver.
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('start-maximized')                 # Same as terminal args, just removed the (--) prefix.
options.add_argument('remote-debugging-port=9222')      # Port must be > 1000.

service = Service(executable_path='chromedriver/chromedriver')
driver = webdriver.Chrome(service=service, options=options, keep_alive=keep_alive)

URL = f'https://translate.google.com/?sl={lang_1}&tl={lang_2}&op=images'
driver.get(URL)

# Start translating.
for image in directory:
    # Find file input field & Give the path.
    file_field = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[5]/c-wiz/div[2]/c-wiz/div/div/div/div[1]/div[2]/div[2]/div[1]/input')
    file_field.send_keys(image)     # image is passed as a path.

    # In case we wanna use the open dialog method instead (only Windows):
    """
    from pynput.keyboard import Key, Controller
    
    # Find the upload button.
    upload_button = driver.find_element(By.XPATH, "/html/body/c-wiz/div/div[2]/c-wiz/div[5]/c-wiz/div[2]/c-wiz/div/div/div/div[1]/div[2]/div[2]/div[1]/div/button/span")
    upload_button.click()
    sleep(1)
    
    # Enter the path in the dialog's input field.
    keyword = Controller()
    keyword.type("/home/mohyoo/Pictures/Wallpaper/3.jpg")
    keyword.press(Key.enter)
    keyword.release(Key.enter)
    """

    # Copy the translated text.
    sleep(time_to_copy)    # Waiting for translation, it varies according to the internet speed.
    copy_button = driver.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.LjDxcd.XhPA0b.LQeN7.qaqQfe')
    copy_button.click()

    try:
        copied_text = pyperclip.paste()
        translated_text += copied_text + '\n' + '-' * 100 + '\n'
    except Exception as error:
        print('Error: ' + repr(error))
        print('Skipping image: ' + image)

    # Return & Upload another image.
    close_button = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[5]/c-wiz/div[2]/c-wiz/div/div[1]/div[2]/span[3]/button')
    close_button.click()

# Save.
try:
    output = open(output_path, 'w')
    output.write(translated_text)
    output.close()

    path = os.path.join(os.getcwd(), output_path)
    print('Translated text saved in: ' + path)
except Exception as error:
    print('Error: ' + repr(error))
    try:
        output = open('Translated Text.txt', "w")
        output.write(translated_text)
        output.close()

        path = os.path.abspath(os.getcwd() + '/Translated Text.txt')
        print('Translated text saved in: ' + path)
    except:
        print('This is the translated text, save it:\n')
        print(translated_text)

# Quit & Close the browser.
sleep(time_to_quit)
driver.quit()