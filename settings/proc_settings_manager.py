from settings.settings_manager import SettingsManager

""" PROC_SETTINGS.JSON FILE STRUCTURE
{
 Monitor 1:
  {
   Enter:
    {
     Restore: ["chrome.exe", "code.exe"],
     Maximize: ["notepad.exe"],
     Minimize: ["discord.exe", "steam.exe"]
    },
   Exit:
    {
     Restore: [],
     Minimize: []
    }
  }
}
"""


class ProcSettingsManager(SettingsManager):
    def __init__(self, settings_file_path):
        super().__init__(settings_file_path)

    def add_setting(
        self, monitor_name, condition, window_action, process_name
    ):
        """
        Parameters:
            monitor_name: Name of the monitor, example 'Monitor 1'
            condition: Either 'Enter' or 'Exit'
            window_action: Either 'Restore', 'Maximize' or 'Minimize'
            process_name: Name of the process, example 'chrome.exe'
        """
        if monitor_name not in self.settings_dict:
            self.settings_dict[monitor_name] = {
                "Enter": {"Restore": [], "Maximize": [], "Minimize": []},
                "Exit": {"Restore": [], "Maximize": [], "Minimize": []},
            }
        process_name_list = self.settings_dict[monitor_name][condition][
            window_action
        ]
        if process_name not in process_name_list:
            process_name_list.append(process_name)

    def remove_setting(
        self, monitor_name, condition, window_action, process_name
    ):
        """
        Parameters:
            monitor_name: Name of the monitor, example 'Monitor 1'
            condition: Either 'Enter', 'Maximize' or 'Exit'
            window_action: Either 'Restore' or 'Minimize'
            process_name: Name of the process, example 'chrome.exe'
        """
        if monitor_name not in self.settings_dict:
            return
        process_name_list = self.settings_dict[monitor_name][condition][
            window_action
        ]
        if process_name in process_name_list:
            process_name_list.remove(process_name)
