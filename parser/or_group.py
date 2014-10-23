class OrGroup(Prereq):
    prereq = RelationshipTo('Course', 'IN')

    def __init__:
        return OrNode(name='Or Group')
