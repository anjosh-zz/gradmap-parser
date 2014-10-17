import sys
import re
from pprint import pprint
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)
from department import Department

# Special Course definitions
SECOND_WRIT = {'name':'Gen Ed Writing Level 2', 'number':2367, 'dept':'ENGR'}

class Course(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty()
    number = IntegerProperty(index=True)
    level = StringProperty()
    credits = IntegerProperty(index=True)

    dept = RelationshipTo('department.Department', 'IS_FROM')
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

    def add_prereqs(self, prereqs, cse_dept):
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
                        # TODO not using dept right now
                        # might need to add relationship to dept
                        #dept = Department(name=dept).save()
                        if dept == 'CSE':
                            c_list = cse_dept.course.search(number=number)
                            if len(c_list) == 0:
                                c = Course(number=number).save()
                                c.dept.connect(cse_dept)
                            else:
                                c = c_list[0]
                        else:
                            c = Course(number=number).save()
                        pprint(vars(c))
                        self.prereq.connect(c)
