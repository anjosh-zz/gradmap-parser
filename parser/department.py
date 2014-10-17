from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)

class Department(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty(unique_index=True)
    number = IntegerProperty(index=True)
    course = RelationshipFrom('Course', 'IS_FROM')

    #def __init__(self, name):
    #    self.name = name
    #    self.courses = []
    #    super(Department, self).__init__(self, **args)

    def add_course(self, course):
        self.courses.append(course)
