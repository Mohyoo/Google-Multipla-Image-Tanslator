import os

# Python venv & libraries.
cmd = ('deactivate && '
       'python -m venv venv && '
       'source venv/bin/activate && '
       'pip install pyperclip selenium && '
       'deactivate')
os.system(cmd)

# Linux packages.
os.system('sudo apt install xclip xsel wl-clipboard')

# Chromedriver & Google Chrome.
# -Chromedriver:  https://googlechromelabs.github.io/chrome-for-testing/#stable
# -Google Chrome: https://www.google.com/chrome/
