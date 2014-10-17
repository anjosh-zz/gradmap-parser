import sys

class Course:
    def __init__(self, name = None, number = None, dept = None,
            level = None, credits = None):
        self.number = number
        self.dept = dept
        self.name = name
        self.level = level
        self.credits = credits
        self.prereqs = []

    @staticmethod
    def print_prereq(prereq):
        sys.stdout.write('({0}, {1})'.format(prereq.dept, prereq.number))

    def print_prereqs(self):
        sys.stdout.write('[')
        sys.stdout.write(' ')
        for p in self.prereqs:
            if p.prereqs:
                Course.print_prereqs(p)
            #if type(p) is list:
            #    sys.stdout.write('[')
            #    sys.stdout.write(' ')
            #    for x in p:
            #        Course.print_prereq(x)
            #        sys.stdout.write(' ')
            #    sys.stdout.write(']')
            else:
                Course.print_prereq(p)
            sys.stdout.write(' ')
        sys.stdout.write(']')

    #def add_prereq(prereq):
    #    self.prereqs.append(prereq)
