from neomodel import (StructuredNode, StringProperty, RelationshipTo, RelationshipFrom)


class Department(StructuredNode):
    # TODO Might want to add more constraint properties later
    name = StringProperty(unique_index=True)
    course = RelationshipFrom('prereq.Course', 'IN')
    uni = RelationshipTo('university.University', 'IN')

    def to_dict(self):
        d = self.__dict__
        d['course'] = self.course.all()
        d['uni'] = self.uni.all()
        # pprint.pprint(d)
        return d