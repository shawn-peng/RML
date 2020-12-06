
from toolz import assoc
import textwrap

class temp_dict(dict):
    def __init__(self, d):
        super().__init__()
        # self.k = k
        # self.v = v
        self.dict = d
        # self[k] = v
        pass

    def __contains__(self, item):
        # return item == self.k or item in self.dict
        return item in self or item in self.dict

    def __getitem__(self, item):
        # if item == self.k:
        #     return self.v
        if item in self:
            return self[item]
        else:
            val = self.dict[item]
            self[item] = val
            return val

    def __setitem__(self, key, value):
        # if key == self.:
        #     return self.v
        self[key] = value # override old dict
        # if key in self:
        #     self[key] = value
        # elif key in self.dict:
        #     self.dict[key] = value

    def __repr__(self):
        # return "temp_dict: { %s: %s ; "%(self.k, self.v) + str(self.dict) + " }"
        return "<temp_dist: {\n" + ";\n".join(["%s: %s"%(k, v) for k, v in self.items()]) + \
            "\n" + textwrap.indent(str(self.dict), '\t') + "}>"
        # return str(dict(self))

    def merge(self):
        if isinstance(self.dict, temp_dict):
            self.dict.merge()
        self.dict.update(self)
        return self.dict





def temp_assoc(d, k, v):
    # return temp_dict(d, k, v)
    return assoc(d, k, v)
