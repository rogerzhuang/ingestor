from abc import ABC, abstractmethod


class Updater(ABC):
    def __init__(self, start_date, root_folder):
        self.start_date = start_date
        self.root_folder = root_folder

    @abstractmethod
    def update(self):
        pass
