import tkinter as tk


class ProgramSelectionContainer(tk.Frame):
    def __init__(self, proc_manager, settings_manager, master=None):
        super().__init__(master)
        self.proc_manager = proc_manager
        self.settings_manager = settings_manager
        tk.Label(
            master=self, text="Select programs to...do X action",
        ).grid(column=0, row=0)
        self.program_selector_listbox = tk.Listbox(
            master=self, selectmode=tk.MULTIPLE,
        )
        self.add_processes_to_listbox()
        self.program_selector_listbox.grid(column=0, row=1)
        self.refresh_programs_button = tk.Button(
            master=self,
            text="Refresh",
            command=self.refresh_button_press_handler,
        )
        self.refresh_programs_button.grid(column=1, row=1)
        self.pack()

    def refresh_button_press_handler(self):
        self.proc_manager.refresh_cache()
        self.program_selector_listbox.delete(0, tk.END)
        self.add_processes_to_listbox()

    def add_processes_to_listbox(self):
        procs_with_windows = self.proc_manager.get_processes_with_windows(
            unique_names=True
        )
        for index, proc in enumerate(procs_with_windows):
            self.program_selector_listbox.insert(index, proc.name())

    def get_selection(self):
        return [
            self.program_selector_listbox.get(index)
            for index in self.program_selector_listbox.curselection()
        ]

    def update_listbox_selections(self, items_to_select):
        listbox_items = self.program_selector_listbox.get(0, tk.END)
        for index, item in enumerate(listbox_items):
            if item in items_to_select:
                self.program_selector_listbox.selection_set(index)
            else:
                self.program_selector_listbox.selection_clear(index)
