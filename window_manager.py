from win32 import win32gui, win32process

SW_MINIMIZE = 6
SW_MAXIMIZE = 3
SW_RESTORE = 9
GW_OWNER = 4


def window_enum_handler(hwnd, handler_param):
    window_process_id = win32process.GetWindowThreadProcessId(hwnd)[1]
    for process in handler_param["processes"]:
        if process.pid == window_process_id:
            owner_window_handle = win32gui.GetWindow(hwnd, GW_OWNER)
            owner_window_is_visible = win32gui.IsWindowVisible(
                owner_window_handle
            )
            if owner_window_is_visible:
                win32gui.ShowWindow(
                    owner_window_handle, handler_param["operation"]
                )


def minimize_windows_belonging_to_processes(processes):
    handler_param = {
        "processes": processes,
        "operation": SW_MINIMIZE,
    }
    win32gui.EnumWindows(window_enum_handler, handler_param)


def maximize_windows_belonging_to_processes(processes):
    handler_param = {
        "processes": processes,
        "operation": SW_MAXIMIZE,
    }
    win32gui.EnumWindows(window_enum_handler, handler_param)


def restore_windows_belonging_to_processes(processes):
    handler_param = {
        "processes": processes,
        "operation": SW_RESTORE,
    }
    win32gui.EnumWindows(window_enum_handler, handler_param)
