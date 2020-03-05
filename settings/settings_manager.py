import json


class SettingsManager:
    def __init__(self, settings_file_path):
        self.settings_file_path = settings_file_path
        self.settings_dict = {}

    def set_settings(self, settings_dict):
        self.settings_dict = settings_dict

    def get_settings(self):
        return self.settings_dict

    def load_settings(self):
        try:
            with open(self.settings_file_path) as f:
                self.settings_dict = json.load(f)
        except FileNotFoundError as error:
            print(error)

    def save_settings(self):
        try:
            with open(self.settings_file_path, "w") as f:
                json.dump(self.settings_dict, f)
        except FileNotFoundError as error:
            print(error)
