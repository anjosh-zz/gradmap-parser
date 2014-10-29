import pprint

import neomodel

import prereq


if __name__ == '__main__':
    # for standalone queries
    query = 'match (n:Course), (d:Department) where not (n)-[:REQUIRES]->(:Prereq)' \
            'and n.level = "U" and (n)-[:IN]->(d) return n, d'
    params = None
    results, meta = neomodel.db.cypher_query(query, params)
    starting_courses = [prereq.Course.inflate(row[0]) for row in results]
    pprint.pprint(starting_courses)

    print(starting_courses[0].name)
    print(starting_courses[0].__dict__)
    print(starting_courses[0].prereq.all())
    print(starting_courses[0].dept.all())
    # pprint.pprint(jsonpickle.encode(starting_courses[0]))
    # for s in starting_courses:
    # print(jsonpickle.encode(s, unpicklable=False))