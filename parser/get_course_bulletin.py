import urllib2
import parser

def get_course_bulletin():
    url = 'https://web.cse.ohio-state.edu/cgi-bin/'\
            'portal/report_manager/list.pl?r=12'

    usock = urllib2.urlopen(url)
    course_bulletin = usock.read()
    usock.close()
    return course_bulletin

if __name__=='__main__':
    f = open('course_bulletin', 'w')
    f.write(parser.parse(get_course_bulletin()))
