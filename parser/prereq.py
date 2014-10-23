import sys
import re
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)

class Prereq(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty()

    @staticmethod
    def print_prereq(prereq):
        sys.stdout.write('({0}, {1})'.format(prereq.dept, prereq.number))

    def print_prereqs(self):
        sys.stdout.write('[')
        sys.stdout.write(' ')
        for p in self.prereqs:
            if p.prereqs:
                Course.print_prereqs(p)
            else:
                Course.print_prereq(p)
            sys.stdout.write(' ')
        sys.stdout.write(']')
