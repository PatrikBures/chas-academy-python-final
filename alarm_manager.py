from enum import IntEnum

class AlarmManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AlarmManager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.__alarms = []

    @property
    def alarms(self):
        return self.__alarms

    class AlarmTypes(IntEnum):
        CPU = 0
        RAM = 1
        DISK = 2

    class Alarm:
        def __init__(self, type: 'AlarmManager.AlarmTypes', threshold: int):
            """
            Takes int alarmtype and int
            :param type: AlarmTypes
            :param threshold: 1-100 int
            :return: None
            """
            self.__type: 'AlarmManager.AlarmTypes' = type
            self.__threshold: int = threshold

        @property
        def type(self):
            return self.__type
        
        @property
        def threshold(self):
            return self.__threshold

    def add_alarm(self, type: 'AlarmManager.AlarmTypes', threshold: int):
        self.__alarms.append(AlarmManager.Alarm(type, threshold))

    def remove_alarm(self, idx: int):
        self.__alarms.pop(idx)

    def remove__alarms(self, indexes: list[int]):
        indexes.sort(reverse=True)

        for idx in indexes:
            self.__alarms.pop(idx)

    def set_alarms(self, new_alarms):
        self.__alarms = new_alarms

    def has_alarms(self) -> bool:
        if self.__alarms:
            return True
        else:
            return False

    def alarm_exists(self, type: AlarmTypes, threshold: int) -> bool:
        for alarm in self.__alarms:
            if alarm.type == type and alarm.threshold == threshold:
                return True
        return False

