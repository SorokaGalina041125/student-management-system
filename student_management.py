class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)
        
    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if not hasattr(lecturer, 'lecture_grades'):
                lecturer.lecture_grades = {}
            if course in lecturer.lecture_grades:
                lecturer.lecture_grades[course].append(grade)
            else:
                lecturer.lecture_grades[course] = [grade]
        else:
            return 'Error'

    def get_average_grade(self):
        total_grades = []
        for course_grades in self.grades.values():
            total_grades.extend(course_grades)
        return sum(total_grades) / len(total_grades) if total_grades else 0

    def __str__(self):
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return f"Name: {self.name}\nSurname: {self.surname}\nAverage homework grade: {self.get_average_grade():.1f}\nCourses in progress: {courses_in_progress}\nCompleted courses: {finished_courses}"

    def __lt__(self, other):
        return self.get_average_grade() < other.get_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Name: {self.name}\nSurname: {self.surname}"


class Lecturer(Mentor):

    def get_average_grade(self):
        if not hasattr(self, 'lecture_grades'):
            return 0
        total_grades = []
        for course_grades in self.lecture_grades.values():
            total_grades.extend(course_grades)
        return sum(total_grades) / len(total_grades) if total_grades else 0

    def __str__(self):
        return f"Name: {self.name}\nSurname: {self.surname}\nAverage lecture grade: {self.get_average_grade():.1f}"

    def __lt__(self, other):
        return self.get_average_grade() < other.get_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Error'