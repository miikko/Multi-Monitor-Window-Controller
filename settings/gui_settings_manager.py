from settings.settings_manager import SettingsManager

""" GUI_SETTINGS_JSON FILE STRUCTURE
{
 GUIVisibleOnStart: True
}
"""

DEFAULT_GUI_START_VISIBILITY = True


class GUISettingsManager(SettingsManager):
    def __init__(self, settings_file_path):
        super().__init__(settings_file_path)

    def modify_gui_start_visibility(self, new_value):
        self.settings_dict["GUIVisibleOnStart"] = bool(new_value)

    def get_gui_start_visibility(self):
        if "GUIVisibleOnStart" not in self.settings_dict:
            return DEFAULT_GUI_START_VISIBILITY
        return self.settings_dict["GUIVisibleOnStart"]
