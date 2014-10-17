import sys
import re
from pprint import pprint
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)
#import department
from department import Department

# Special Course definitions
SECOND_WRIT = {'name':'Gen Ed Writing Level 2', 'number':2367, 'dept':'ENGR'}

class Course(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty()
    number = IntegerProperty(index=True)
    level = StringProperty()
    credits = IntegerProperty(index=True)
    dept = StringProperty()

    #dept = RelationshipTo('Deptartment', 'IS_FROM')
    prereq = RelationshipFrom('Course', 'PREREQ')

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

    def add_prereqs(self, prereqs):
        m = re.search(r"([A-Za-z]{3,4})", prereqs)
        dept = m.group(1).upper() if m else 'CSE'
        if dept != 'NOT':
            p_list = prereqs.split(',')
            for c_str in p_list:
                if c_str == "Gen Ed Writing Level 2":
                    c = Course(SECOND_WRIT).save()
                    self.prereq.connect(c)
                else:
                    m = re.search(r"(\d{4})", c_str)
                    if m:
                        number = int(m.group(1))
                        print number
                        print dept
                        c = Course(number=number, dept=dept).save()
                        pprint(vars(c))
                        self.prereq.connect(c)
