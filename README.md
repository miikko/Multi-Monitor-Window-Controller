# Multi-Monitor Window Controller for Windows OS

![Picture displaying the GUI](pictures/gui_picture.PNG?raw=true "Picture displaying the GUI")

## Features

* Allows the user to control how application windows behave when cursor is moved from one monitor to another
* Window actions available: Restore, Maximize and Minimize
* Allows the user to control how CPU intensive the program is by modifying monitoring values
* Allows the user to control whether the GUI is visible on startup
* Program will minimize to taskbar when the GUI is closed
* Works with Windows OS
* Tested with Python 3.7

## Setup

1. Make sure you have an appropriate [Python](https://www.python.org/downloads/windows/) version installed and added to PATH.
1. Clone this repository: `git clone https://github.com/miikko/Multi-Monitor-Window-Controller.git`
1. Navigate into cloned repository: `cd Multi-Monitor-Window-Controller`
1. Install dependencies: `pip install -r requirements.txt`
1. Run the application: `python -m gui.application`

You can control where the settings JSON-files are stored by changing their values at the bottom of `gui/application.py`.

## Generating a Windows Executable from the project

The [PyInstaller](https://www.pyinstaller.org/) dependency enables you to generate a single .exe file from the project. You can do a bunch more with it aswell and it is highly recommended to read the [manual](https://pyinstaller.readthedocs.io/en/stable/).

To generate a single .exe file from this project, run the following command while in this project's root: `pyinstaller --onefile --windowed gui/application.py`

The generated application.exe file is located in the dist-folder.

!NOTE: Before running the command, you should change the settings JSON-file paths to be in this projects root folder.

## TODO

* Add option to close program from GUI
* Make GUI clearer