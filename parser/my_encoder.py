import json

from prereq import Course, OrGroup


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (OrGroup, Course)):
            return obj.to_dict()

        return super(MyEncoder, self).default(obj)