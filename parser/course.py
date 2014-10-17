import sys
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)

class Course(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty(unique_index=True)
    number = IntegerProperty(index=True)
    level = StringProperty()
    credits = IntegerProperty(index=True)

    dept = RelationshipTo('Deptartment', 'IS_FROM')
    prereq = RelationshipTo('Course', 'REQUIRES')

    #def __init__(self, name = None, number = None, dept = None,
    #        level = None, credits = None):
    #    self.number = number
    #    self.dept = dept
    #    self.name = name
    #    self.level = level
    #    self.credits = credits
    #    self.prereqs = []
    #    super(Course, self).__init__(self, **args)

    @staticmethod
    def print_prereq(prereq):
        sys.stdout.write('({0}, {1})'.format(prereq.dept, prereq.number))

    def print_prereqs(self):
        sys.stdout.write('[')
        sys.stdout.write(' ')
        for p in self.prereqs:
            if p.prereqs:
                Course.print_prereqs(p)
            else:
                Course.print_prereq(p)
            sys.stdout.write(' ')
        sys.stdout.write(']')

    #def add_prereq(prereq):
    #    self.prereqs.append(prereq)
