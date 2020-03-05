from win32 import win32gui, win32process
import psutil


class ProcessManager:
    def __init__(self):
        self.processes_with_windows_cache = None
        self.refresh_cache()

    def get_processes_with_windows(self, unique_names=False):
        if unique_names:
            return filter_processes_with_same_name(
                self.processes_with_windows_cache
            )
        return self.processes_with_windows_cache

    def add_window_process_ids(self, hwnd, window_process_ids):
        window_text = win32gui.GetWindowText(hwnd).strip()
        if window_text == "":
            return
        window_process_id = win32process.GetWindowThreadProcessId(hwnd)[1]
        window_process_ids.add(window_process_id)

    def refresh_cache(self):
        all_processes = psutil.process_iter(["name", "pid"])
        window_process_ids = set()
        win32gui.EnumWindows(
            self.add_window_process_ids, window_process_ids
        )
        processes_with_windows = set()
        for process in all_processes:
            process_has_window = False
            for process_id in window_process_ids:
                if process.pid == process_id:
                    process_has_window = True
                    break
            if process_has_window:
                processes_with_windows.add(process)
        self.processes_with_windows_cache = processes_with_windows

    def does_process_own_window(self, process_name):
        for process in self.processes_with_windows_cache:
            if process.name().lower() == process_name.lower():
                return True
        return False

    def get_processes_with_window_and_name(self, name):
        selected_processes = []
        for process in self.processes_with_windows_cache:
            if process.name().lower() == name.lower():
                selected_processes.append(process)
        return selected_processes


def filter_processes_with_same_name(processes):
    uniquely_named_processes = []
    for process in processes:
        is_unique = True
        for uniquely_named_process in uniquely_named_processes:
            if uniquely_named_process.name() == process.name():
                is_unique = False
                break
        if is_unique:
            uniquely_named_processes.append(process)
    return uniquely_named_processes
