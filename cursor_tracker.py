from win32 import win32gui


def get_cursor_pos():
    return win32gui.GetCursorPos()
