import sys
import os
import unittest
import tempfile
import shutil

# Add the project directory to sys.path so we can import modules
sys.path.append(r"C:\Users\HP\.gemini\antigravity\scratch\student_performance_analytics")

from utils.helpers import (
    custom_sort,
    validate_student_id,
    validate_name,
    validate_class_section,
    validate_subject,
    validate_mark,
    generate_ai_insights
)
from models.student import Student, DatabaseManager
from analytics.performance import Analytics

class TestHelpers(unittest.TestCase):
    """Tests for helpers.py containing custom stable Merge Sort, validators, and AI Insights."""
    
    def test_custom_sort_ascending(self):
        data = [5, 3, 8, 2, 1, 9]
        self.assertEqual(custom_sort(data), [1, 2, 3, 5, 8, 9])
        
    def test_custom_sort_descending(self):
        data = [5, 3, 8, 2, 1, 9]
        self.assertEqual(custom_sort(data, reverse=True), [9, 8, 5, 3, 2, 1])
        
    def test_custom_sort_key_func(self):
        data = ["apple", "banana", "kiwi", "fig"]
        # Sort by string length
        self.assertEqual(custom_sort(data, key_func=len), ["fig", "kiwi", "apple", "banana"])
        
    def test_custom_sort_stability(self):
        """
        Verifies that custom_sort is a stable sorting algorithm.
        Elements with equal keys must maintain their original relative order.
        """
        # List of tuples: (name, priority)
        # We will sort by priority (index 1) in ascending order
        data = [("Alice", 2), ("Bob", 1), ("Charlie", 2), ("David", 1), ("Eve", 3)]
        sorted_data = custom_sort(data, key_func=lambda x: x[1])
        
        # Expected stable output:
        # Priority 1: Bob, then David (Bob comes first in original list)
        # Priority 2: Alice, then Charlie (Alice comes first in original list)
        # Priority 3: Eve
        expected = [("Bob", 1), ("David", 1), ("Alice", 2), ("Charlie", 2), ("Eve", 3)]
        self.assertEqual(sorted_data, expected)

    def test_validators(self):
        # Student ID Validation
        self.assertTrue(validate_student_id("STD-1234"))
        self.assertTrue(validate_student_id("std-0001"))
        self.assertFalse(validate_student_id("STD-123"))
        self.assertFalse(validate_student_id("ST-12345"))
        self.assertFalse(validate_student_id(""))
        
        # Name Validation
        self.assertTrue(validate_name("John Doe"))
        self.assertTrue(validate_name("O'Connor"))
        self.assertTrue(validate_name("Anne-Marie"))
        self.assertFalse(validate_name("John123"))
        self.assertFalse(validate_name("J"))  # too short
        
        # Class Section Validation
        self.assertTrue(validate_class_section("10-A"))
        self.assertTrue(validate_class_section("1-Z"))
        self.assertTrue(validate_class_section("12-C"))
        self.assertFalse(validate_class_section("0-A"))
        self.assertFalse(validate_class_section("13-B"))
        self.assertFalse(validate_class_section("10A"))
        
        # Subject Validation
        self.assertTrue(validate_subject("Mathematics"))
        self.assertTrue(validate_subject("Computer Science"))
        self.assertTrue(validate_subject("C++ Programming"))
        self.assertFalse(validate_subject("M"))  # too short
        
        # Mark Validation
        self.assertTrue(validate_mark(95))
        self.assertTrue(validate_mark(0))
        self.assertTrue(validate_mark(100.0))
        self.assertFalse(validate_mark(-5))
        self.assertFalse(validate_mark(105))
        self.assertFalse(validate_mark("abc"))

    def test_ai_insights(self):
        marks = {"Math": 90, "Science": 45, "English": 75}
        insights = generate_ai_insights(marks)
        
        self.assertIn("Math", insights["strengths"])
        self.assertIn("Science", insights["weak_areas"])
        self.assertIn("English", insights["scope_for_improvement"])
        self.assertEqual(insights["academic_risk"], "MEDIUM RISK")
        self.assertTrue(len(insights["suggestions"]) > 0)


