class Deptartment:
    def __init__(self, name):
        self.name = name
        self.courses = set()

    def add_course(self, course):
        #self.courses[course.number] = course
        self.courses.add(course)
