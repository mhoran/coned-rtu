from datetime import datetime, timedelta, timezone
import unittest

from reading import Reading


class TestReading(unittest.TestCase):
    def setUp(self):
        self.sometime = datetime(2010, 12, 25, 14, 30, 0, tzinfo=timezone.utc)
        self.later = datetime(2010, 12, 25, 14, 30, 1, tzinfo=timezone.utc)

    def test_start_time_must_be_before_end_time(self):
        # start and end time the same
        with self.assertRaises(ValueError):
            Reading(self.sometime, self.sometime, "wh", 1)

        # start time after end time
        with self.assertRaises(ValueError):
            Reading(self.later, self.sometime, "wh", 1)

    def test_enforces_units(self):
        # only wh or kwh supported
        with self.assertRaises(ValueError):
            Reading(self.sometime, self.later, "mwh", 1)

        # incorrect capitalization is okay
        Reading(self.sometime, self.later, "Wh", 1)

    def test_duration(self):
        r = Reading(self.sometime, self.later, "wh", 1)
        self.assertEqual(r.duration(), timedelta(seconds=1))
