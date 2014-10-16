import re
import course
from pprint import pprint

# Parser for Course Bulletin page (https://web.cse.ohio-state.edu/cgi-bin/portal/report_manager/list.pl?r=12)
# TODO might want to try parsing from CSE Semester Courses page (http://coe-portal.cse.ohio-state.edu/pdf-exports/CSE/) instead

# Special Class definitions
SECOND_WRIT = (2367, 'ENGR')

def parse(prereq_data):
    m_obj = re.search(r"(\d{4}) ([\w\s,]+?) ([UG]{1,2}) (\d).*\n.*Prereq: (.*?)\.", prereq_data);
    print m_obj.groups()
    number = m_obj.group(1)
    name = m_obj.group(2)
    level = m_obj.group(3)
    credits = m_obj.group(4)
    dept = 'CSE'

    c = course.Course(number, dept, name, level, credits)
    prereq_str = m_obj.group(5)
    print prereq_str

    added_groups = prereq_str.split('and')
    prereqs = []
    or_list = []

    print str(added_groups)
    print 'ANDED groups:'
    for and_group in added_groups:
        and_group = and_group.strip()
        print '"' + str(and_group) + '"'
        if 'or' in and_group:
            print 'OR group found'
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

    return c.prereqs

def add_prereqs(prereqs, to_list):
    c_list = prereqs.split(',')
    for c in c_list:
        if c == "Gen Ed Writing Level 2":
            to_list.append(course.Course(*SECOND_WRIT))
        else:
            # might need to look for dept only at
            # beginning of group of prereqs 
            m = re.search(r"(\w{3,4})? ?(\d{4})", c)
            if m:
                dept = m.group(1)
                number = int(m.group(2))
                if dept:
                    c = course.Course(number, dept)
                else:
                    c = course.Course(number)
                to_list.append(c)
    return to_list

if __name__=='__main__':
    f = open('data')
    prereq_data = f.read()
    tests = [
            #("Prereq: 2231, 2331 (680), and 2421, and 3901 (560), 3902, or 3903.", {('CSE', 3341): [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]]}),
            #("Description: Formal languages and grammars; recursive descent parsing; data types, expressions, control structures, parameter passing; compilers and interpreters; memory management; functional programming principles. Prereq: 2231, 2331 (680), and 2421, and 3901 (560), 3902, or 3903. Not open to students with credit for 5341 (655).", [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]]),
            ("2501 Social, Ethical, and Professional Issues in Computing U 1\nDescription: Social, ethical, and professional issues facing computing professionals; ethical principles; discussion of case studies. Prereq: 1222, 1223, 2231, 214, 222, or 230, and 2321 or Math 366, and Gen Ed Writing Level 2. Not open to students with credit for 5501 (601).", [[('CSE', 1222), ('CSE', 1223), ('CSE', 2231)], ('CSE', 2321), ('ENGR', 2367)]),
            (prereq_data, [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]]),
            ]

    for test, answer in tests:
        result = parse(test)
        if result == answer:
            print('GOOD: {0} => {1}'.format(test, answer))
        else:
            print('ERROR: {0} => {1} != {2}'.format(test, result, answer))
            break
