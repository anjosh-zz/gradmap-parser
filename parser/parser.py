import re

def parse(prereq_data):
    m_obj = re.search(r"Prereq: (.*).", prereq_data);
    prereq_str = m_obj.group(1)
    print prereq_str

    added_groups = prereq_str.split('and')
    result = []
    or_list = []

    print str(added_groups)
    print 'ANDED groups:'
    for and_group in added_groups:
        and_group = and_group.strip()
        print '"' + str(and_group) + '"'
        if 'or' in and_group:
            print 'OR group found'
            or_list = add_courses(and_group, or_list)
            result.append(or_list)
        else:
            result = add_courses(and_group, result)

    result = filter(None, result)
    return result

def add_courses(courses, to_list):
    c_list = courses.split(',')
    for c in c_list:
        #TODO add match for course deptarment
        m = re.search(r"(\w)?\d{4}", c)
        if m:
            c = int(m.group())
            to_list.append(c)
    return to_list

if __name__=='__main__':
    tests = [ ("Prereq: 2231, 2331 (680), and 2421, and 3901 (560), 3902, or 3903.", [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]] ),
            ("Description: Formal languages and grammars; recursive descent parsing; data types, expressions, control structures, parameter passing; compilers and interpreters; memory management; functional programming principles. Prereq: 2231, 2331 (680), and 2421, and 3901 (560), 3902, or 3903. Not open to students with credit for 5341 (655).", [('CSE', 2231), ('CSE', 2331), ('CSE', 2421), [('CSE', 3901), ('CSE', 3902), ('CSE', 3903)]] ),
            ("2501 Social, Ethical, and Professional Issues in Computing U 1
Description: Social, ethical, and professional issues facing computing professionals; ethical principles; discussion of case studies. Prereq: 1222, 1223, 2231, 214, 222, or 230, and 2321 or Math 366, and Gen Ed Writing Level 2. Not open to students with credit for 5501 (601).", [[('CSE', 1222), ('CSE', 1223), ('CSE', 2231)], ('CSE', 2321), ('ENGR', 2367), ]

    for test, answer in tests:
        result = parse(test)
        if result == answer:
            print('GOOD: {0} => {1}'.format(test, answer))
        else:
            print('ERROR: {0} => {1} != {2}'.format(test, result, answer))
            break
