import urllib2
from parser import parser
import json
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)

class Department(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty(unique_index=True)
    course = RelationshipFrom('course.Course', 'BELONGS_TO')
    uni = RelationshipTo('university.University', 'BELONGS_TO')

    def add_course(self, course):
        self.courses.append(course)

def get_course_bulletin():
    url = 'https://web.cse.ohio-state.edu/cgi-bin/'\
            'portal/report_manager/list.pl?r=12'

    usock = urllib2.urlopen(url)
    course_bulletin = usock.read()
    usock.close()
    return course_bulletin

if __name__=='__main__':
    f = open('course_bulletin.json', 'w')
    courses_json = parser.parse(get_course_bulletin())
    #pretty_json = json.dumps(courses_json, \
    #    sort_keys=True, indent=4, separators=(',', ': '))
    #f.write(courses_json)
