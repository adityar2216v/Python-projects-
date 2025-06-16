class Person:
    def __init__(self, person_id, name, email):
        self.person_id = person_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"ID: {self.person_id}, Name: {self.name}, Email: {self.email}"

class Student(Person):
    def __init__(self, person_id, name, email, major):
        super().__init__(person_id, name, email)
        self.major = major
        self.enrolled_courses = []

    def enroll_course(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            course.add_student(self)
            print(f"Student {self.name} enrolled in {course.name}.")
        else:
            print(f"Student {self.name} is already enrolled in {course.name}.")

    def get_enrolled_courses(self):
        return self.enrolled_courses

    def __str__(self):
        return f"Student - {super().__str__()}, Major: {self.major}"

class Professor(Person):
    def __init__(self, person_id, name, email, department):
        super().__init__(person_id, name, email)
        self.department = department
        self.taught_courses = []

    def assign_course(self, course):
        if course not in self.taught_courses:
            self.taught_courses.append(course)
            course.set_professor(self)
            print(f"Professor {self.name} assigned to {course.name}.")
        else:
            print(f"Professor {self.name} is already assigned to {course.name}.")

    def get_taught_courses(self):
        return self.taught_courses

    def __str__(self):
        return f"Professor - {super().__str__()}, Department: {self.department}"

class Course:
    def __init__(self, course_id, name, credits):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.students = []
        self.professor = None

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
        else:
            print(f"Student {student.name} is already in {self.name}.")

    def set_professor(self, professor):
        self.professor = professor

    def __str__(self):
        prof_name = self.professor.name if self.professor else "Not assigned"
        return f"Course ID: {self.course_id}, Name: {self.name}, Credits: {self.credits}, Professor: {prof_name}, Enrolled Students: {len(self.students)}"

class University:
    def __init__(self, name):
        self.name = name
        self.students = {}
        self.professors = {}
        self.courses = {}

    def add_student(self, student):
        if student.person_id not in self.students:
            self.students[student.person_id] = student
            print(f"Student {student.name} added to {self.name}.")
        else:
            print(f"Student with ID {student.person_id} already exists.")

    def add_professor(self, professor):
        if professor.person_id not in self.professors:
            self.professors[professor.person_id] = professor
            print(f"Professor {professor.name} added to {self.name}.")
        else:
            print(f"Professor with ID {professor.person_id} already exists.")

    def add_course(self, course):
        if course.course_id not in self.courses:
            self.courses[course.course_id] = course
            print(f"Course {course.name} added to {self.name}.")
        else:
            print(f"Course with ID {course.course_id} already exists.")

    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_professor(self, professor_id):
        return self.professors.get(professor_id)

    def get_course(self, course_id):
        return self.courses.get(course_id)

    def __str__(self):
        return f"University: {self.name}, Students: {len(self.students)}, Professors: {len(self.professors)}, Courses: {len(self.courses)}"

# Example Usage:
if __name__ == "__main__":
    my_university = University("State University")

    # Add professors
    prof1 = Professor("P001", "Dr. Smith", "smith@uni.edu", "Computer Science")
    prof2 = Professor("P002", "Dr. Jones", "jones@uni.edu", "Mathematics")
    my_university.add_professor(prof1)
    my_university.add_professor(prof2)

    # Add courses
    course1 = Course("CS101", "Introduction to Programming", 3)
    course2 = Course("MA201", "Calculus I", 4)
    my_university.add_course(course1)
    my_university.add_course(course2)

    # Assign professors to courses
    prof1.assign_course(course1)
    prof2.assign_course(course2)

    # Add students
    student1 = Student("S001", "Alice", "alice@uni.edu", "Computer Science")
    student2 = Student("S002", "Bob", "bob@uni.edu", "Mathematics")
    student3 = Student("S003", "Charlie", "charlie@uni.edu", "Computer Science")
    my_university.add_student(student1)
    my_university.add_student(student2)
    my_university.add_student(student3)

    # Enroll students in courses
    student1.enroll_course(course1)
    student3.enroll_course(course1)
    student2.enroll_course(course2)

    print("\n--- University Status ---")
    print(my_university)

    print("\n--- Course Details ---")
    print(my_university.get_course("CS101"))
    print(my_university.get_course("MA201"))

    print("\n--- Student Details ---")
    print(my_university.get_student("S001"))
    for c in my_university.get_student("S001").get_enrolled_courses():
        print(f"  - {c.name}")

    print("\n--- Professor Details ---")
    print(my_university.get_professor("P001"))
    for c in my_university.get_professor("P001").get_taught_courses():
        print(f"  - {c.name}")