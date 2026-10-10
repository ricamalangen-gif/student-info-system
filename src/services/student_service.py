"""CRUD service with JSON/XML persistence and basic error handling."""
import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from src.models.student import Student

logger = logging.getLogger(__name__)


class StudentService:
    def __init__(self, data_file, storage_format="json"):
        self.data_file = Path(data_file)
        self.storage_format = storage_format.lower()
        if self.storage_format not in ("json", "xml"):
            raise ValueError("Storage format must be 'json' or 'xml'.")
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._save([])

    def _load(self):
        try:
            if self.storage_format == "json":
                with self.data_file.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                return [Student.from_dict(item) for item in data]
            tree = ET.parse(self.data_file)
            students = []
            for node in tree.getroot().findall("student"):
                values = {child.tag: child.text or "" for child in node}
                students.append(Student.from_dict(values))
            return students
        except (json.JSONDecodeError, ET.ParseError) as exc:
            logger.exception("Could not parse student data.")
            raise ValueError(f"Student data file is invalid: {exc}") from exc
        except OSError:
            logger.exception("Could not read student data file.")
            raise

    def _save(self, students):
        try:
            if self.storage_format == "json":
                with self.data_file.open("w", encoding="utf-8") as file:
                    json.dump([student.to_dict() for student in students], file, indent=2)
            else:
                root = ET.Element("students")
                for student in students:
                    node = ET.SubElement(root, "student")
                    for key, value in student.to_dict().items():
                        ET.SubElement(node, key).text = str(value)
                ET.ElementTree(root).write(
                    self.data_file, encoding="utf-8", xml_declaration=True
                )
        except OSError:
            logger.exception("Could not save student data.")
            raise

    def list_students(self):
        return sorted(self._load(), key=lambda student: student.student_id.lower())

    def get_student(self, student_id):
        return next(
            (s for s in self._load() if s.student_id.lower() == student_id.strip().lower()),
            None,
        )

    def add_student(self, student):
        student.validate()
        students = self._load()
        if any(s.student_id.lower() == student.student_id.lower() for s in students):
            raise ValueError("A student with that ID already exists.")
        students.append(student)
        self._save(students)
        logger.info("Added student ID %s", student.student_id)

    def update_student(self, student_id, updated_student):
        updated_student.validate()
        students = self._load()
        index = next(
            (i for i, s in enumerate(students)
             if s.student_id.lower() == student_id.strip().lower()),
            None,
        )
        if index is None:
            raise LookupError("Student ID was not found.")
        if updated_student.student_id.lower() != student_id.strip().lower():
            if any(s.student_id.lower() == updated_student.student_id.lower() for s in students):
                raise ValueError("Another student already uses that ID.")
        students[index] = updated_student
        self._save(students)
        logger.info("Updated student ID %s", student_id)

    def delete_student(self, student_id):
        students = self._load()
        remaining = [s for s in students if s.student_id.lower() != student_id.strip().lower()]
        if len(remaining) == len(students):
            raise LookupError("Student ID was not found.")
        self._save(remaining)
        logger.info("Deleted student ID %s", student_id)

    def search_students(self, keyword):
        keyword = keyword.strip().lower()
        return [
            s for s in self.list_students()
            if keyword in " ".join(map(str, s.to_dict().values())).lower()
        ]

    def export_json(self, output_file):
        students = self.list_students()
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump([student.to_dict() for student in students], file, indent=2)
        logger.info("Exported %d students to %s", len(students), path)
        return path
