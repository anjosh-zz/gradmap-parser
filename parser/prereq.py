import sys

from neomodel import (StructuredNode, StringProperty, RelationshipFrom, RelationshipTo, IntegerProperty)


class Prereq(StructuredNode):
    name = StringProperty(index=True)

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
    parent = RelationshipFrom('Course', 'REQUIRES')
    orgroup = RelationshipFrom('OrGroup', 'REQUIRES')

    def to_dict(self):
        d = dict.copy(self.__dict__)
        d.pop('dept')
        d.pop('prereq')
        d.pop('parent')
        d.pop('orgroup')
        return d


class OrGroup(Prereq):
    course = RelationshipFrom('Course', 'REQUIRES')
    prereq = RelationshipTo('Course', 'REQUIRES')

    def to_dict(self):
        d = dict.copy(self.__dict__)
        d.pop('course')
        d.pop('prereq')
        children = self.course.all()
        c_array = []
        for c in children:
            c_array.append(c.to_dict())
        d['children'] = c_array
        return d