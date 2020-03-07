import tkinter as tk
import copy
from gui.proc_settings_window.containers.cursor_event_container import (
    CursorEventContainer,
)
from gui.proc_settings_window.containers.program_selection_container import (
    ProgramSelectionContainer,
)
from gui.proc_settings_window.containers.window_action_container import (
    WindowActionContainer,
)


class SettingsWindow(tk.Toplevel):
    def __init__(
        self,
        selected_monitor_id,
        width,
        height,
        proc_manager,
        settings_manager,
        master=None,
        root=None,
    ):
        super().__init__(master)
        self.monitor_name = f"Monitor {selected_monitor_id}"
        self.root = root
        self.root.wm_attributes("-disabled", True)
        self.protocol("WM_DELETE_WINDOW", self.window_close_handler)
        self.proc_manager = proc_manager
        self.settings_manager = settings_manager
        self.original_settings = copy.deepcopy(
            settings_manager.get_settings()
        )
        self.create_widgets()
        self.geometry(f"{width}x{height}")

    def window_close_handler(self):
        self.root.wm_attributes("-disabled", False)
        self.destroy()

    def selection_change_handler(self, *args):
        condition = self.cursor_event_container.get_selection()
        window_action = self.window_action_container.get_selection()
        settings = self.settings_manager.get_settings()
        if condition and window_action and self.monitor_name in settings:
            process_names = settings[self.monitor_name][condition][
                window_action
            ]
            self.program_selection_container.update_listbox_selections(
                items_to_select=process_names
            )

    def create_widgets(self):
        tk.Label(
            master=self, text=f"{self.monitor_name} selected",
        ).pack()
        self.cursor_event_container = CursorEventContainer(
            self.selection_change_handler, master=self
        )
        self.program_selection_container = ProgramSelectionContainer(
            self.proc_manager, self.settings_manager, master=self
        )
        self.window_action_container = WindowActionContainer(
            self.selection_change_handler, master=self
        )
        self.create_bottom_button_container()

    def create_bottom_button_container(self):
        self.bottom_button_container = tk.Frame(master=self)
        self.confirm_button = tk.Button(
            master=self.bottom_button_container,
            text="OK",
            command=self.confirm_changes,
        )
        self.confirm_button.grid(column=0, row=0)
        self.apply_button = tk.Button(
            master=self.bottom_button_container,
            text="APPLY",
            command=self.apply_changes,
        )
        self.apply_button.grid(column=1, row=0)
        self.cancel_button = tk.Button(
            master=self.bottom_button_container,
            text="CANCEL",
            command=self.cancel_changes,
        )
        self.cancel_button.grid(column=2, row=0)
        self.bottom_button_container.pack()

    def confirm_changes(self):
        self.apply_changes()
        self.settings_manager.save_settings()
        self.window_close_handler()

    def apply_changes(self):
        condition = self.cursor_event_container.get_selection()
        window_action = self.window_action_container.get_selection()
        if not condition or not window_action:
            return
        selected_process_names = (
            self.program_selection_container.get_selection()
        )
        settings = self.settings_manager.get_settings()
        if self.monitor_name in settings:
            process_names = settings[self.monitor_name][condition][
                window_action
            ]
            for process_name in process_names:
                if process_name not in selected_process_names:
                    self.settings_manager.remove_setting(
                        self.monitor_name,
                        condition,
                        window_action,
                        process_name,
                    )
        for process_name in selected_process_names:
            self.settings_manager.add_setting(
                self.monitor_name, condition, window_action, process_name
            )

    def cancel_changes(self):
        self.settings_manager.set_settings(self.original_settings)
        self.window_close_handler()
