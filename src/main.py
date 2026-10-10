"""Command-line interface for the Student Information System."""
from pathlib import Path
import logging

from src.models.student import Student
from src.services.student_service import StudentService
from src.utils.config import load_config
from src.utils.logger import setup_logging

ROOT = Path(__file__).resolve().parent.parent


def ask_student(existing_id=None):
    print("Enter student information (fields cannot be blank).")
    student_id = input(f"Student ID [{existing_id or ''}]: ").strip()
    if not student_id and existing_id:
        student_id = existing_id
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    course = input("Course / Program: ").strip()
    year_text = input("Year level (1-6): ").strip()
    email = input("Email: ").strip()
    try:
        year_level = int(year_text)
    except ValueError as exc:
        raise ValueError("Year level must be a whole number.") from exc
    return Student(student_id, first_name, last_name, course, year_level, email)


def show_students(students):
    if not students:
        print("\nNo student records found.")
        return
    print("\n" + "-" * 94)
    print(f"{'ID':<12} {'NAME':<25} {'COURSE':<22} {'YEAR':<6} {'EMAIL':<27}")
    print("-" * 94)
    for s in students:
        print(f"{s.student_id:<12} {(s.first_name + ' ' + s.last_name):<25} "
              f"{s.course:<22} {s.year_level:<6} {s.email:<27}")
    print("-" * 94)


def main():
    config = load_config(ROOT / "config" / "config.json")
    setup_logging(ROOT / config["log_file"])
    service = StudentService(ROOT / config["data_file"], config["storage_format"])
    logger = logging.getLogger(__name__)

    while True:
        print("\n" + "=" * 42)
        print("       STUDENT INFORMATION SYSTEM")
        print("=" * 42)
        print("1. Add student")
        print("2. View all students")
        print("3. Update student")
        print("4. Delete student")
        print("5. Search students")
        print("6. Export records to JSON")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                student = ask_student()
                service.add_student(student)
                print("Student added successfully.")
            elif choice == "2":
                show_students(service.list_students())
            elif choice == "3":
                student_id = input("Enter the ID to update: ").strip()
                if not service.get_student(student_id):
                    print("Student ID was not found.")
                    continue
                updated = ask_student(student_id)
                service.update_student(student_id, updated)
                print("Student updated successfully.")
            elif choice == "4":
                student_id = input("Enter the ID to delete: ").strip()
                confirm = input(f"Delete student {student_id}? (y/n): ").strip().lower()
                if confirm == "y":
                    service.delete_student(student_id)
                    print("Student deleted successfully.")
                else:
                    print("Delete cancelled.")
            elif choice == "5":
                keyword = input("Search by ID, name, course, year, or email: ")
                show_students(service.search_students(keyword))
            elif choice == "6":
                output = ROOT / "data" / "students_export.json"
                service.export_json(output)
                print(f"Export saved to: {output.relative_to(ROOT)}")
            elif choice == "0":
                print("Thank you for using the Student Information System.")
                break
            else:
                print("Invalid option. Please choose one of the listed options.")
        except (ValueError, LookupError, OSError) as exc:
            logger.warning("Operation failed: %s", exc)
            print(f"Error: {exc}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception:
            logger.exception("Unexpected application error.")
            print("Something went wrong. Check logs/app.log for details.")


if __name__ == "__main__":
    main()
