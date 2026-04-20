from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from canvas_material_downloader.fs_utils import course_directory_name, file_destination_name, sanitize_segment


class FsUtilsTests(unittest.TestCase):
    def test_sanitize_segment_removes_windows_invalid_characters(self) -> None:
        self.assertEqual(sanitize_segment('Week 1: Intro/Overview?.pdf'), "Week 1_ Intro_Overview_.pdf")

    def test_sanitize_segment_handles_reserved_names(self) -> None:
        self.assertEqual(sanitize_segment("CON"), "CON_")

    def test_course_directory_name_includes_course_id(self) -> None:
        course = {"id": 42, "course_code": "CS101", "name": "Intro to Programming"}
        self.assertEqual(course_directory_name(course), "42 - CS101 - Intro to Programming")

    def test_file_destination_name_prefixes_file_id(self) -> None:
        file_data = {"id": 99, "display_name": "Syllabus.pdf"}
        self.assertEqual(file_destination_name(file_data), "99 - Syllabus.pdf")


if __name__ == "__main__":
    unittest.main()
