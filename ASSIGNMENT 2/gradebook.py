# GradeBook Analyzer
# Name: Deepanshu Gulia
# Roll No: 2501730335
# Course: BTECH CSE (AIML)
# Subject: Problem Solving Using Python

import csv
import statistics

def manual_input():
    marks = {}
    n = int(input("Enter number of students: "))
    for i in range(n):
        name = input("Enter student name: ")
        score = float(input("Enter marks: "))
        marks[name] = score
    return marks

def csv_input():
    marks = {}
    filename = input("Enter CSV file name: ")
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0]
                score = float(row[1])
                marks[name] = score
        print("CSV data loaded successfully!")
    except:
        print("Error loading file.")
    return marks

def calculate_average(marks):
    return sum(marks.values()) / len(marks)

def calculate_median(marks):
    return statistics.median(marks.values())

def find_max_score(marks):
    return max(marks.values())

def find_min_score(marks):
    return min(marks.values())

def assign_grades(marks):
    grades = {}
    for name, score in marks.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"
    return grades

def pass_fail(marks):
    passed = [name for name, score in marks.items() if score >= 40]
    failed = [name for name, score in marks.items() if score < 40]
    return passed, failed

def display_table(marks, grades):
    print("\nName\t\tMarks\tGrade")
    print("-------------------------------")
    for name in marks:
        print(f"{name}\t\t{marks[name]}\t{grades[name]}")

def main():
    print("\nWELCOME TO GRADEBOOK ANALYZER")
    print("1. Manual Input")
    print("2. Load from CSV")

    choice = input("Enter your choice: ")

    if choice == "1":
        marks = manual_input()
    elif choice == "2":
        marks = csv_input()
    else:
        print("Invalid choice!")
        return

    avg = calculate_average(marks)
    med = calculate_median(marks)
    max_score = find_max_score(marks)
    min_score = find_min_score(marks)

    print("\n--- Analysis Summary ---")
    print("Average:", avg)
    print("Median:", med)
    print("Maximum:", max_score)
    print("Minimum:", min_score)

    grades = assign_grades(marks)

    print("\n--- Grade Distribution ---")
    for grade in ["A", "B", "C", "D", "F"]:
        print(f"{grade}: {list(grades.values()).count(grade)}")

    passed, failed = pass_fail(marks)
    print("\nPassed Students:", passed)
    print("Failed Students:", failed)

    display_table(marks, grades)

    repeat = input("\nDo you want to analyze another set? (yes/no): ")
    if repeat.lower() == "yes":
        main()
    else:
        print("Thank you for using GradeBook Analyzer!")

main()
