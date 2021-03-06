import Utils
import Data
class StopSign:
    def __init__(self, config, drive_data: Data.DataControl):
        self.config = config
        self.drive_data = drive_data
        self.reaction_en = True
    
    def enb(self):
        self.reaction_en = True
    def go(self):
        self.drive_data.set("speed", self.drive_data.get("std_speed").data)

        @Utils.delay(delay=self.config.attention_delay)
        def go():
            self.enb()
        go()
    def run(self):
        signs_d = self.drive_data.get(Utils.SIGNS_LIST)
        stop_sign = "stop" in signs_d or "stop_sign" in signs_d
        if stop_sign:
            self.reaction_en = False
            self.drive_data.set("speed", 0)

            @Utils.delay(delay=self.config.stop_time)
            def go():
                self.go()
            go()