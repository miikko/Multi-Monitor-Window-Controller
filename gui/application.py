import tkinter as tk
import tkinter.ttk
from threading import Thread
from monitor_manager import get_monitors
from process_manager import ProcessManager
from gui.proc_settings_window.main import SettingsWindow
from gui.mon_settings_container import MonitoringSettingsContainer
from gui.gui_settings_container import GUISettingsContainer
from settings.proc_settings_manager import ProcessSettingsManager
from settings.monitoring_settings_manager import MonitoringSettingsManager
from settings.gui_settings_manager import GUISettingsManager
from background_task import execute_task
from gui_visibility_handler import GUIVisibilityHandler


class Application(tk.Frame):
    def __init__(
        self,
        proc_manager,
        proc_settings_manager,
        mon_settings_manager,
        gui_settings_manager,
        gui_visibility_handler,
        width,
        height,
        master=None,
    ):
        super().__init__(master)
        self.monitors = get_monitors()
        self.proc_manager = proc_manager
        self.proc_settings_manager = proc_settings_manager
        self.mon_settings_manager = mon_settings_manager
        self.gui_settings_manager = gui_settings_manager
        self.gui_visibility_handler = gui_visibility_handler
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handle_window_close)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.master.geometry(f"{width}x{height}")

    def create_widgets(self):
        self.create_monitor_selection_section()
        self.mon_settings_container = MonitoringSettingsContainer(
            self.mon_settings_manager, master=self
        )
        self.mon_settings_container.pack()
        GUISettingsContainer(
            self.gui_settings_manager, master=self
        ).pack()

    def handle_window_close(self):
        self.gui_visibility_handler.hide_gui()

    def create_monitor_selection_section(self):
        tk.Label(
            self,
            text="You can toggle GUI visibilty by pressing Ctrl + Alt + P",
        ).pack(pady=(10, 10))
        tk.Label(
            self,
            text="Monitors are numbered the same way as can be seen in Windows Display Settings.",
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
        self.mon_settings_container.refresh_tk_vars()


if __name__ == "__main__":
    proc_manager = ProcessManager()
    proc_settings_manager = ProcessSettingsManager("proc_settings.json")
    proc_settings_manager.load_settings()
    mon_settings_manager = MonitoringSettingsManager(
        "monitoring_settings.json"
    )
    mon_settings_manager.load_settings()
    gui_settings_manager = GUISettingsManager("gui_settings.json")
    gui_settings_manager.load_settings()
    root = tk.Tk()
    background_thread = Thread(
        target=execute_task,
        args=(proc_settings_manager, mon_settings_manager),
        daemon=True,
    )
    background_thread.start()
    gui_visibility_handler = GUIVisibilityHandler(root, "ctrl+alt+P")
    app = Application(
        proc_manager,
        proc_settings_manager,
        mon_settings_manager,
        gui_settings_manager,
        gui_visibility_handler,
        800,
        400,
        master=root,
    )
    if not gui_settings_manager.get_gui_start_visibility():
        gui_visibility_handler.hide_gui()
    root.title("Multi-monitor Window Manager For Windows OS")
    app.mainloop()
