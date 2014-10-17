import urllib2
import parser
import json

def get_course_bulletin():
    url = 'https://web.cse.ohio-state.edu/cgi-bin/'\
            'portal/report_manager/list.pl?r=12'

    usock = urllib2.urlopen(url)
    course_bulletin = usock.read()
    usock.close()
    return course_bulletin

if __name__=='__main__':
    f = open('course_bulletin', 'w')
    courses_json = parser.parse(get_course_bulletin())
    #pretty_json = json.dumps(courses_json, \
    #    sort_keys=True, indent=4, separators=(',', ': '))
    f.write(courses_json)
