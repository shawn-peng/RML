
from toolz import assoc

class temp_dict:
    def __init__(self, dict, k, v):
        self.k = k
        self.v = v
        self.dict = dict
        pass

    def __contains__(self, item):
        return item == self.k or item in self.dict

    def __getitem__(self, item):
        if item == self.k:
            return self.v
        else:
            return self.dict[item]

    def __setitem__(self, key, value):
        if key == self.k:
            return self.v
        else:
            self.dict[key] = value

    def __repr__(self):
        return "temp_dict: { %s: %s ; "%(self.k, self.v) + str(self.dict) + " }"
        # return str(dict(self))

    def merge(self):
        if isinstance(self.dict, temp_dict):
            self.dict.merge()
        self.dict[self.k] = self.v
        return self.dict





def temp_assoc(d, k, v):
    # return temp_dict(d, k, v)
    return assoc(d, k, v)
