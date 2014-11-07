import sys

import neomodel

import prereq

def cost(course):
    result = 0
    if not course.visited:
        if (not course.cost) or (course.cost == 0):
            print((course.name or str(course.number)) + " NO cost")
            if isinstance(course, prereq.Course):
                result = course.credit_hours or 3
                for p in course.prereq.all():
                    result += cost(p)
                for o in course.orgroup_prereq.all():
                    result += cost(o)
            else:
                cost_list = []
                for p in course.prereq.all():
                    cost_list.append(cost(p))
                result = min(cost_list)
        else:
            print((course.name or str(course.number)) + " has cost")
            result = course.cost
    course.visited = True
    course.cost = result
    course.save()
    return result

def cost2(course, visited):
    result = int()
    if course not in visited:
        visited.add(course)
        if isinstance(course, prereq.Course):
            result = course.credit_hours or 3
            for p in course.prereq.all():
                result += cost2(p, visited)
            for o in course.orgroup_prereq.all():
                result += cost2(o, visited)
        else:
            cost_list = []
            for p in course.prereq.all():
                cost_list.append(cost2(p, visited))
            result = min(cost_list)
    print("{0}: {1}".format(course.name or course.dept.all()[0].name + " " + str(course.number), result))
    if course not in visited: print("not visited")
    else: print("already visited")
    return result

if __name__ == '__main__':
    #course_num = sys.argv[1]
    #course = prereq.Course.nodes.get(number=course_num)
    for c in prereq.Course.nodes:
        c.cost = 0
        c.save()
        print(c.cost)
    for c in prereq.Course.nodes:
        if (not c.cost) or (c.cost == 0):
            for p in prereq.Prereq.nodes:
                p.visited = False
                p.save()
        print("{0}: {1}".format(c.dept.all()[0].name + " " + str(c.number), cost(c)))
        print
