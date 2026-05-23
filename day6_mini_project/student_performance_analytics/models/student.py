import os
import json
import logging
import shutil
from typing import Dict, List, Optional, Any

from utils.helpers import (
    validate_student_id,
    validate_name,
    validate_class_section,
    validate_subject,
    validate_mark
)

logger = logging.getLogger(__name__)

class Student:
    """
    Represents an individual student's academic record, providing encapsulation
    of grades, statuses, and performance calculations.
    """

    def __init__(self, student_id: str, name: str, class_section: str, marks: Optional[Dict[str, float]] = None):
        # Validate properties on initialization
        if not validate_student_id(student_id):
            raise ValueError(f"Invalid Student ID format: {student_id}. Should be STD-XXXX (e.g. STD-0042).")
        if not validate_name(name):
            raise ValueError(f"Invalid Name: {name}. Must be 2-50 letters/spaces.")
        if not validate_class_section(class_section):
            raise ValueError(f"Invalid Class/Section: {class_section}. Format: Class-Section (e.g., 10-A, 12-F).")
        
        self._student_id = student_id.strip().upper()
        self.name = name.strip()
        self.class_section = class_section.strip().upper()
        self.marks = {}
        
        if marks:
            for sub, score in marks.items():
                self.add_subject_mark(sub, score)

    @property
    def student_id(self) -> str:
        """Read-only property for Student ID."""
        return self._student_id

    def add_subject_mark(self, subject: str, mark: float) -> None:
        """Adds a subject and its mark to the student's records after validation."""
        sub_cleaned = subject.strip()
        if not validate_subject(sub_cleaned):
            raise ValueError(f"Invalid subject name: '{sub_cleaned}'. Must be 2-30 alphanumeric characters/spaces.")
        if not validate_mark(mark):
            raise ValueError(f"Invalid mark value: {mark}. Must be between 0 and 100.")
        self.marks[sub_cleaned] = float(mark)

    def update_mark(self, subject: str, mark: float) -> None:
        """Updates the mark for an existing subject."""
        sub_cleaned = subject.strip()
        if sub_cleaned not in self.marks:
            raise KeyError(f"Subject '{sub_cleaned}' does not exist for this student. Use add_subject_mark.")
        if not validate_mark(mark):
            raise ValueError(f"Invalid mark value: {mark}. Must be between 0 and 100.")
        self.marks[sub_cleaned] = float(mark)

    def remove_subject(self, subject: str) -> None:
        """Removes a subject from the student's records."""
        sub_cleaned = subject.strip()
        if sub_cleaned in self.marks:
            del self.marks[sub_cleaned]
        else:
            raise KeyError(f"Subject '{sub_cleaned}' not found.")

    def get_total_marks(self) -> float:
        """Calculates total marks scored across all subjects."""
        return sum(self.marks.values())

    def get_average_mark(self) -> float:
        """Calculates the average mark scored."""
        if not self.marks:
            return 0.0
        return self.get_total_marks() / len(self.marks)

    def get_percentage(self) -> float:
        """
        Calculates student percentage. Since each subject is graded out of 100,
        the percentage is equivalent to the average mark.
        """
        return self.get_average_mark()

    def get_grade(self) -> str:
        """
        Calculates letter grade based on percentage:
        A+: >= 90
        A : >= 80 and < 90
        B : >= 70 and < 80
        C : >= 60 and < 70
        D : >= 50 and < 60
        E : >= 40 and < 50
        F : < 40 (Fail)
        """
        pct = self.get_percentage()
        if not self.marks:
            return "N/A"
        if pct >= 90.0:
            return "A+"
        elif pct >= 80.0:
            return "A"
        elif pct >= 70.0:
            return "B"
        elif pct >= 60.0:
            return "C"
        elif pct >= 50.0:
            return "D"
        elif pct >= 40.0:
            return "E"
        else:
            return "F"

    def get_status(self) -> str:
        """
        Determines student status.
        PASS: Overall percentage >= 40.0 AND all subject marks >= 40.0
        FAIL: Overall percentage < 40.0 OR any subject mark < 40.0
        """
        if not self.marks:
            return "NO MARKS"
        pct = self.get_percentage()
        if pct < 40.0:
            return "FAIL"
        for sub, score in self.marks.items():
            if score < 40.0:
                return "FAIL"
        return "PASS"

    def to_dict(self) -> Dict[str, Any]:
        """Serializes Student object data to a dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_section": self.class_section,
            "marks": self.marks
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Factory method to instantiate a Student object from a dictionary."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            class_section=data["class_section"],
            marks=data.get("marks", {})
        )

    def __repr__(self) -> str:
        return f"Student({self.student_id}, {self.name}, {self.class_section}, Marks: {len(self.marks)})"


class DatabaseManager:
    """
    Handles student records persistence using a local JSON file.
    Supports transactional backups and data recovery upon file corruption.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.backup_filepath = filepath + ".bak"
        self.students: Dict[str, Student] = {}
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        self.load_data()

    def load_data(self) -> None:
        """
        Loads student records from the JSON database file.
        Recovers from a backup file if the primary file is missing, corrupt, or empty.
        """
        self.students = {}
        data_loaded = False
        
        # 1. Try reading the primary file
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    self._parse_raw_data(raw_data)
                data_loaded = True
                logger.info("Database loaded successfully from primary file.")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"Primary database corrupt or invalid: {e}. Attempting recovery from backup.")
        
        # 2. Try reading from the backup if primary failed
        if not data_loaded and os.path.exists(self.backup_filepath) and os.path.getsize(self.backup_filepath) > 0:
            try:
                with open(self.backup_filepath, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    self._parse_raw_data(raw_data)
                data_loaded = True
                # Recover primary from backup
                shutil.copy(self.backup_filepath, self.filepath)
                logger.info("Database successfully recovered from backup file.")
            except Exception as e:
                logger.critical(f"Backup file recovery failed: {e}. Initializing empty database.")
                
        # 3. If neither worked, initialize an empty file
        if not data_loaded:
            logger.info("No existing valid database found. Initializing new database file.")
            self.save_data()

    def _parse_raw_data(self, raw_data: Any) -> None:
        """Parses raw list of dicts from JSON and populates the local dictionary."""
        if not isinstance(raw_data, list):
            raise ValueError("Invalid database format: Root element must be a list of student records.")
        for item in raw_data:
            student = Student.from_dict(item)
            self.students[student.student_id] = student

    def save_data(self) -> None:
        """
        Saves the current student records to the JSON file.
        Creates a backup of the current database before overwriting to ensure resilience.
        """
        try:
            # 1. Create a backup of the current valid file if it exists and has content
            if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
                try:
                    shutil.copy(self.filepath, self.backup_filepath)
                except Exception as e:
                    logger.warning(f"Failed to write backup database file: {e}")
            
            # 2. Write new data to primary file
            raw_list = [student.to_dict() for student in self.students.values()]
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(raw_list, f, indent=4, ensure_ascii=False)
            logger.info("Database saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save database: {e}")
            raise IOError(f"Could not save database: {e}")

    def add_student(self, student: Student) -> None:
        """Adds a student record to the database and persists it."""
        if student.student_id in self.students:
            raise KeyError(f"Student ID '{student.student_id}' already exists in the database.")
        self.students[student.student_id] = student
        self.save_data()

    def delete_student(self, student_id: str) -> None:
        """Deletes a student record by ID and persists changes."""
        clean_id = student_id.strip().upper()
        if clean_id not in self.students:
            raise KeyError(f"Student ID '{clean_id}' not found.")
        del self.students[clean_id]
        self.save_data()

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieves a student object by ID. Returns None if not found."""
        return self.students.get(student_id.strip().upper())

    def get_all_students(self) -> List[Student]:
        """Returns a list of all Student objects currently stored."""
        return list(self.students.values())

    def search_students(self, query: str, search_by: str = "name") -> List[Student]:
        """
        Searches students based on a query parameter.
        
        Args:
            query: The search term
            search_by: Fields to search - 'name', 'id', 'class', or 'any'
            
        Returns:
            List of matching Student objects.
        """
        clean_query = query.strip().lower()
        if not clean_query:
            return self.get_all_students()
            
        results = []
        for s in self.students.values():
            match = False
            if search_by == "name" and clean_query in s.name.lower():
                match = True
            elif search_by == "id" and clean_query in s.student_id.lower():
                match = True
            elif search_by == "class" and clean_query in s.class_section.lower():
                match = True
            elif search_by == "any":
                if (clean_query in s.name.lower() or 
                    clean_query in s.student_id.lower() or 
                    clean_query in s.class_section.lower()):
                    match = True
            if match:
                results.append(s)
        return results
