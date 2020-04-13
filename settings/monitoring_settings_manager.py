from settings.settings_manager import SettingsManager

""" MONITORING_SETTINGS.JSON FILE STRUCTURE
{
 MonitoringIntervalSecs: 0.1,
 IntervalsBeforeProcCacheRefresh: 10
}
"""

DEFAULT_INTERVAL_VALUE = 5
DEFAULT_PROC_CACHE_REFRESH_RATE = 10


class MonitoringSettingsManager(SettingsManager):
    def __init__(self, settings_file_path):
        super().__init__(settings_file_path)

    def modify_interval_setting(self, new_value):
        self.settings_dict["MonitoringIntervalSecs"] = float(new_value)

    def modify_proc_cache_refresh_rate(self, new_value):
        self.settings_dict["IntervalsBeforeProcCacheRefresh"] = int(
            new_value
        )

    def get_interval_setting(self):
        if "MonitoringIntervalSecs" not in self.settings_dict:
            return DEFAULT_INTERVAL_VALUE
        return self.settings_dict["MonitoringIntervalSecs"]

    def get_process_cache_refresh_rate(self):
        if "IntervalsBeforeProcCacheRefresh" not in self.settings_dict:
            return DEFAULT_PROC_CACHE_REFRESH_RATE
        return self.settings_dict["IntervalsBeforeProcCacheRefresh"]
