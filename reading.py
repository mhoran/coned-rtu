ENERGY_UNITS = ("wh", "kwh")


class Reading:
    """
    Reading represents an energy reading over an interval. It is essentially
    the same in concept as an ESPI IntervalBlock.
    """

    def __init__(self, start_time, end_time, unit, value):
        if start_time >= end_time:
            raise ValueError("end_time must be after start_time.")

        self.start_time = start_time
        self.end_time = end_time

        if unit.lower() not in ENERGY_UNITS:
            raise ValueError("Invalid unit: use only Wh or kWh.")

        if unit.lower() == "kwh":
            value = value * 1000

        self.wh = value

    def duration(self):
        return self.end_time - self.start_time
