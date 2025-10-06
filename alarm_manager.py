from enum import IntEnum

class AlarmManager:
    class AlarmTypes(IntEnum):
        CPU = 0
        RAM = 1
        DISK = 2

    class Alarm:
        def __init__(self, alarm_type, threshold):
            self.type = alarm_type
            self.threshold = threshold

    alarms = [Alarm]
