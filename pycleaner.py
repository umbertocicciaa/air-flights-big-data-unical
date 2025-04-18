import os

os.popen('find . | grep -E "(__pycache__)" | xargs rm -rf')