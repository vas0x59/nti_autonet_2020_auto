import Utils
import Data
class PedestrianSign:
    def __init__(self, config, drive_data: Data.DataControl):
        self.config = config
        self.drive_data = drive_data
        self.reaction_en = True
    
    def enb(self):
        self.reaction_en = True
    def go(self):
        self.drive_data.set("speed", self.drive_data.get("std_speed").data)

        @Utils.delay(delay=self.config.attention_delay)
        self.enb()
    def run(self):
        signs_d = self.drive_data.get(Utils.SIGNS_LIST)
        stop_sign = "stop" in signs_d or "stop_sign" in signs_d
        if stop_sign:
            self.reaction_en = False
            self.drive_data.set("speed", self.config.slow_speed)

            @Utils.delay(delay=self.config.slow_time)
            self.go()