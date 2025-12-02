import threading


class SimpleProcessor:
    def __init__(self, data: dict):
        self.time_passed_flag = True
        self.pet_data = data

    def changes_satiety(self, change: int):
        self.pet_data["satiety"] += change

    def as_time_passes(self):
        if self.time_passed_flag:
            self.changes_satiety(-1)
            print(f"pet_data: {self.pet_data}")
            threading.Timer(10, self.as_time_passes).start()

