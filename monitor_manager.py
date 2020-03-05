from win32 import win32api
from cursor_tracker import get_cursor_pos


def get_monitors():
    return win32api.EnumDisplayMonitors()


def cursor_is_in_monitor(monitor):
    cursor_x_pos, cursor_y_pos = get_cursor_pos()
    (
        monitor_x_start,
        monitor_y_start,
        monitor_x_end,
        monitor_y_end,
    ) = monitor[-1:][0]
    return (
        monitor_x_start <= cursor_x_pos < monitor_x_end
        and monitor_y_start <= cursor_y_pos < monitor_y_end
    )


def get_active_monitor_name():
    monitors = get_monitors()
    for monitor_number, monitor in enumerate(monitors, 1):
        if cursor_is_in_monitor(monitor):
            return f"Monitor {monitor_number}"
    raise Exception("Cursor was not inside any of the detected monitors")
