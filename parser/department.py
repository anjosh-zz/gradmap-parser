from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)

class Department(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty(unique_index=True)
    course = RelationshipFrom('course.Course', 'IS_FROM')

    def add_course(self, course):
        self.courses.append(course)
