import json

import neomodel

import prereq


if __name__ == '__main__':
    starting_dept = 'CSE'

    query = 'match (n:Course),  (d:Department) where not (n)-[:REQUIRES]->(:Prereq) and ' \
            'n.level = "U" and d.name = "{0}" and (n)-[:IN]->(d) return n'.format(starting_dept)
    results, meta = neomodel.db.cypher_query(query)
    starting_courses = [prereq.Course.inflate(row[0]) for row in results]

    f = open('../graph/static/output.json', 'w')

    starting_json = {"name": "CSE", "credit_hours": 10}
    children_arr = []
    for c in starting_courses:
        grand_children = c.parent.all()
        grand_children += c.orgroup.all()
        grand_children_arr = []
        for g in grand_children:
            grand_children_arr.append(g.to_dict())
        c_dict = c.to_dict()
        c_dict['children'] = grand_children_arr
        children_arr.append(c_dict)
    starting_json['children'] = children_arr
    f.write(json.dumps(starting_json, indent=4))