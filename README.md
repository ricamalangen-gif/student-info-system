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

No third-party Python packages are required.

## Run the application

Open a terminal in the project folder and run:

```bash
python -m src.main
```

Choose an option from the menu and follow the prompts. The initial JSON file contains sample records that you can edit or delete while testing.

## Choose JSON or XML storage

The default configuration is in `config/config.json`:

```json
{
  "storage_format": "json",
  "data_file": "data/students.json",
  "log_file": "logs/app.log"
}
```

To use XML, change `storage_format` to `xml` and change `data_file` to `data/students.xml`. The application will create the XML data file if it does not exist. JSON is the default.

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

## GitHub workflow suggestion

Use small commits with messages that describe the change. Example:

```bash
git init
git add .
git commit -m "Set up project structure and configuration"
git branch feature/student-crud
git checkout feature/student-crud
git add src data
git commit -m "Implement student CRUD and JSON persistence"
git checkout main
git merge feature/student-crud
git add .
git commit -m "Add validation, search, export, logging, and tests"
```
