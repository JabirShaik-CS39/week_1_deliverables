import os
import csv
import logging
from typing import List, Dict, Any, Optional

import matplotlib
# Use a non-interactive backend to prevent GUI/Tkinter errors in automated CLI environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from models.student import Student
from utils.helpers import custom_sort, generate_ai_insights

logger = logging.getLogger(__name__)

class Analytics:
    """
    Computes class-level and subject-level academic performance statistics.
    """

    @staticmethod
    def get_class_average(students: List[Student]) -> float:
        """Calculates the average percentage score across all students."""
        if not students:
            return 0.0
        return sum(s.get_percentage() for s in students) / len(students)

    @staticmethod
    def get_class_highest_scorer(students: List[Student]) -> Optional[Student]:
        """Returns the student with the highest overall percentage score."""
        if not students:
            return None
        # Rank students using our custom_sort in descending order
        ranked = custom_sort(students, key_func=lambda s: s.get_percentage(), reverse=True)
        return ranked[0]

    @staticmethod
    def get_class_lowest_scorer(students: List[Student]) -> Optional[Student]:
        """Returns the student with the lowest overall percentage score."""
        if not students:
            return None
        # Rank students using our custom_sort in ascending order
        ranked = custom_sort(students, key_func=lambda s: s.get_percentage(), reverse=False)
        return ranked[0]

    @staticmethod
    def get_subject_statistics(students: List[Student]) -> Dict[str, Dict[str, Any]]:
        """
        Computes detailed statistics for every subject present in the database.
        
        Returns:
            Dict containing subject names as keys, and a dict of stats as values:
            {
                "Subject": {
                    "average": float,
                    "highest": float,
                    "highest_toppers": List[str],
                    "lowest": float,
                    "lowest_students": List[str],
                    "count": int
                }
            }
        """
        subject_data: Dict[str, List[Dict[str, Any]]] = {}
        
        # Collect all student scores by subject
        for s in students:
            for sub, mark in s.marks.items():
                if sub not in subject_data:
                    subject_data[sub] = []
                subject_data[sub].append({"student": s, "score": mark})
                
        stats: Dict[str, Dict[str, Any]] = {}
        for sub, records in subject_data.items():
            scores = [r["score"] for r in records]
            avg = sum(scores) / len(scores)
            
            # Find high and low scores
            highest = max(scores)
            lowest = min(scores)
            
            # Find who scored high and low
            highest_toppers = [f"{r['student'].name} ({r['student'].student_id})" for r in records if r["score"] == highest]
            lowest_students = [f"{r['student'].name} ({r['student'].student_id})" for r in records if r["score"] == lowest]
            
            stats[sub] = {
                "average": round(avg, 2),
                "highest": highest,
                "highest_toppers": highest_toppers,
                "lowest": lowest,
                "lowest_students": lowest_students,
                "count": len(scores)
            }
            
        return stats

    @staticmethod
    def get_rankings(students: List[Student], criteria: str = "percentage", subject: Optional[str] = None) -> List[Student]:
        """
        Ranks all students based on overall percentage, total marks, or subject-specific marks.
        Uses our custom_sort Merge Sort algorithm to guarantee stable sorting.
        """
        if not students:
            return []
            
        if criteria == "total_marks":
            key_fn = lambda s: s.get_total_marks()
        elif criteria == "subject" and subject:
            # Treat missing subjects as 0.0 to ensure they are ranked bottom
            key_fn = lambda s: s.marks.get(subject, 0.0)
        else:
            # Default to percentage
            key_fn = lambda s: s.get_percentage()
            
        return custom_sort(students, key_func=key_fn, reverse=True)


