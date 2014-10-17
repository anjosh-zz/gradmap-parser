import re
import jsonpickle
from pprint import pprint
import course
import deptartment

# Parser for Course Bulletin page (https://web.cse.ohio-state.edu/cgi-bin/portal/report_manager/list.pl?r=12)
# TODO might want to try parsing from CSE Semester Courses page (http://coe-portal.cse.ohio-state.edu/pdf-exports/CSE/) instead

# Special Class definitions
SECOND_WRIT = (2367, 'ENGR')

def parse(prereq_data):
    #depts = {}
    cse_dept = deptartment.Deptartment('CSE')
    it = re.finditer(r"(\d{4})\s+([\w\s,:-]+?)\s+([UG]{1,2})\s+(\d).*?" \
                            "Prereq: (.*?)\.", prereq_data, re.MULTILINE|re.DOTALL);
    count = 0
    for m_obj in it:
        count += 1
        number = m_obj.group(1)
        name = m_obj.group(2)
        level = m_obj.group(3)
        credits = m_obj.group(4)
        dept = 'CSE'
        #if dept not in depts:
        #    depts.add(dept)
        #cse_dept = dept.Dept('CSE')

        c = course.Course(number, dept, name, level, credits)
        prereq_str = m_obj.group(5)

        added_groups = prereq_str.split('and')
        prereqs = []
        or_list = []

        for and_group in added_groups:
            and_group = and_group.strip()
            if 'or' in and_group:
                or_list = add_prereqs(and_group, or_list)
                if len(or_list) == 1:
                    prereqs.append(or_list[0])
                else:
                    prereqs.append(or_list)
                or_list = []
            else:
                prereqs = add_prereqs(and_group, prereqs)

        # get rid of empty lists
        prereqs = filter(None, prereqs)

        c.prereqs = prereqs
        c.print_prereqs()
        pprint(vars(c))

        cse_dept.add_course(c)

        #### only run 10 times
        if count > 30:
            break
    
    pprint(vars(cse_dept))
    cse_dept_json = jsonpickle.encode(cse_dept, unpicklable=False)

    return cse_dept_json

def add_prereqs(prereqs, to_list):
    m = re.search(r"([A-Za-z]{3,4})", prereqs)
    if m:
        dept = m.group(1)
    else:
        dept = 'CSE'
    if dept != 'Not':
        c_list = prereqs.split(',')
        for c in c_list:
            if c == "Gen Ed Writing Level 2":
                to_list.append(course.Course(*SECOND_WRIT))
                #to_list = add_prereq(course.Course(*SECOND_WRIT))
            else:
                m = re.search(r"(\d{4})", c)
                if m:
                    number = int(m.group(1))
                    c = course.Course(number, dept.upper())
                    to_list.append(c)
                    #to_list.add_prereq(c)

    return to_list

#def add_prereq(self, prereq):
#    if self is None:
#        self.prereqs = list(prereq)
#    else:
#        self.prereqs.append(prereq)


if __name__=='__main__':
    f = open('data')
    prereq_data = f.read()
    tests = [
            #("Prereq: 2231, 2331 (680), and 2421, and 3901 (560), 3902, or 3903.", {('CSE', 3341): [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]]}),
            #("Description: Formal languages and grammars; recursive descent parsing; data types, expressions, control structures, parameter passing; compilers and interpreters; memory management; functional programming principles. Prereq: 2231, 2331 (680), and 2421, and 3901 (560), 3902, or 3903. Not open to students with credit for 5341 (655).", [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]]),
            #("2501 Social, Ethical, and Professional Issues in Computing U 1\nDescription: Social, ethical, and professional issues facing computing professionals; ethical principles; discussion of case studies. Prereq: 1222, 1223, 2231, 214, 222, or 230, and 2321 or Math 366, and Gen Ed Writing Level 2. Not open to students with credit for 5501 (601).", [[('CSE', 1222), ('CSE', 1223), ('CSE', 2231)], ('CSE', 2321), ('ENGR', 2367)]),
            (prereq_data, [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]]),
            ]

    for test, answer in tests:
        result = parse(test)
        if result == answer:
            print('GOOD: {0} => {1}'.format(test, answer))
        else:
            print('ERROR: {0} => {1} != {2}'.format(test, result, answer))
            break
