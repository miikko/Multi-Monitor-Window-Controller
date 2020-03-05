import tkinter as tk
import tkinter.ttk
from threading import Thread
from monitor_manager import get_monitors
from process_manager import ProcessManager
from gui.settings_window.main import SettingsWindow
from settings.proc_settings_manager import ProcSettingsManager
from settings.monitoring_settings_manager import MonitoringSettingsManager
from background_task import execute_task
from gui_visibility_handler import GUIVisibilityHandler


class Application(tk.Frame):
    def __init__(
        self,
        proc_manager,
        proc_settings_manager,
        mon_settings_manager,
        width,
        height,
        master=None,
    ):
        super().__init__(master)
        self.monitors = get_monitors()
        self.proc_manager = proc_manager
        self.proc_settings_manager = proc_settings_manager
        self.mon_settings_manager = mon_settings_manager
        self.master = master
        self.pack(fill="both", expand=True)
        self.mon_interval_var = tk.StringVar()
        self.mon_proc_refresh_rate_var = tk.StringVar()
        self.mon_interval_var.set(
            str(self.mon_settings_manager.get_interval_setting())
        )
        self.mon_proc_refresh_rate_var.set(
            str(
                self.mon_settings_manager.get_process_cache_refresh_rate()
            )
        )
        self.create_widgets()
        self.mon_interval_var.trace("w", self.tk_var_change_handler)
        self.mon_proc_refresh_rate_var.trace(
            "w", self.tk_var_change_handler
        )
        self.master.geometry(f"{width}x{height}")

    def create_widgets(self):
        self.create_monitor_selection_section()
        self.create_mon_settings_config_container()

    def create_monitor_selection_section(self):
        tk.Label(
            self,
            text="You can toggle GUI visibilty by pressing Ctrl + Alt + P",
        ).pack(pady=(10, 10))
        tk.Label(
            self, text="Monitors are numbered starting from left."
        ).pack()
        self.mon_selector_dropdown = tk.ttk.Combobox(
            self,
            values=[
                f"Monitor {index}"
                for index, _ in enumerate(self.monitors, 1)
            ],
            state="readonly",
        )
        self.mon_selector_dropdown.set("Choose a monitor")
        self.mon_selector_dropdown.bind(
            "<<ComboboxSelected>>", self.monitor_selection_handler
        )
        self.mon_selector_dropdown.pack()
        tk.Label(
            self,
            text="""Changing the monitor setup after creating settings may cause unexpected behaviour.
            It is highly recommended to clear any previously made settings after changing monitor setups.
            """,
        ).pack(pady=(10, 0))
        tk.Button(
            self, text="Clear settings", command=self.clear_settings
        ).pack()

    def monitor_selection_handler(self, event_object):
        monitor_id = self.mon_selector_dropdown.get().split(" ")[-1]
        SettingsWindow(
            monitor_id,
            800,
            400,
            self.proc_manager,
            self.proc_settings_manager,
            master=self,
            root=self.master,
        )

    def clear_settings(self):
        self.proc_settings_manager.set_settings({})
        self.proc_settings_manager.save_settings()
        self.mon_settings_manager.set_settings({})
        self.mon_settings_manager.save_settings()

    # TODO: Move this to own Class
    def create_mon_settings_config_container(self):
        tk.Label(
            self,
            text="""You can configure the background task that monitors your cursor, processes and their windows by changing the values below.
        When using this program for the first time, it is recommended to follow the computer's CPU usage and adjust the values accordingly.""",
        ).pack(pady=(10, 10))
        tk.Label(
            self,
            text="Number of seconds between monitoring checkups. Takes a positive decimal number",
        ).pack()
        tk.Entry(self, textvariable=self.mon_interval_var).pack()
        tk.Label(
            self,
            text="Number of monitoring checkups before refreshing running process cache. Takes a positive whole number (decimals are rounded down).",
        ).pack()
        tk.Entry(self, textvariable=self.mon_proc_refresh_rate_var).pack()
        self.button_container = tk.Frame(self)
        self.mon_settings_apply_button = tk.Button(
            self.button_container,
            text="APPLY",
            command=self.modify_monitoring_settings,
        )
        self.mon_settings_apply_button.grid(column=0, row=0)
        self.mon_settings_save_button = tk.Button(
            self.button_container,
            text="SAVE",
            command=self.save_monitoring_settings,
        )
        self.mon_settings_save_button.grid(column=1, row=0)
        self.button_container.pack()

    def tk_var_change_handler(self, *args):
        try:
            new_mon_interval = float(self.mon_interval_var.get())
            new_mon_proc_refresh_rate = int(
                self.mon_proc_refresh_rate_var.get()
            )
            if new_mon_interval > 0 and new_mon_proc_refresh_rate > 0:
                button_state = tk.NORMAL
            else:
                button_state = tk.DISABLED
        except ValueError:
            button_state = tk.DISABLED
        self.mon_settings_apply_button.config(state=button_state)
        self.mon_settings_save_button.config(state=button_state)

    def modify_monitoring_settings(self):
        self.mon_settings_manager.modify_interval_setting(
            float(self.mon_interval_var.get())
        )
        self.mon_settings_manager.modify_proc_cache_refresh_rate(
            int(self.mon_proc_refresh_rate_var.get())
        )

    def save_monitoring_settings(self):
        self.modify_monitoring_settings()
        self.mon_settings_manager.save_settings()


if __name__ == "__main__":
    proc_manager = ProcessManager()
    proc_settings_manager = ProcSettingsManager(
        "settings/proc_settings.json"
    )
    proc_settings_manager.load_settings()
    mon_settings_manager = MonitoringSettingsManager(
        "settings/monitoring_settings.json"
    )
    mon_settings_manager.load_settings()
    root = tk.Tk()
    background_thread = Thread(
        target=execute_task,
        args=(proc_settings_manager, mon_settings_manager),
        daemon=True,
    )
    background_thread.start()
    app = Application(
        proc_manager,
        proc_settings_manager,
        mon_settings_manager,
        800,
        400,
        master=root,
    )
    root.title("Multi-monitor Window Manager For Windows OS")
    GUIVisibilityHandler(root, "ctrl+alt+P")
    app.mainloop()
