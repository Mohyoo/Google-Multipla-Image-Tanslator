try:
    import os
    import sys
    import pyperclip
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep

except Exception as error:
    print('Error while importing modules, did you install all the requirements?')
    print(repr(error))
    quit()

# Prepare the fonts.
R  = '\033[31m\033[1m'      # Red.
G  = '\033[32m\033[1m'      # Green.
B  = '\033[34m'             # Blue.
RF = '\033[0m'              # Reset Font.


# Prepare the functions.
def show_instructions():
    """Display instructions & commands."""
    message = (f"""
               {G}*) First thing first:{RF}
                  -Put your images in a folder, then copy the folder's path.
                  -Go to 'languages_list.txt' and find your language's shortcut.
               {G}*) Required arguments:{RF}
                  -i        Path to the images folder.
                  -l        Languages, e.g: '-l en_ar', this means from english to arabic;
                            don't forget the underscore.
               {G}*) Optional arguments:{RF}
                  -o        Path of the output text file, default is: current directory.
                  -q        After finishing, time to wait before closing the browser (in seconds),
                            default is 60.
                  -k        Keep the same connection for every server request (it may speed up the
                            process), default is false.
               {G}*) Tips:{RF}
                  -Compress your files before uploading, thus you can use less waiting time argument (-c);
                   you can use 'Curtail' for Linux, or 'MassCompressor' for Windows.
                  -Use waiting time (-c) according to image size & internet speed, if it's too low
                   you may get an error.
                  -Not all languages are supported for image translating.""")

    print(message)


def get_arguments():
    """Organize the command line arguments."""
    global images_path, lang_1, lang_2, output_path, time_to_copy, time_to_quit, keep_alive

    print(R, end='')
    required_args = []
    for index, arg in enumerate(sys.argv):
        if (arg == '-h') or (arg == 'help') or (arg == '--help'):
            show_instructions()
            quit()

        # Required arguments.
        elif arg == '-i':
            required_args.append('-i')
            images_path = sys.argv[index + 1]
            if not os.path.exists(images_path):
                print("Path doesn't exist, try absolute path instead!")
                quit()

        elif arg == '-l':
            try:
                required_args.append('-l')
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

    # Check missing arguments.
    if '-i' not in required_args:
        print('Missing images folder argument (-i)!')
        quit()
    if '-l' not in required_args:
        print('Missing languages argument (-l)!')
        quit()

    print(RF, end='')


def emergency_save():
    """In case of unexpected error, immediately save the translated text."""
    try:
        output = open('Translated Text.txt', "w")
        output.write(translated_text)
        output.close()

        path = os.path.abspath(os.getcwd() + '/Translated Text.txt')
        print(G + 'Translated text was partially saved in: ' + path)
    except Exception as error:
        print(R + 'Error: ' + repr(error))
        print('Could not save the text file.')
        print(G + 'This is the translated text, save it:\n')
        print(B + translated_text)


# Program options.
translated_text = ''
output_path = 'Translated Text.txt'
time_to_click = 0.1
MAX_ATTEMPTS = 600
time_to_quit = 60
keep_alive = False

get_arguments()

# Prepare the images.
directory = os.listdir(images_path)
only_names = directory[:]      # Used for debugging.
for index, image in enumerate(directory):
    index = int(index)
    image = images_path + '/' + str(image)
    directory[index] = os.path.abspath(image)

# Set up the driver.
try:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('start-maximized')                 # Same as terminal args, just removed the (--) prefix.
    options.add_argument('remote-debugging-port=9222')      # Port must be > 1000.

    driver = webdriver.Chrome(options=options, keep_alive=keep_alive)

    URL = f'https://translate.google.com/?sl={lang_1}&tl={lang_2}&op=images'
    driver.get(URL)

    # Start translating.
    for image in directory:
        # Find file input field & Give the path.
        attempts = 0
        while True:
            try:
                file_field = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[5]/c-wiz/div[2]/c-wiz/div/div/div/div[1]/div[2]/div[2]/div[1]/input')
                file_field.send_keys(image)     # image is passed as a path.
                break
            except:
                if attempts >= MAX_ATTEMPTS:
                    print('Timeout, skipping this image...')
                    driver.get(URL)
                    continue
                else:
                    attempts += 1
                    sleep(time_to_click)

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
        image = only_names[directory.index(image)]      # Use the image name for errors, not full path.
        attempts = 0

        try:
            while True:
                try:
                    copy_button = driver.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.LjDxcd.XhPA0b.LQeN7.qaqQfe')
                    copy_button.click()
                    break
                except:
                    if attempts >= MAX_ATTEMPTS:
                        print('Timeout, skipping this image...')
                        driver.get(URL)
                        continue
                    else:
                        attempts += 1
                        sleep(time_to_click)

        except Exception as error:
            print(R + 'Error while copying: ' + repr(error))
            print('Skipping image: ' + image + RF)
            driver.get(URL)
            continue

        # Access the copied text from clipboard.
        try:
            copied_text = pyperclip.paste()
            translated_text += copied_text + '\n' + '-' * 100 + '\n'
        except Exception as error:
            print(R + 'Error while accessing the clipboard: ' + repr(error))
            print('Maybe you are missing python libraries: (pyperclip) & (selenium).')
            print('Skipping image: ' + image + RF)


        # Return & Upload another image.
        attempts = 0

        while True:
            try:
                close_button = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[5]/c-wiz/div[2]/c-wiz/div/div[1]/div[2]/span[3]/button')
                close_button.click()
                break
            except:
                if attempts >= MAX_ATTEMPTS:
                    print('Timeout, skipping this image...')
                    driver.get(URL)
                    continue
                else:
                    attempts += 1
                    sleep(time_to_click)


    # Save the translated text.
    print('\n')
    try:
        output = open(output_path, 'w')
        output.write(translated_text)
        output.close()

        path = os.path.join(os.getcwd(), output_path)
        print(G + 'Translated text saved in: ' + path + RF)
    except Exception as error:
        print(R + 'Error: ' + repr(error) + RF)
        emergency_save()

    # Quit & Close the browser.
    sleep(time_to_quit)
    driver.quit()

except Exception as error:
    print('\nUnexpected error, please report the red text to me.' + G)
    print('Github: https://github.com/Mohyoo/Google-Multiple-Images-Tanslator/issues')
    print('Email: didouna.mohyeddine@gmail.com' + R)
    emergency_save()
    raise error
