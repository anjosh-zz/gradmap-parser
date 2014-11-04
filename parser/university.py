from neomodel import (StructuredNode, StringProperty, RelationshipFrom)


class University(StructuredNode):
    # TODO Might want to add more constraint properties later
    name = StringProperty(unique_index=True)
    dept = RelationshipFrom('department.Department', 'IN')

    def to_dict(self):
        d = self.__dict__
        d['dept'] = self.dept.all()
        # pprint.pprint(d)
        return d