"""Unit tests for student record operations."""
import json
import tempfile
import unittest
from pathlib import Path

from src.models.student import Student
from src.services.student_service import StudentService


def sample_student(student_id="T-001"):
    return Student(student_id, "Taylor", "Sample", "BSIT", 3, "taylor@example.com")


class StudentServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name) / "students.json"
        self.service = StudentService(self.data_path, "json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_student(self):
        self.service.add_student(sample_student())
        records = self.service.list_students()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].student_id, "T-001")

    def test_duplicate_student_id_is_rejected(self):
        self.service.add_student(sample_student())
        with self.assertRaises(ValueError):
            self.service.add_student(sample_student())

    def test_update_student(self):
        self.service.add_student(sample_student())
        updated = Student("T-001", "Taylor", "Updated", "BSIT", 4, "taylor@example.com")
        self.service.update_student("T-001", updated)
        self.assertEqual(self.service.get_student("T-001").last_name, "Updated")

    def test_delete_student(self):
        self.service.add_student(sample_student())
        self.service.delete_student("T-001")
        self.assertEqual(self.service.list_students(), [])

    def test_invalid_email_is_rejected(self):
        invalid = Student("T-002", "Casey", "Test", "BSIT", 2, "not-an-email")
        with self.assertRaises(ValueError):
            self.service.add_student(invalid)

    def test_search_student(self):
        self.service.add_student(sample_student())
        self.assertEqual(len(self.service.search_students("Taylor")), 1)


if __name__ == "__main__":
    unittest.main()
