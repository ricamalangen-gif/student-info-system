"""Student model and input validation."""
from dataclasses import dataclass, asdict


@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    course: str
    year_level: int
    email: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=str(data["student_id"]).strip(),
            first_name=str(data["first_name"]).strip(),
            last_name=str(data["last_name"]).strip(),
            course=str(data["course"]).strip(),
            year_level=int(data["year_level"]),
            email=str(data["email"]).strip(),
        )

    def validate(self):
        required = {
            "Student ID": self.student_id,
            "First name": self.first_name,
            "Last name": self.last_name,
            "Course": self.course,
            "Email": self.email,
        }
        missing = [label for label, value in required.items() if not value]
        if missing:
            raise ValueError("Required field(s) missing: " + ", ".join(missing))
        if self.year_level not in (1, 2, 3, 4, 5, 6):
            raise ValueError("Year level must be between 1 and 6.")
        if "@" not in self.email or "." not in self.email.rsplit("@", 1)[-1]:
            raise ValueError("Please enter a valid email address.")
