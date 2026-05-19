# Dictionary Comprehension: Grading System
test_scores = {
    "Alice": 85,
    "Bob": 42,
    "Charlie": 78,
    "Diana": 59
}
grade_results = {name: "Passed" if score >= 60 
                 else "Failed" for name, score in test_scores.items()} # Dict Comprehension with if-else logic
print("Final Results:")
print(grade_results)
