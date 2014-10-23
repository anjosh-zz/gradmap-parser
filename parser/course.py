import sys
import re
from pprint import pprint
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)
from department import Department

# Special Course definitions
SECOND_WRIT = {'name':'Gen Ed Writing Level 2', 'number':2367, 'dept':'ENGR'}

class Course(Prereq):
    # TODO Might want to add more constraint properties latter
    name = StringProperty()
    number = IntegerProperty(index=True)
    level = StringProperty()
    credits = IntegerProperty(index=True)

    dept = RelationshipTo('department.Department', 'BELONGS_TO')
    prereq = RelationshipTo('Course', 'REQUIRES')

    # using a string here unlike parse_department
    def parse_course(m_obj):
        count += 1
        number = int(m_obj.group(1))
        name = m_obj.group(2)
        level = m_obj.group(3)
        credits = int(m_obj.group(4))
        c = Course(name=name, number=number, level=level, credits=credits)

        prereq_str = m_obj.group(5)
        added_groups = prereq_str.split('and')

        for and_group in added_groups:
            and_group = and_group.strip()
            if 'or' in and_group:
                or_group = OrNode()
                or_group.add_prereqs(and_group, cse_dept)
                # TODO might want to test to see if or_group.prereqs equals
                # 0 or 1 and then delete the or_group obj if that's true
                c.prereq.connect(or_group)
            else:
                c.add_prereqs(and_group, cse_dept)

        pprint(vars(c))
        c.save()

    def add_prereqs(self, prereqs, cse_dept):
        m = re.search(r"([A-Za-z]{3,4})", prereqs)
        dept = m.group(1).upper() if m else 'CSE'
        if dept != 'NOT':
            p_list = prereqs.split(',')
            for c_str in p_list:
                if c_str == "Gen Ed Writing Level 2":
                    c = Course(SECOND_WRIT)
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
