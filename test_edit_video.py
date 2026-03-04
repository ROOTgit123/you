import unittest
from edit_video import parse_timeline

class TestEditVideo(unittest.TestCase):
    def test_parse_timeline(self):
        timeline_str = "01:10-01:15, 03:20-03:35, 06:45-07:05, 10:15-10:25"
        expected = [
            ("01:10", "01:15"),
            ("03:20", "03:35"),
            ("06:45", "07:05"),
            ("10:15", "10:25")
        ]
        self.assertEqual(parse_timeline(timeline_str), expected)

    def test_parse_timeline_spaces(self):
        timeline_str = " 01:10 - 01:15 , 03:20-03:35 "
        expected = [
            ("01:10", "01:15"),
            ("03:20", "03:35")
        ]
        self.assertEqual(parse_timeline(timeline_str), expected)

if __name__ == "__main__":
    unittest.main()
