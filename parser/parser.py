import re

import requests

import university
import department
import prereq


DEPARTMENT = "([A-Za-z]{3,4})"

ABBREV_DICT = {'Computer Science Engineering': 'CSE',
               'Mathematics': 'MATH', }

# Special Course definitions
SECOND_WRIT_STRS = ['Gen Ed Writing Level 2',
                    'second level writing course']
SECOND_WRIT = {'name': 'Gen Ed Writing Level 2', 'number': 2367}

NUMBER = "(\d{4}(?:\.\d{2})?)"
# NUMBER = "(\d{4})"
COURSE = r"(?:(?:{0} )?{1})|{2}|{3}".format(DEPARTMENT, NUMBER, *SECOND_WRIT_STRS)

OR_GROUP = 'Or Group'


def search_dept(c):
    dept = c.dept.all()[0]
    c_list = dept.course.search(number=c.number)
    if len(c_list) > 0:
        c.delete()
        c = c_list[0]
        c.dept.connect(dept)
        return c
    else:
        return c


def add_prereqs(self, prereqs):
    print("parent: " + self.name)

    if self.name == 'Or Group':
        g_parent = self.parent.all()[0]
        parent_dept = g_parent.dept.all()[0]
    else:
        parent_dept = self.dept.all()[0]

    # get the university using the parent's department's uni
    uni = parent_dept.uni.all()[0]

    # the department starts off as the parent's department
    dept_str = parent_dept.name

    it = re.finditer(COURSE, prereqs)

    for m_obj in it:
        # if there is a match for department then update
        # otherwise continue to use the old department
        if m_obj.group(1):
            dept_str = m_obj.group(1).upper()

        if dept_str != 'NOT':
            if m_obj.group(2):
                number = int(m_obj.group(2))
                print("dept: " + dept_str + " number: " + str(number))

                # check if department already exists in this uni
                dept_list = uni.dept.search(name=dept_str)

                if len(dept_list) > 0:
                    print("department already exists")
                    # check to see if the course is already listed in the
                    # department
                    dept = dept_list[0]
                    c_list = dept.course.search(number=number)

                    # class already exists in department so don't make a new one
                    if len(c_list) > 0:
                        print("class already exists")
                        c = c_list[0]

                    # the class isn't in the department so make a new one
                    else:
                        print("class doens't exist")
                        c = prereq.Course(number=number).save()
                        c.dept.connect(dept)

                # the department doesn't exist in the db
                else:
                    print("department doens't exist")
                    dept = department.Department(name=dept_str).save()
                    c = prereq.Course(number=number).save()
                    dept.uni.connect(uni)
                    c.dept.connect(dept)

                self.prereq.connect(c)


# using a string here unlike parse_department
def parse_course(c, m_obj):
    c.number = int(m_obj.group(1))

    # see if course already exists and return if it does
    c = search_dept(c)

    c.name = m_obj.group(2)
    c.level = m_obj.group(3)
    c.credit_hours = int(m_obj.group(4))

    prereq_str = m_obj.group(5)
    added_groups = prereq_str.split('and')

    for and_group in added_groups:
        and_group = and_group.strip()
        print(and_group)
        if 'or' in and_group:
            o = prereq.OrGroup(name=OR_GROUP).save()

            o.parent.connect(c)
            add_prereqs(o, and_group)
            # o.refresh()
            or_prereqs = o.prereq.all()

            # if there is more than 1 prereq in the or group
            # keep the group
            if len(or_prereqs) > 1:
                c.prereq.connect(o)

            # if there is only one prereq in the group directly
            # set that prereq as a prereq to the parent course
            # and delete the or group
            elif len(or_prereqs) == 1:
                add_prereqs(c, and_group)
                o.delete()

            # don't add anything as prereq if there are no
            # classes in the o
            else:
                o.delete()
        else:
            add_prereqs(c, and_group)

    return c


# data_str here is a string
def parse_course_bulletin(data_str, dept):
    # dept_str = re.search(r"Department of ([\w\s]+?): Course Descriptions", data_str).group(1)
    dept_str = 'Computer Science Engineering'
    dept.name = ABBREV_DICT[dept_str]
    dept.save()

    it = re.finditer(r"(\d{4})\s+([\w\s,:-]+?)\s+([UG]{1,2})\s+(\d).*?"
                     "Prereq: (.*?)\.", data_str, re.MULTILINE | re.DOTALL)

    count = 0
    for m_obj in it:
        # here we're passing a match object to parse course
        c = prereq.Course().save()
        dept.course.connect(c)
        c = parse_course(c, m_obj)
        c.save()

        count += 1
        # only run 10 times
        if count > 30:
            break

    return dept


def parse(data):
    uni = university.University(name='The Ohio State University').save()
    dept = department.Department().save()
    dept.uni.connect(uni)

    dept = parse_course_bulletin(data, dept)
    dept.save()


def get_course_bulletin():
    url = 'https://web.cse.ohio-state.edu/cgi-bin/' \
          'portal/report_manager/list.pl?r=12'

    r = requests.get(url)
    return r.text


if __name__ == '__main__':
    # course_bulletin = dept.get_course_bulletin()
    f = open('data')
    course_bulletin = f.read()
    parse(course_bulletin)

    # f = open('course_bulletin.json', 'w')
    # pretty_json = json.dumps(courses_json, \
    # sort_keys=True, indent=4, separators=(',', ': '))
    # f.write(courses_json)