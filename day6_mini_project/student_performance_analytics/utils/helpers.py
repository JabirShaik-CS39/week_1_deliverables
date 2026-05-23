import re
import math
from typing import List, Dict, Any, Callable, Optional, Union

def custom_sort(data: List[Any], key_func: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> List[Any]:
    """
    A stable Merge Sort algorithm that mimics Python's built-in sorted() function.
    Maintains the original relative order of elements that have equal keys (stability).
    
    Args:
        data: The iterable to sort.
        key_func: A function of one argument that is used to extract a comparison key from each element.
        reverse: If True, the list elements are sorted as if each comparison were reversed.
        
    Returns:
        A new sorted list.
    """
    # Create a shallow copy of the input list to avoid side effects
    arr = list(data)
    if len(arr) <= 1:
        return arr
    
    # If no key function is provided, use the identity function
    if key_func is None:
        key_func = lambda x: x
        
    def _merge_sort(sub_arr: List[Any]) -> List[Any]:
        if len(sub_arr) <= 1:
            return sub_arr
        
        mid = len(sub_arr) // 2
        left = _merge_sort(sub_arr[:mid])
        right = _merge_sort(sub_arr[mid:])
        
        return _merge(left, right)
        
    def _merge(left: List[Any], right: List[Any]) -> List[Any]:
        result = []
        i, j = 0, 0
        
        while i < len(left) and j < len(right):
            left_key = key_func(left[i])
            right_key = key_func(right[j])
            
            if not reverse:
                # Stable ascending: prefer left element if left_key <= right_key
                if left_key <= right_key:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            else:
                # Stable descending: prefer left element if left_key >= right_key
                if left_key >= right_key:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
                    
        # Append remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        return result
        
    return _merge_sort(arr)


# ==========================================
# Input Validation Helpers
# ==========================================

def validate_student_id(student_id: str) -> bool:
    """
    Validates the Student ID format.
    Canonical Format: STD-XXXX (where X is a digit, e.g. STD-0042)
    Supports case-insensitivity during input and auto-converts to upper case.
    """
    pattern = r"^STD-\d{4}$"
    return bool(re.match(pattern, student_id.strip().upper()))

def validate_name(name: str) -> bool:
    """
    Validates name strings.
    Must be between 2 and 50 characters, containing only letters and spaces.
    """
    trimmed = name.strip()
    if len(trimmed) < 2 or len(trimmed) > 50:
        return False
    # Allow spaces, alphabetic characters, and single quotes/hyphens in names
    pattern = r"^[a-zA-Z\s\'-]+$"
    return bool(re.match(pattern, trimmed))

def validate_class_section(class_section: str) -> bool:
    """
    Validates class-section format.
    Format: Class-Section (e.g. 10-A, 12-F, 5-C)
    Classes can range from 1 to 12, and sections from A to Z.
    """
    pattern = r"^([1-9]|1[0-2])-[A-Z]$"
    return bool(re.match(pattern, class_section.strip().upper()))

def validate_subject(subject: str) -> bool:
    """
    Validates subject names.
    Must be between 2 and 30 characters, containing only letters, numbers, and spaces.
    """
    trimmed = subject.strip()
    if len(trimmed) < 2 or len(trimmed) > 30:
        return False
    pattern = r"^[a-zA-Z0-9\s#\+-]+$"  # Allow letters, spaces, and minor marks like #, +, and - (e.g., C#, C++)
    return bool(re.match(pattern, trimmed))

def validate_mark(mark: Union[int, float]) -> bool:
    """
    Validates subject mark values.
    Must be a number between 0 and 100 inclusive.
    """
    try:
        val = float(mark)
        return 0.0 <= val <= 100.0
    except (ValueError, TypeError):
        return False


# ==========================================
# Rule-Based AI Insights Engine
# ==========================================

def generate_ai_insights(marks: Dict[str, float]) -> Dict[str, Any]:
    """
    Analyzes student marks to generate professional, contextual feedback,
    identifying strengths, weaknesses, consistency, and risk factors.
    
    Args:
        marks: Dictionary of {subject: mark}
        
    Returns:
        Dict containing analytical categories:
        - strengths: List of strong subjects (marks >= 85)
        - weak_areas: List of weak subjects (marks < 50)
        - scope_for_improvement: List of average subjects (50 <= marks < 80)
        - consistency_score: High/Moderate/Low (based on Standard Deviation)
        - academic_risk: High/Medium/Low (based on overall performance & fails)
        - suggestions: List of actionable study tips
    """
    if not marks:
        return {
            "strengths": [],
            "weak_areas": [],
            "scope_for_improvement": [],
            "consistency_score": "N/A",
            "academic_risk": "N/A",
            "suggestions": ["No academic records available to compile insights. Please add marks first."]
        }
        
    # Calculate stats
    scores = list(marks.values())
    avg_score = sum(scores) / len(scores)
    
    # Calculate Standard Deviation to determine performance consistency
    mean = avg_score
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    std_dev = math.sqrt(variance)
    
    strengths = [sub for sub, score in marks.items() if score >= 85]
    weak_areas = [sub for sub, score in marks.items() if score < 50]
    scope_for_improvement = [sub for sub, score in marks.items() if 50 <= score < 80]
    
    # Consistency evaluation
    if len(scores) <= 1:
        consistency = "Consistent (Single Subject)"
    elif std_dev < 10:
        consistency = "High (Balanced performance across all subjects)"
    elif std_dev < 20:
        consistency = "Moderate (Variable performance, some subject skew)"
    else:
        consistency = "Low (Highly uneven, excels in some but struggles in others)"
        
    # Academic Risk Level
    num_failing = len(weak_areas)
    if avg_score < 40 or num_failing >= 3:
        risk_level = "HIGH RISK"
    elif avg_score < 55 or num_failing > 0:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"
        
    # Actionable suggestions
    suggestions = []
    if strengths:
        suggestions.append(f"Outstanding execution in {', '.join(strengths)}. Consider mentoring peers or taking advanced topics in these areas.")
    
    if weak_areas:
        suggestions.append(f"Immediate remediation required in {', '.join(weak_areas)}. Recommend joining remedial classes, consulting teachers, and allocating 45 mins daily to these subjects.")
        
    if scope_for_improvement:
        suggestions.append(f"Targeted practice in {', '.join(scope_for_improvement)} can easily elevate overall academic rank. Dedicate focus to weak concepts in these subjects.")
        
    if consistency == "Low (Highly uneven, excels in some but struggles in others)":
        suggestions.append("Work on balancing study hours. Avoid spending disproportionate time only on favorite subjects; create a structured study timetable.")
        
    if risk_level == "HIGH RISK":
        suggestions.append("CRITICAL: Schedule an urgent meeting with parent/guardian and subject teachers to design a customized academic turnaround plan.")
    elif risk_level == "MEDIUM RISK":
        suggestions.append("Academic counseling is recommended to address initial bottlenecks before final term exams.")
    elif not weak_areas and not scope_for_improvement and avg_score >= 90:
        suggestions.append("Superb performance! Maintain this momentum and participate in Olympiads, national competitive exams, or hobby projects.")
        
    if not suggestions:
        suggestions.append("Steady progress observed. Maintain regular revisions and complete all mock tests to stay sharp.")
        
    return {
        "strengths": strengths,
        "weak_areas": weak_areas,
        "scope_for_improvement": scope_for_improvement,
        "consistency_score": consistency,
        "academic_risk": risk_level,
        "suggestions": suggestions
    }


# ==========================================
# Robust CLI Input Prompt Helpers
# ==========================================

def get_string_input(prompt: str, min_len: int = 1, max_len: int = 100, 
                     validator: Optional[Callable[[str], bool]] = None, 
                     error_msg: str = "Invalid input.") -> str:
    """
    Safely prompts user for a string with validation and length checks.
    """
    while True:
        try:
            val = input(prompt).strip()
            if len(val) < min_len or len(val) > max_len:
                print(f"Error: Length must be between {min_len} and {max_len} characters.")
                continue
            if validator and not validator(val):
                print(f"Error: {error_msg}")
                continue
            return val
        except (KeyboardInterrupt, EOFError):
            print("\nInput interrupted. Using default.")
            return ""

def get_int_input(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Safely prompts user for an integer within an optional range.
    """
    while True:
        try:
            val_str = input(prompt).strip()
            val = int(val_str)
            if min_val is not None and val < min_val:
                print(f"Error: Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Error: Value cannot exceed {max_val}.")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid integer.")
        except (KeyboardInterrupt, EOFError):
            print("\nInput interrupted. Returning 0.")
            return 0

def get_float_input(prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
    """
    Safely prompts user for a float within an optional range.
    """
    while True:
        try:
            val_str = input(prompt).strip()
            val = float(val_str)
            if min_val is not None and val < min_val:
                print(f"Error: Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Error: Value cannot exceed {max_val}.")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid float number.")
        except (KeyboardInterrupt, EOFError):
            print("\nInput interrupted. Returning 0.0.")
            return 0.0

def get_choice_input(prompt: str, choices: List[str]) -> str:
    """
    Prompts user to select from a list of options. Case-insensitive matching.
    """
    choices_lower = [c.lower() for c in choices]
    while True:
        try:
            val = input(prompt).strip()
            if val.lower() in choices_lower:
                idx = choices_lower.index(val.lower())
                return choices[idx]
            print(f"Error: Invalid choice. Choose from {', '.join(choices)}.")
        except (KeyboardInterrupt, EOFError):
            print("\nInput interrupted. Selecting first option.")
            return choices[0]
