# Description
1) A python program that allows you to translate multiple images
via google translator, without wasting time in clicking & dragging; based on selenium.
2) Still under development, please report bugs.
3) For now, it only works on Debian; but it may work for other ditributions if you know how to install dependencies.

# Requirements
1) Python libraries: pyperclip & selenium.
2) Linux packages: xclip, xsel & wl-clipboard.
3) Google Chrome.

# Installation
- There is an installer for the requirements (for Debian), but you can install them manually (better to install python libraries in a venv) & skip step (1). <br>
- Open the terminal in the program's directory and:
1) type: ````python install_requirements.py```` (or python3), and wait.
2) A <b>'venv'</b> folder should appear, now before executing the program, activate the venv: ````source venv/bin/activate````
2) Download & install google chrome: https://www.google.com/chrome/ (flatpak repository may cause issues!).

# Examples
-For brief instructions, type in the terminal: ````python google_translate.py -h```` <br>
### 1) Example 1:
- This is the simplest command: <br>
````
python google_translate.py -i images -l en_ar <br>
````
- The argument <b>'-i images'</b> is the folder containing the images, it must be inside the program folder, otherwise use absolute path. <br>
- The argument <b>'-l en_ar'</b> means translating from english (en) to arabic (ar), separated with an underscore. <br>
- To find your language's shortcut, see the <b>'languages_list.txt'</b> file. <br>
- When this command is executed, google chrome will show up & start translating on its own (it's not a virus o_o). <br> <br>

### 2) Example 2:
````
python google_translate.py -i images -l en_ar -o output.txt -q 60 -k true
````
- The argument <b>'-o output.txt'</b> is where your translated text will be saved, here it will be saved inside the program folder, otherwise use absolute path. <br>
- The argument <b>'-q 60'</b> means: when the translation finishes, how much time to wait before closing the browser & exiting the program (in seconds). <br>
- The argument <b>'-k true'</b> is an HTTP connection parameter; when true, the client binding keeps the
 same connection for every request, which <b>may</b> speed up the process.

# Exiting venv & uninstallation
1) To deactivate the venv, simply type: ````deactivate````
2) To remove the venv, simply delete the folder.
3) A <b>selenium</b> folder may be left in the <b>~/.cache</b> directory, delete it.

# What's new!
- Errors handling.
- No need to specify the <b>'-c'</b> argument anymore (c: time between upload & copy).

