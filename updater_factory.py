import json
from updaters.edgar_updater import EDGARUpdater


class UpdaterFactory():
    def __init__(self, start_date, root_folder, updaters_info_file):
        self.start_date = start_date
        self.root_folder = root_folder
        with open(updaters_info_file) as f:
            updaters_info = json.load(f)
        self.updaters_info = updaters_info

    def get_updaters(self):
        updaters = []
        for updater_info in self.updaters_info:
            if updater_info["updater_type"] == "EDGAR":
                updaters.append(EDGARUpdater(
                    self.start_date, self.root_folder, updater_info["updater_params"]))
            # Add other updaters here
            else:
                raise ValueError(
                    f"Unsupported updater type: {updater_info['type']}")
        return updaters
