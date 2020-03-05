import time
from process_manager import ProcessManager
from monitor_manager import get_active_monitor_name
from window_manager import (
    minimize_windows_belonging_to_processes,
    maximize_windows_belonging_to_processes,
    restore_windows_belonging_to_processes,
)


def execute_task(proc_settings_manager, mon_settings_manager):
    active_monitor_name = get_active_monitor_name()
    process_manager = ProcessManager()
    interval_counter = 0
    while True:
        proc_cache_refresh_rate = mon_settings_manager.get_process_cache_refresh_rate()
        interval_secs = mon_settings_manager.get_interval_setting()
        if (
            interval_counter
            >= proc_cache_refresh_rate
        ):
            process_manager.refresh_cache()
            interval_counter = 0
        time.sleep(interval_secs)
        proc_settings = proc_settings_manager.get_settings()
        prev_monitor_name = active_monitor_name
        active_monitor_name = get_active_monitor_name()
        if prev_monitor_name != active_monitor_name:
            handle_active_monitor_change(
                prev_monitor_name,
                active_monitor_name,
                proc_settings,
                process_manager,
            )
        interval_counter += 1


def handle_active_monitor_change(
    prev_monitor_name, active_monitor_name, proc_settings, process_manager
):
    process_names_to_minimize = []
    process_names_to_maximize = []
    process_names_to_restore = []
    if prev_monitor_name in proc_settings:
        process_names_to_minimize += proc_settings[prev_monitor_name][
            "Exit"
        ]["Minimize"]
        process_names_to_maximize += proc_settings[prev_monitor_name][
            "Exit"
        ]["Maximize"]
        process_names_to_restore += proc_settings[prev_monitor_name][
            "Exit"
        ]["Restore"]
    if active_monitor_name in proc_settings:
        process_names_to_minimize += proc_settings[active_monitor_name][
            "Enter"
        ]["Minimize"]
        process_names_to_maximize += proc_settings[active_monitor_name][
            "Enter"
        ]["Maximize"]
        process_names_to_restore += proc_settings[active_monitor_name][
            "Enter"
        ]["Restore"]
    for process_name in process_names_to_minimize:
        processes_with_name = process_manager.get_processes_with_window_and_name(
            process_name
        )
        minimize_windows_belonging_to_processes(processes_with_name)
    for process_name in process_names_to_maximize:
        processes_with_name = process_manager.get_processes_with_window_and_name(
            process_name
        )
        maximize_windows_belonging_to_processes(processes_with_name)
    for process_name in process_names_to_restore:
        processes_with_name = process_manager.get_processes_with_window_and_name(
            process_name
        )
        restore_windows_belonging_to_processes(processes_with_name)
