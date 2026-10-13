# Student Information System

A simple Python command-line application for managing student records. It was built for the Midterm Lab Exam on Student Information System with GitHub Integration.

## Features

- Add, view, update, and delete student records (CRUD).
- Store records locally in JSON or XML format.
- Search records by student ID, name, course, year level, or email.
- Export the records to a separate JSON file.
- Validate required fields, email format, year level, and duplicate IDs.
- Keep a log of application activity and errors.
- Use an external JSON configuration file.
- Include unit tests for the main data operations.

## Requirements

- Python 3.10 or later
- Git and a GitHub account (for version control)

## Run the application

Open a terminal in the project folder and run:

```bash
python -m src.main
```

## Choose JSON or XML storage

The default configuration is in `config/config.json`:

```json
{
  "storage_format": "json",
  "data_file": "data/students.json",
  "log_file": "logs/app.log"
}
```

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
student-info-system/
├── src/
│   ├── models/student.py
│   ├── services/student_service.py
│   ├── utils/config.py
│   ├── utils/logger.py
│   └── main.py
├── data/students.json
├── config/config.json
├── logs/
├── tests/test_student_service.py
├── README.md
├── requirements.txt
└── .gitignore
```
