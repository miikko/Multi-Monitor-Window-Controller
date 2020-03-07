import tkinter as tk


class MonitoringSettingsContainer(tk.Frame):
    def __init__(self, mon_settings_manager, master):
        super().__init__(master)
        self.mon_settings_manager = mon_settings_manager
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

    def create_widgets(self):
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

    def refresh_tk_vars(self):
        self.mon_interval_var.set(
            str(self.mon_settings_manager.get_interval_setting())
        )
        self.mon_proc_refresh_rate_var.set(
            str(
                self.mon_settings_manager.get_process_cache_refresh_rate()
            )
        )

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
