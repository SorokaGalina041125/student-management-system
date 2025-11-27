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
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Error'
        
        
# Добавить функции в конец файла
def calculate_average_homework_grade(students, course_name):
    total_grades = []
    for student in students:
        if course_name in student.grades:
            total_grades.extend(student.grades[course_name])
    return sum(total_grades) / len(total_grades) if total_grades else 0

def calculate_average_lecture_grade(lecturers, course_name):
    total_grades = []
    for lecturer in lecturers:
        if hasattr(lecturer, 'lecture_grades') and course_name in lecturer.lecture_grades:
            total_grades.extend(lecturer.lecture_grades[course_name])
    return sum(total_grades) / len(total_grades) if total_grades else 0

# Добавить тестовый код
if __name__ == "__main__":
    # Создание и тестирование объектов
    student1 = Student('Ruoy', 'Eman', 'male')
    student1.courses_in_progress = ['Python']
    
    lecturer1 = Lecturer('Some', 'Buddy')
    lecturer1.courses_attached = ['Python']
    
    reviewer1 = Reviewer('John', 'Doe')
    reviewer1.courses_attached = ['Python']
    
    # Тестирование методов
    reviewer1.rate_hw(student1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Python', 9)
    
    print(student1)
    print(lecturer1)
    
    # Тестирование сравнения
    student2 = Student('Alice', 'Smith', 'female')
    student2.courses_in_progress = ['Python']
    reviewer1.rate_hw(student2, 'Python', 8)
    
    print(f"\nStudent comparison: {student1 > student2}")
    print(f"Student equality: {student1 == student2}")