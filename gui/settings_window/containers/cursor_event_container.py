import tkinter as tk


class CursorEventContainer(tk.Frame):
    def __init__(self, change_handler, master=None):
        super().__init__(master)
        self.cursor_event_option = tk.StringVar(value="None")
        self.cursor_event_option.trace("w", change_handler)
        self.create_radio_buttons()
        self.pack()

    def create_radio_buttons(self):
        tk.Radiobutton(
            self,
            text="if cursor enters this monitor...",
            variable=self.cursor_event_option,
            value="Enter",
        ).pack()
        tk.Radiobutton(
            self,
            text="if cursor leaves this monitor...",
            variable=self.cursor_event_option,
            value="Exit",
        ).pack()

    def get_selection(self):
        if self.cursor_event_option.get() == "None":
            return None
        return self.cursor_event_option.get()
