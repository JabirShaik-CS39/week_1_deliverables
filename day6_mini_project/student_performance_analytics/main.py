import os
import sys
import logging
from typing import Dict, List, Any

# Ensure current directory is in the path to import custom modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.student import Student, DatabaseManager
from analytics.performance import Analytics, ReportGenerator
from utils.helpers import (
    custom_sort,
    get_string_input,
    get_int_input,
    get_float_input,
    get_choice_input,
    validate_student_id,
    validate_name,
    validate_class_section,
    validate_subject,
    validate_mark
)

# Initialize project directories
os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Set up logging configuration
logging.basicConfig(
    filename=os.path.join("logs", "app.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("main")

# Database File Path
DB_FILE = os.path.join("data", "students.json")

def print_header():
    """Prints a premium visual terminal header."""
    print("═" * 73)
    print("║" + " " * 71 + "║")
    print(f"║ {'🎓  STUDENT ACADEMIC PERFORMANCE ANALYTICS':^67} ║")
    print("║" + " " * 71 + "║")
    print("═" * 73)


def add_student_flow(db: DatabaseManager):
    """CLI flow to add a new student and their subject marks."""
    print("\n--- 📝 ADD NEW STUDENT RECORD ---")
    
    # Prompt for Student ID
    def id_check(x):
        return validate_student_id(x) and db.get_student(x) is None
    
    student_id = get_string_input(
        prompt="Enter Student ID (Format: STD-XXXX, e.g. STD-0042): ",
        validator=id_check,
        error_msg="Invalid Student ID format or ID already exists in database."
    ).upper()
    
    # Prompt for Name
    name = get_string_input(
        prompt="Enter Student Full Name (2-50 chars): ",
        validator=validate_name,
        error_msg="Invalid name. Must contain only letters and spaces."
    )
    
    # Prompt for Class-Section
    class_sec = get_string_input(
        prompt="Enter Class & Section (Format: Class-Section, e.g. 10-A, 12-F): ",
        validator=validate_class_section,
        error_msg="Invalid class/section format. Must be between class 1-12 and section A-Z (e.g. 9-B)."
    ).upper()
    
    # Initialize Student
    student = Student(student_id=student_id, name=name, class_section=class_sec)
    
    # Prompt to add subject marks
    print("\nAdd academic marks for this student:")
    while True:
        sub_name = input("Enter Subject Name (or press Enter to finish adding): ").strip()
        if not sub_name:
            if not student.marks:
                print("Warning: Student must have at least one subject to record marks. Please add a subject.")
                continue
            break
            
        if not validate_subject(sub_name):
            print("Error: Subject must be 2-30 alphanumeric characters/spaces.")
            continue
            
        if sub_name in student.marks:
            print(f"Error: Subject '{sub_name}' already exists. Use the Update menu to edit marks.")
            continue
            
        mark_val = get_float_input(
            prompt=f"Enter Marks for {sub_name} (0.0 to 100.0): ",
            min_val=0.0,
            max_val=100.0
        )
        
        student.add_subject_mark(sub_name, mark_val)
        print(f"Added: {sub_name} -> {mark_val:.2f}")
        
    db.add_student(student)
    print(f"\n[+] Success: Student '{name}' ({student_id}) recorded successfully!")
    logger.info(f"Added student: {student_id} - {name}")


def view_students_flow(db: DatabaseManager):
    """CLI flow to view, search, and list students in a structured table."""
    print("\n--- 🔍 VIEW & SEARCH STUDENT RECORDS ---")
    students = db.get_all_students()
    
    if not students:
        print("[!] No records found in the database. Please add a student first.")
        return
        
    print("Filter options:")
    print("1. View All Students")
    print("2. Search by Name")
    print("3. Search by Student ID")
    print("4. Search by Class-Section")
    
    choice = get_int_input("Select filter option (1-4): ", min_val=1, max_val=4)
    
    results = []
    if choice == 1:
        results = students
    elif choice == 2:
        query = get_string_input("Enter search query (Name): ")
        results = db.search_students(query, search_by="name")
    elif choice == 3:
        query = get_string_input("Enter search query (Student ID): ")
        results = db.search_students(query, search_by="id")
    elif choice == 4:
        query = get_string_input("Enter search query (Class-Section): ")
        results = db.search_students(query, search_by="class")
        
    if not results:
        print("\n[!] No students matched your search criteria.\n")
        return
        
    # Render search table
    print("\n" + "─" * 75)
    print(f"{'ID':<10} │ {'Student Name':<25} │ {'Class':<8} │ {'Subjects':^8} │ {'Avg %':^10} │ {'Status':^8}")
    print("─" * 75)
    
    # Sort results by ID for clean viewing
    sorted_results = custom_sort(results, key_func=lambda s: s.student_id)
    for s in sorted_results:
        num_subs = len(s.marks)
        avg = s.get_percentage()
        status = s.get_status()
        print(f"{s.student_id:<10} │ {s.name:<25} │ {s.class_section:<8} │ {num_subs:^8} │ {avg:^10.2f} │ {status:^8}")
    print("─" * 75 + f"\nTotal Records: {len(sorted_results)}\n")


def update_marks_flow(db: DatabaseManager):
    """CLI flow to edit, add, or delete marks from a student record."""
    print("\n--- ✏️ UPDATE STUDENT MARKS ---")
    student_id = get_string_input("Enter Student ID to update (e.g. STD-0042): ").upper()
    student = db.get_student(student_id)
    
    if not student:
        print(f"[!] Error: Student ID '{student_id}' not found.")
        return
        
    print(f"\nStudent Details: {student.name} (Class {student.class_section})")
    print("Current Academic Marks:")
    if not student.marks:
        print("  (No marks recorded)")
    else:
        for sub, val in student.marks.items():
            print(f"  • {sub}: {val:.2f}")
            
    print("\nSelect Operation:")
    print("1. Add a new subject mark")
    print("2. Edit an existing subject mark")
    print("3. Delete a subject")
    print("4. Go back")
    
    choice = get_int_input("Choose option (1-4): ", min_val=1, max_val=4)
    
    if choice == 1:
        sub_name = get_string_input(
            prompt="Enter New Subject Name: ",
            validator=validate_subject,
            error_msg="Invalid subject. Must be 2-30 alphanumeric characters/spaces."
        )
        if sub_name in student.marks:
            print(f"Error: Subject '{sub_name}' already exists. Select 'Edit' to change mark.")
            return
            
        mark_val = get_float_input(f"Enter Marks for {sub_name} (0-100): ", min_val=0.0, max_val=100.0)
        student.add_subject_mark(sub_name, mark_val)
        db.save_data()
        print(f"[+] Added subject {sub_name} with mark {mark_val:.2f}")
        logger.info(f"Student {student_id}: Added subject {sub_name} ({mark_val})")
        
    elif choice == 2:
        if not student.marks:
            print("Error: No subjects recorded. Add a subject first.")
            return
        sub_name = get_string_input("Enter subject name to edit: ")
        if sub_name not in student.marks:
            print(f"Error: Subject '{sub_name}' not found.")
            return
            
        mark_val = get_float_input(f"Enter New Marks for {sub_name} (0-100): ", min_val=0.0, max_val=100.0)
        student.update_mark(sub_name, mark_val)
        db.save_data()
        print(f"[+] Updated subject {sub_name} mark to {mark_val:.2f}")
        logger.info(f"Student {student_id}: Updated subject {sub_name} ({mark_val})")
        
    elif choice == 3:
        if not student.marks:
            print("Error: No subjects recorded.")
            return
        sub_name = get_string_input("Enter subject name to delete: ")
        try:
            student.remove_subject(sub_name)
            db.save_data()
            print(f"[+] Subject '{sub_name}' deleted successfully.")
            logger.info(f"Student {student_id}: Deleted subject {sub_name}")
        except KeyError:
            print(f"Error: Subject '{sub_name}' not found.")
            
    elif choice == 4:
        return


def delete_student_flow(db: DatabaseManager):
    """CLI flow to delete a student record with confirmation."""
    print("\n--- 🗑️ DELETE STUDENT RECORD ---")
    student_id = get_string_input("Enter Student ID to delete: ").upper()
    student = db.get_student(student_id)
    
    if not student:
        print(f"[!] Error: Student ID '{student_id}' not found.")
        return
        
    print(f"\nCRITICAL: You are about to permanently delete the academic profile of:")
    print(f"  Name: {student.name}")
    print(f"  ID: {student.student_id}")
    print(f"  Class: {student.class_section}")
    print(f"  Total Subjects: {len(student.marks)}")
    
    confirm = get_choice_input("Are you absolutely sure you want to delete this record? (Yes/No): ", ["Yes", "No"])
    
    if confirm == "Yes":
        db.delete_student(student_id)
        print(f"\n[-] Success: Student record '{student_id}' deleted successfully.")
        logger.info(f"Deleted student: {student_id} - {student.name}")
    else:
        print("\nOperation cancelled. Student record preserved.")


def generate_reports_flow(db: DatabaseManager):
    """CLI flow to generate CLI report cards, text outputs, and CSV database summaries."""
    print("\n--- 📄 REPORT GENERATOR SERVICE ---")
    student_id = get_string_input("Enter Student ID for Academic Report Card: ").upper()
    student = db.get_student(student_id)
    
    if not student:
        print(f"[!] Error: Student ID '{student_id}' not found.")
        return
        
    # Render CLI report card
    ReportGenerator.print_student_report_card(student)
    
    print("Export Options:")
    print("1. Save this Report Card to a Text File")
    print("2. Export All Database Student Records to CSV")
    print("3. Export Both (Report card & CSV summary)")
    print("4. Return to main menu")
    
    choice = get_int_input("Choose export option (1-4): ", min_val=1, max_val=4)
    
    if choice in [1, 3]:
        # Save Report Card as TXT file
        filepath = os.path.join("reports", f"report_card_{student.student_id}.txt")
        try:
            # Capture report card string by redirecting standard output temporarily
            import io
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            ReportGenerator.print_student_report_card(student)
            card_content = new_stdout.getvalue()
            sys.stdout = old_stdout
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(card_content)
                
            print(f"[+] Success: Report Card saved to: {os.path.abspath(filepath)}")
            logger.info(f"Exported Report Card TXT for: {student.student_id}")
        except Exception as e:
            print(f"Error saving report card text file: {e}")
            
    if choice in [2, 3]:
        # Export all to CSV
        filepath = os.path.join("reports", "student_summary.csv")
        try:
            ReportGenerator.export_students_to_csv(db.get_all_students(), filepath)
            print(f"[+] Success: Student Database exported to CSV: {os.path.abspath(filepath)}")
            logger.info("Exported database CSV report summary.")
        except Exception as e:
            print(f"Error exporting CSV: {e}")


def rankings_flow(db: DatabaseManager):
    """CLI flow to view rankings and leaderboards."""
    print("\n--- 🏆 LEADERBOARD & RANKINGS ---")
    students = db.get_all_students()
    
    if not students:
        print("[!] No students registered in the system database.")
        return
        
    print("Rank by Criteria:")
    print("1. Rank by Overall Academic Percentage (Highest to Lowest)")
    print("2. Rank by Overall Cumulative Marks")
    print("3. Rank by Subject Specific Score")
    print("4. View Bottom Performers (Ascending Academic Percentage)")
    
    choice = get_int_input("Select ranking criteria (1-4): ", min_val=1, max_val=4)
    
    ranked = []
    title = ""
    
    if choice == 1:
        ranked = Analytics.get_rankings(students, criteria="percentage")
        title = "LEADERBOARD (OVERALL PERCENTAGE)"
    elif choice == 2:
        ranked = Analytics.get_rankings(students, criteria="total_marks")
        title = "LEADERBOARD (CUMULATIVE MARKS)"
    elif choice == 3:
        sub_name = get_string_input("Enter Subject Name to rank by: ")
        ranked = Analytics.get_rankings(students, criteria="subject", subject=sub_name)
        title = f"LEADERBOARD (SUBJECT: {sub_name.upper()})"
    elif choice == 4:
        # Ascending order
        ranked = Analytics.get_rankings(students, criteria="percentage")
        ranked.reverse()  # Reverse descending to get ascending
        title = "ACADEMIC INTERVENTION LIST (BOTTOM PERFORMERS)"
        
    print("\n" + "═" * 70)
    print(f"║ {title:^68} ║")
    print("╠" + "═" * 70 + "╣")
    
    if choice == 3:
        print(f"║ {'Rank':^6} │ {'ID':<10} │ {'Name':<22} │ {'Class':<8} │ {'Subject Mark':^12} ║")
        print("╟" + "─" * 6 + "┼" + "─" * 10 + "┼" + "─" * 22 + "┼" + "─" * 8 + "┼" + "─" * 12 + "╢")
        for i, s in enumerate(ranked):
            sub_mark = s.marks.get(sub_name, 0.0)
            print(f"║ {i+1:^6} │ {s.student_id:<10} │ {s.name:<22} │ {s.class_section:<8} │ {sub_mark:^12.2f} ║")
    elif choice == 2:
        print(f"║ {'Rank':^6} │ {'ID':<10} │ {'Name':<22} │ {'Class':<8} │ {'Total Marks':^12} ║")
        print("╟" + "─" * 6 + "┼" + "─" * 10 + "┼" + "─" * 22 + "┼" + "─" * 8 + "┼" + "─" * 12 + "╢")
        for i, s in enumerate(ranked):
            print(f"║ {i+1:^6} │ {s.student_id:<10} │ {s.name:<22} │ {s.class_section:<8} │ {s.get_total_marks():^12.2f} ║")
    else:
        print(f"║ {'Rank':^6} │ {'ID':<10} │ {'Name':<22} │ {'Class':<8} │ {'Percentage':^12} ║")
        print("╟" + "─" * 6 + "┼" + "─" * 10 + "┼" + "─" * 22 + "┼" + "─" * 8 + "┼" + "─" * 12 + "╢")
        for i, s in enumerate(ranked):
            print(f"║ {i+1:^6} │ {s.student_id:<10} │ {s.name:<22} │ {s.class_section:<8} │ {s.get_percentage():^12.2f}% ║")
            
    print("╚" + "═" * 70 + "╝\n")


def analytics_flow(db: DatabaseManager):
    """CLI flow to view class analytics and generate matplotlib charts."""
    print("\n--- 📈 ANALYTICS & VISUALIZATIONS ---")
    students = db.get_all_students()
    
    if not students:
        print("[!] No students registered in the system database.")
        return
        
    # Render ASCII Summary Dashboard
    ReportGenerator.print_class_summary_report(students, Analytics)
    
    generate_charts = get_choice_input(
        prompt="Would you like to generate and save visual graphical charts (PNG format)? (Yes/No): ",
        choices=["Yes", "No"]
    )
    
    if generate_charts == "Yes":
        print("\n[~] Generating Matplotlib visualization charts...")
        try:
            paths = ReportGenerator.generate_performance_charts(students, "charts")
            print("\n[+] Success! Visual assets generated and saved successfully:")
            for p in paths:
                print(f"  • {os.path.abspath(p)}")
            logger.info("Saved data visualization charts to charts/ directory.")
        except Exception as e:
            print(f"Error generating charts: {e}")
            logger.error(f"Failed to generate charts: {e}")


def main():
    """Main terminal application loop."""
    db = DatabaseManager(DB_FILE)
    logger.info("Application initialized successfully.")
    
    while True:
        try:
            print_header()
            print("1. Add Student Record")
            print("2. View & Search Student Records")
            print("3. Update Student Marks")
            print("4. Delete Student Record")
            print("5. Generate CLI Report Cards & Export Reports")
            print("6. View Rankings & Leaderboard")
            print("7. Class Analytics Dashboard & Save Charts")
            print("8. Save and Exit Application")
            print("═" * 73)
            
            choice = get_int_input("Select operation (1-8): ", min_val=1, max_val=8)
            
            if choice == 1:
                add_student_flow(db)
            elif choice == 2:
                view_students_flow(db)
            elif choice == 3:
                update_marks_flow(db)
            elif choice == 4:
                delete_student_flow(db)
            elif choice == 5:
                generate_reports_flow(db)
            elif choice == 6:
                rankings_flow(db)
            elif choice == 7:
                analytics_flow(db)
            elif choice == 8:
                print("\nSaving database changes... Thank you for using Student Performance Analytics!\n")
                db.save_data()
                logger.info("Application closed successfully.")
                break
                
            input("\nPress Enter to return to main menu...")
            
        except KeyboardInterrupt:
            print("\n\n[!] Force Exit detected. Saving student data changes...")
            db.save_data()
            logger.info("Application closed by keyboard interrupt.")
            break
        except Exception as e:
            print(f"\n[CRITICAL ERROR] An unexpected error occurred: {e}")
            print("Please see logs/app.log for full trace details.")
            logger.exception("An unhandled exception occurred in the CLI loop:")
            input("\nPress Enter to reload menu...")

if __name__ == "__main__":
    main()
