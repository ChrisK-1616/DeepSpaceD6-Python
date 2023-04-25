"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       launcher.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Launcher for the main game application
"""

# Imports
from engine.game_app import GameApp


# Consts
# Globals
# Classes


# Functions
def main():
    """
    Main game application function

    :return: nothing
    """
    game_app = GameApp()
    game_app.run()


if __name__ == "__main__":
    """
    Launches the game application
    """
    # # Set the HIGHDPIAWARE registry flag for the Python interpreter if it is not as yet set, on first setting this you
    # #  will have to restart the launcher, after that it will continue to work
    # import winreg
    # reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    # key = winreg.OpenKey(reg, r"Control Panel\Desktop\WindowMetrics")
    # if winreg.QueryValueEx(key, "AppliedDPI")[0] != 96:
    #     key.Close()
    #     key = winreg.OpenKey(reg, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", 0, winreg.KEY_ALL_ACCESS)
    #
    #     # Use path to the current Python interpreter
    #     winreg.SetValueEx(key, "C:\Python39\pythonw.exe", 0, winreg.REG_SZ, "HIGHDPIAWARE")
    #     winreg.SetValueEx(key, "C:\Python39\python.exe", 0, winreg.REG_SZ, "HIGHDPIAWARE")
    # key.Close()
    # reg.Close()
    #
    main()