class ReportGenerator:
    """
    Handles report generation, file exporting, and visual graph renderings.
    """

    @staticmethod
    def print_student_report_card(student: Student) -> None:
        """
        Prints a visually stunning academic report card in the terminal
        using Unicode box-drawing elements.
        """
        print("\n" + "╔" + "═" * 60 + "╗")
        print(f"║ {'ACADEMIC REPORT CARD':^58} ║")
        print("╠" + "═" * 60 + "╣")
        print(f"║ ID: {student.student_id:<25} Class/Sec: {student.class_section:<20} ║")
        print(f"║ Name: {student.name:<50} ║")
        print("╠" + "═" * 60 + "╣")
        print(f"║ {'Subject':<30} │ {'Marks / 100':^25} ║")
        print("╟" + "─" * 30 + "┼" + "─" * 25 + "╢")
        
        if not student.marks:
            print(f"║ {'(No academic marks recorded)':^58} ║")
        else:
            for sub, score in student.marks.items():
                print(f"║ {sub:<30} │ {score:^25.2f} ║")
                
        print("╠" + "═" * 60 + "╣")
        print(f"║ Total Marks: {student.get_total_marks():<15.2f} Percentage: {student.get_percentage():<17.2f}% ║")
        print(f"║ Grade: {student.get_grade():<21} Status: {student.get_status():<24} ║")
        print("╠" + "═" * 60 + "╣")
        
        # AI Insights Section
        insights = generate_ai_insights(student.marks)
        print(f"║ {'AI PERFORMANCE INSIGHTS & RECOMMENDATIONS':^58} ║")
        print("╟" + "─" * 60 + "╢")
        print(f"║ Risk Level: {insights['academic_risk']:<18} Consistency: {insights['consistency_score']:<21} ║")
        
        if insights['strengths']:
            print(f"║ Strong Subjects: {', '.join(insights['strengths']):<41} ║")
        if insights['weak_areas']:
            print(f"║ Focus Required: {', '.join(insights['weak_areas']):<42} ║")
            
        print("╟" + "─" * 60 + "╢")
        print(f"║ {'Actionable Suggestions:':<58} ║")
        for sug in insights["suggestions"]:
            # Word wrap suggestion to fit inside CLI report box (max 56 chars)
            words = sug.split(" ")
            line = ""
            for word in words:
                if len(line) + len(word) + 1 <= 54:
                    line += (" " if line else "") + word
                else:
                    print(f"║   • {line:<52} ║")
                    line = word
            if line:
                print(f"║   • {line:<52} ║")
                
        print("╚" + "═" * 60 + "╝\n")

    @staticmethod
    def print_class_summary_report(students: List[Student], analytics: Analytics) -> None:
        """
        Prints a class-wide statistics dashboard to the terminal.
        """
        if not students:
            print("\n[!] No students registered in the system database.\n")
            return
            
        total_enrolled = len(students)
        passed_count = sum(1 for s in students if s.get_status() == "PASS")
        failed_count = total_enrolled - passed_count
        pass_ratio = (passed_count / total_enrolled) * 100
        
        class_avg = analytics.get_class_average(students)
        highest_s = analytics.get_class_highest_scorer(students)
        lowest_s = analytics.get_class_lowest_scorer(students)
        
        print("\n" + "╔" + "═" * 70 + "╗")
        print(f"║ {'CLASS PERFORMANCE DASHBOARD SUMMARY':^68} ║")
        print("╠" + "═" * 70 + "╣")
        print(f"║ Total Enrolled: {total_enrolled:<15} Passed: {passed_count:<10} Failed: {failed_count:<12} ║")
        print(f"║ Class Pass Rate: {pass_ratio:<13.2f}% Class Average Score: {class_avg:<18.2f}% ║")
        
        if highest_s:
            print(f"║ Class Topper: {highest_s.name:<25} (ID: {highest_s.student_id:<12} - {highest_s.get_percentage():.2f}%) ║")
        if lowest_s:
            print(f"║ Needs Support: {lowest_s.name:<25} (ID: {lowest_s.student_id:<12} - {lowest_s.get_percentage():.2f}%) ║")
            
        print("╠" + "═" * 70 + "╣")
        print(f"║ {'SUBJECT-WISE PERFORMANCE METRICS':^68} ║")
        print("╟" + "─" * 70 + "╢")
        print(f"║ {'Subject':<18} │ {'Avg %':^10} │ {'Highest':^10} │ {'Lowest':^10} │ {'Enrolled':^8} ║")
        print("╟" + "─" * 18 + "┼" + "─" * 10 + "┼" + "─" * 10 + "┼" + "─" * 10 + "┼" + "─" * 8 + "╢")
        
        sub_stats = analytics.get_subject_statistics(students)
        if not sub_stats:
            print(f"║ {'(No subject-specific marks recorded)':^68} ║")
        else:
            for sub, info in sub_stats.items():
                print(f"║ {sub:<18} │ {info['average']:^10.2f} │ {info['highest']:^10.2f} │ {info['lowest']:^10.2f} │ {info['count']:^8} ║")
                
        print("╠" + "═" * 70 + "╣")
        print(f"║ {'CLASS LEADERBOARD (TOP 5)':^68} ║")
        print("╟" + "─" * 70 + "╢")
        print(f"║ {'Rank':^6} │ {'ID':<10} │ {'Name':<22} │ {'Class':<8} │ {'Percentage':^12} ║")
        print("╟" + "─" * 6 + "┼" + "─" * 10 + "┼" + "─" * 22 + "┼" + "─" * 8 + "┼" + "─" * 12 + "╢")
        
        ranked_list = analytics.get_rankings(students, criteria="percentage")
        for i, s in enumerate(ranked_list[:5]):
            print(f"║ {i+1:^6} │ {s.student_id:<10} │ {s.name:<22} │ {s.class_section:<8} │ {s.get_percentage():^12.2f}% ║")
            
        print("╚" + "═" * 70 + "╝\n")

    @staticmethod
    def export_students_to_csv(students: List[Student], filepath: str) -> None:
        """
        Exports summary academic data of all students in the database to a CSV file.
        """
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Write header row
                writer.writerow(["Student ID", "Name", "Class-Section", "Total Marks", "Average/Percentage", "Grade", "Status", "Subject Marks"])
                
                # Write student data rows
                for s in students:
                    marks_str = "; ".join([f"{sub}:{score}" for sub, score in s.marks.items()])
                    writer.writerow([
                        s.student_id,
                        s.name,
                        s.class_section,
                        round(s.get_total_marks(), 2),
                        round(s.get_percentage(), 2),
                        s.get_grade(),
                        s.get_status(),
                        marks_str
                    ])
            logger.info(f"Student data exported to CSV successfully at {filepath}")
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            raise IOError(f"Could not export database to CSV: {e}")

    @staticmethod
    def generate_performance_charts(students: List[Student], output_dir: str) -> List[str]:
        """
        Generates publication-quality data visualization charts using Matplotlib
        and saves them as high-DPI PNG images in the specified directory.
        
        Returns:
            List of generated absolute file paths.
        """
        if not students:
            logger.warning("No student records available. Skipping chart generation.")
            return []
            
        os.makedirs(output_dir, exist_ok=True)
        generated_paths = []
        
        # Color palette definitions for modern sleek dashboard appearance
        accent_color = "#4f46e5"  # indigo
        secondary_color = "#06b6d4"  # cyan
        success_color = "#10b981"  # emerald
        danger_color = "#ef4444"  # rose
        neutral_muted = "#6b7280"  # gray
        
        # ==========================================
        # CHART 1: Subject-Wise Average Scores
        # ==========================================
        subject_scores: Dict[str, List[float]] = {}
        for s in students:
            for sub, score in s.marks.items():
                if sub not in subject_scores:
                    subject_scores[sub] = []
                subject_scores[sub].append(score)
                
        if subject_scores:
            subjects = list(subject_scores.keys())
            averages = [sum(scores)/len(scores) for scores in subject_scores.values()]
            
            plt.figure(figsize=(10, 6), dpi=150)
            bars = plt.bar(subjects, averages, color=accent_color, width=0.5, edgecolor="black", linewidth=0.7)
            
            # Formatting Chart
            plt.title("Class Average Score by Academic Subject", fontsize=14, fontweight="bold", pad=15)
            plt.xlabel("Subjects", fontsize=12, fontweight="semibold", labelpad=10)
            plt.ylabel("Average Score (%)", fontsize=12, fontweight="semibold", labelpad=10)
            plt.ylim(0, 105)
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            
            # Value tags on top of bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2.0, height + 2, f"{height:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='semibold')
                
            plt.tight_layout()
            chart1_path = os.path.join(output_dir, "subject_averages.png")
            plt.savefig(chart1_path)
            plt.close()
            generated_paths.append(chart1_path)
            
        # ==========================================
        # CHART 2: Class Grade Distribution
        # ==========================================
        grades = ["A+", "A", "B", "C", "D", "E", "F"]
        grade_counts = {g: 0 for g in grades}
        for s in students:
            g = s.get_grade()
            if g in grade_counts:
                grade_counts[g] += 1
                
        if sum(grade_counts.values()) > 0:
            labels = [g for g, cnt in grade_counts.items() if cnt > 0]
            counts = [cnt for cnt in grade_counts.values() if cnt > 0]
            
            # Curated harmonious color theme for grades
            grade_colors = ["#10b981", "#3b82f6", "#6366f1", "#f59e0b", "#ef4444", "#ec4899", "#6b7280"]
            colors_slice = grade_colors[:len(labels)]
            
            plt.figure(figsize=(8, 8), dpi=150)
            plt.pie(
                counts,
                labels=labels,
                autopct=lambda pct: f'{pct:.1f}%\n({int(pct*sum(counts)/100)})',
                startangle=140,
                colors=colors_slice,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'antialiased': True},
                textprops={'fontsize': 11, 'fontweight': 'semibold'}
            )
            
            plt.title("Class Academic Letter Grade Distribution", fontsize=14, fontweight="bold", pad=15)
            plt.tight_layout()
            chart2_path = os.path.join(output_dir, "grade_distribution.png")
            plt.savefig(chart2_path)
            plt.close()
            generated_paths.append(chart2_path)
            
        # ==========================================
        # CHART 3: Top 5 Performers Leaderboard
        # ==========================================
        # Get sorted students
        ranked = custom_sort(students, key_func=lambda s: s.get_percentage(), reverse=True)
        top_5 = ranked[:5]
        
        if top_5:
            names = [f"{s.name}\n({s.student_id})" for s in top_5]
            pcts = [s.get_percentage() for s in top_5]
            
            plt.figure(figsize=(10, 6), dpi=150)
            # Create a horizontal bar chart
            y_pos = range(len(names))
            bars = plt.barh(y_pos, pcts, color=secondary_color, edgecolor="black", linewidth=0.7, height=0.55)
            
            plt.yticks(y_pos, names, fontsize=10, fontweight="semibold")
            plt.title("Top Academic Performers Leaderboard", fontsize=14, fontweight="bold", pad=15)
            plt.xlabel("Overall Academic Percentage (%)", fontsize=12, fontweight="semibold", labelpad=10)
            plt.xlim(0, 105)
            plt.gca().invert_yaxis()  # Put #1 ranked on top
            plt.grid(axis='x', linestyle='--', alpha=0.5)
            
            # Value tags on side of bars
            for bar in bars:
                width = bar.get_width()
                plt.text(width + 1, bar.get_y() + bar.get_height()/2.0, f" {width:.2f}%", ha='left', va='center', fontsize=10, fontweight='semibold')
                
            plt.tight_layout()
            chart3_path = os.path.join(output_dir, "top_performers.png")
            plt.savefig(chart3_path)
            plt.close()
            generated_paths.append(chart3_path)
            
        return generated_paths
