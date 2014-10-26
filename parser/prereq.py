import sys

from neomodel import (StructuredNode, StringProperty, RelationshipFrom, RelationshipTo, IntegerProperty)


class Prereq(StructuredNode):
    name = StringProperty(index=True)
    parent = RelationshipFrom('Course', 'REQUIRES')

    @staticmethod
    def print_prereq(prereq):
        sys.stdout.write('({0}, {1})'.format(prereq.dept, prereq.number))

    def print_prereqs(self):
        sys.stdout.write('[')
        sys.stdout.write(' ')
        for p in self.prereqs:
            if p.prereqs:
                p.print_prereqs()
            else:
                p.print_prereq()
            sys.stdout.write(' ')
        sys.stdout.write(']')


class Course(Prereq):
    # TODO Might want to add more constraint properties later
    number = IntegerProperty(index=True)
    level = StringProperty()
    credit_hours = IntegerProperty(index=True)

    dept = RelationshipTo('department.Department', 'IN')
    prereq = RelationshipTo('Prereq', 'REQUIRES')


class OrGroup(Prereq):
    # course = RelationshipFrom('prereq.Course', 'IN')
    prereq = RelationshipFrom('Course', 'REQUIRES')