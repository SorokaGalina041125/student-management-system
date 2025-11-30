import sys
import io

# Устанавливаем кодировку UTF-8 для вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_finished_course(self, course_name):
        """Adds a completed course"""
        self.finished_courses.append(course_name)
    
    def rate_lecture(self, lecturer, course, grade):
        """Rates a lecturer's lecture"""
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.lecture_grades:
                lecturer.lecture_grades[course].append(grade)
            else:
                lecturer.lecture_grades[course] = [grade]
        else:
            return 'Error'
    
    def get_average_grade(self):
        """Calculates average grade with rounding"""
        total_grades = []
        for course_grades in self.grades.values():
            total_grades.extend(course_grades)
        if total_grades:
            return round(sum(total_grades) / len(total_grades), 1)
        return 0
    
    def __str__(self):
        """String representation of student"""
        courses_in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else "none"
        finished_courses = ', '.join(self.finished_courses) if self.finished_courses else "none"
        return f"Name: {self.name}\nSurname: {self.surname}\nAverage homework grade: {self.get_average_grade()}\nCourses in progress: {courses_in_progress}\nCompleted courses: {finished_courses}"
    
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()
    
    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() <= other.get_average_grade()
    
    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() == other.get_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Name: {self.name}\nSurname: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        """Constructor with super() call and lecture_grades initialization"""
        super().__init__(name, surname)
        self.lecture_grades = {}
    
    def get_average_grade(self):
        """Calculates average lecture grade with rounding"""
        total_grades = []
        for course_grades in self.lecture_grades.values():
            total_grades.extend(course_grades)
        if total_grades:
            return round(sum(total_grades) / len(total_grades), 1)
        return 0
    
    def __str__(self):
        """String representation of lecturer"""
        return f"Name: {self.name}\nSurname: {self.surname}\nAverage lecture grade: {self.get_average_grade()}"

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()
    
    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() <= other.get_average_grade()
    
    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() == other.get_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        """Grades student's homework"""
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Error'


def calculate_average_homework_grade(students, course_name):
    """Calculates average homework grade for a course"""
    total_grades = []
    for student in students:
        if course_name in student.grades:
            total_grades.extend(student.grades[course_name])
    if total_grades:
        average = round(sum(total_grades) / len(total_grades), 1)
        return f"Average homework grade for {course_name}: {average}"
    return f"No grades for course {course_name}"


def calculate_average_lecture_grade(lecturers, course_name):
    """Calculates average lecture grade for a course"""
    total_grades = []
    for lecturer in lecturers:
        if course_name in lecturer.lecture_grades:
            total_grades.extend(lecturer.lecture_grades[course_name])
    if total_grades:
        average = round(sum(total_grades) / len(total_grades), 1)
        return f"Average lecture grade for {course_name}: {average}"
    return f"No lecture grades for course {course_name}"


# Testing
if __name__ == "__main__":
    # Create objects
    student1 = Student('Ruoy', 'Eman', 'male')
    student1.courses_in_progress = ['Python', 'Git']
    student1.finished_courses = ['Introduction to programming']
    
    student2 = Student('Alice', 'Smith', 'female')
    student2.courses_in_progress = ['Python', 'Java']
    
    lecturer1 = Lecturer('Some', 'Buddy')
    lecturer1.courses_attached = ['Python', 'Git']
    
    lecturer2 = Lecturer('John', 'Doe')
    lecturer2.courses_attached = ['Python', 'Java']
    
    reviewer1 = Reviewer('Mike', 'Johnson')
    reviewer1.courses_attached = ['Python']
    
    # Assign grades
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student2, 'Python', 8)
    
    student1.rate_lecture(lecturer1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Python', 9)
    student2.rate_lecture(lecturer2, 'Python', 8)
    
    # Test output
    print("=== STUDENTS ===")
    print(student1)
    print("\n" + "-" * 30)
    print(student2)
    
    print("\n=== LECTURERS ===")
    print(lecturer1)
    print("\n" + "-" * 30)
    print(lecturer2)
    
    print("\n=== COMPARISON ===")
    print(f"student1 > student2: {student1 > student2}")
    print(f"lecturer1 > lecturer2: {lecturer1 > lecturer2}")
    
    print("\n=== AVERAGE GRADES BY COURSE ===")
    students_list = [student1, student2]
    lecturers_list = [lecturer1, lecturer2]
    
    print(calculate_average_homework_grade(students_list, 'Python'))
    print(calculate_average_lecture_grade(lecturers_list, 'Python'))