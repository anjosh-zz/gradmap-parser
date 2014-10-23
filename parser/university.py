from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, RelationshipFrom)

class University(StructuredNode):
    # TODO Might want to add more constraint properties latter
    name = StringProperty(unique_index=True)
    dept = RelationshipFrom('department.Department', 'BELONGS_TO')
