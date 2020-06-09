#The command to publish as .exe on Windows:
pyinstaller -i "kanji.ico" --add-data "dkengine;dkengine" -F kanji.py