class TestStudentModel(unittest.TestCase):
    """Tests for Student class validation and calculations."""
    
    def test_student_calculations(self):
        s = Student(student_id="STD-0001", name="Alice Smith", class_section="10-A")
        s.add_subject_mark("Math", 90.0)
        s.add_subject_mark("English", 80.0)
        s.add_subject_mark("Science", 70.0)
        
        self.assertEqual(s.get_total_marks(), 240.0)
        self.assertEqual(s.get_average_mark(), 80.0)
        self.assertEqual(s.get_percentage(), 80.0)
        self.assertEqual(s.get_grade(), "A")
        self.assertEqual(s.get_status(), "PASS")
        
        # Add a failing mark
        s.add_subject_mark("History", 35.0)
        self.assertEqual(s.get_status(), "FAIL")  # should fail because of History < 40
        
        # Serialization checks
        s_dict = s.to_dict()
        self.assertEqual(s_dict["student_id"], "STD-0001")
        
        s_loaded = Student.from_dict(s_dict)
        self.assertEqual(s_loaded.name, "Alice Smith")
        self.assertEqual(s_loaded.marks["Math"], 90.0)


class TestDatabaseManager(unittest.TestCase):
    """Tests for DatabaseManager persistence, backups, and search."""
    
    def setUp(self):
        # Set up a temporary directory and file for database tests
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "students_test.json")
        
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)
        
    def test_database_persistence_and_search(self):
        db = DatabaseManager(self.db_path)
        
        # Verify db is empty
        self.assertEqual(len(db.get_all_students()), 0)
        
        # Add students
        s1 = Student("STD-0001", "Bob Johnson", "11-B", {"Math": 85})
        s2 = Student("STD-0002", "Jane Doe", "11-A", {"Math": 95, "History": 72})
        db.add_student(s1)
        db.add_student(s2)
        
        # Verify additions
        self.assertEqual(len(db.get_all_students()), 2)
        
        # Re-initialize DB from file and verify persistence
        db2 = DatabaseManager(self.db_path)
        self.assertEqual(len(db2.get_all_students()), 2)
        self.assertIsNotNone(db2.get_student("STD-0001"))
        self.assertEqual(db2.get_student("STD-0002").name, "Jane Doe")
        
        # Test Search
        results = db2.search_students("jane")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].student_id, "STD-0002")
        
        # Test Delete
        db2.delete_student("STD-0001")
        self.assertEqual(len(db2.get_all_students()), 1)
        self.assertIsNone(db2.get_student("STD-0001"))


class TestAnalytics(unittest.TestCase):
    """Tests for class-wide and subject-wide analytics aggregates."""
    
    def test_analytics_formulas(self):
        s1 = Student("STD-0001", "Bob Johnson", "11-B", {"Math": 80, "English": 70})
        s2 = Student("STD-0002", "Jane Doe", "11-A", {"Math": 90, "History": 80})
        s3 = Student("STD-0003", "Alice Smith", "11-B", {"Math": 70, "English": 90})
        
        students = [s1, s2, s3]
        
        # Class average
        # s1: 75.0, s2: 85.0, s3: 80.0 -> class avg: (75 + 85 + 80) / 3 = 80.0
        self.assertEqual(Analytics.get_class_average(students), 80.0)
        
        # High and low scorers
        self.assertEqual(Analytics.get_class_highest_scorer(students).student_id, "STD-0002")
        self.assertEqual(Analytics.get_class_lowest_scorer(students).student_id, "STD-0001")
        
        # Subject stats
        sub_stats = Analytics.get_subject_statistics(students)
        self.assertIn("Math", sub_stats)
        self.assertEqual(sub_stats["Math"]["average"], 80.0)
        self.assertEqual(sub_stats["Math"]["highest"], 90.0)
        self.assertEqual(sub_stats["Math"]["lowest"], 70.0)
        self.assertEqual(sub_stats["Math"]["count"], 3)


if __name__ == "__main__":
    unittest.main()
