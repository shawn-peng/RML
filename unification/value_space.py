# import numpy as np
import tensorflow as tf
import math
#from number_relations import *

class ValueSet:
    def __init__(self):
        pass

class DiscreteSet(ValueSet):
    def __init__(self):
        super().__init__()
        pass

class CategorySet(DiscreteSet):
    def __init__(self):
        super().__init__()
        pass

class IDSet(DiscreteSet):
    def __init__(self):
        super().__init__()
        pass

class IntSet(DiscreteSet):
    def __init__(self):
        super().__init__()
        pass

class RealSimpleRange(ValueSet):
    def __init__(self, lo=-math.inf, hi=math.inf):
        super().__init__()
        self.lo = lo
        # self.includelo = includelo
        self.hi = hi
        # self.includehi = includehi

    def __gt__(self, other):
        if self.lo > other.lo:
            return True
        elif self.lo < other.lo:
            return False
        elif self.hi > other.hi:
            return True
        elif self.hi < other.hi:
            return False
        else:
            return False

    def __eq__(self, other):
        return self.hi == other.hi and self.lo == other.lo

    def __and__(self, other):
        if self.hi < other.hi:
            return self.hi > other.lo
        else:
            return other.hi > self.lo

    def __contains__(self, item):
        return self.lo <= item and self.hi > item

    def __str__(self):
        return "[%f,%f)"%(self.lo, self.hi)
    __repr__ = __str__


class RealRange(ValueSet):
    # def __init__(self, lo=-math.inf, hi=math.inf, includelo=True, includehi=False):
    def __init__(self, itv_list=None):
        super().__init__()
        if itv_list is None:
            self.intervals = [RealSimpleRange()]
            return
        prev_hi = None
        self.intervals = []
        for lo, hi in itv_list:
            if prev_hi is not None and lo <= prev_hi:
                raise ValueError()
            self.intervals.append(RealSimpleRange(lo,hi))
            prev_hi = hi

    def __contains__(self, X):
        for interval in self.intervals:
            if X in interval:
                return True
        return False

    def __eq__(self, other):
        itv_a = self.intervals
        itv_b = other.intervals

        na = len(itv_a)
        nb = len(itv_b)
        if na != nb:
            return False
        n = na

        for i in range(n):
            a = itv_a[i]
            b = itv_b[i]
            if a != b:
                return False

        return True

    def __ne__(self, other):
        itv_a = self.intervals
        itv_b = other.intervals

        na = len(itv_a)
        nb = len(itv_b)
        if na != nb:
            return True
        n = na

        for i in range(n):
            a = itv_a[i]
            b = itv_b[i]
            if a != b:
                return True

        return False

    def __invert__(self):
        itv = self.intervals
        n = len(itv)
        ret = RealRange([])

        start = -math.inf

        new_itv = ret.intervals
        for a in itv:
            if a.lo > start:
                new_itv.append(RealSimpleRange(start, a.lo))
            start = a.hi
        if math.inf > start:
            new_itv.append(RealSimpleRange(start, math.inf))

        return ret




    @classmethod
    def _merge_intervals(cls, itv_a, itv_b):
        # [1 4]
        # [2 3]
        # [1 3]
        # [2 4]
        # intervals = sorted(itv_a + itv_b)
        # single intervals don't have overlap
        intervals = []
        if not itv_a:
            return itv_b[:]
        if not itv_b:
            return itv_a[:]
        na = len(itv_a)
        nb = len(itv_b)
        i = 0
        j = 0
        a = itv_a[i]
        b = itv_b[j]
        while i < na and j < nb:
            if a.hi < b.hi:
                if a.hi < b.lo: # no intersection
                    intervals.append(a)
                #else: have intersection
                elif a.lo < b.lo: # a has part outside of b
                    b = RealSimpleRange(a.lo, b.hi)
                else:
                    # b = b
                    pass
                i += 1
                if i >= na:
                    intervals.append(b)
                    j += 1
                    while j < nb:
                        intervals.append(itv_b[j])
                        j += 1
                    break
                a = itv_a[i]
            else:
                if b.hi < a.lo: # no intersection
                    intervals.append(b)
                #else: have intersection
                elif b.lo < a.lo: # b has part outside of a
                    a = RealSimpleRange(b.lo, a.hi)
                else:
                    # b = b
                    pass
                j += 1
                if j >= nb:
                    intervals.append(a)
                    i += 1
                    while i < na:
                        intervals.append(itv_a[i])
                        i += 1
                    break
                b = itv_b[j]

        return intervals

    @classmethod
    def _intersect_intervals(cls, itv_a, itv_b):
        intervals = []
        if not itv_a or not itv_b:
            return intervals
        na = len(itv_a)
        nb = len(itv_b)
        i = 0
        j = 0
        a = itv_a[i]
        b = itv_b[j]
        while i < na and j < nb:
            if a.hi < b.hi:
                if a.hi > b.lo:
                    intervals.append(RealSimpleRange(max(a.lo, b.lo), a.hi))
                i += 1
                a = itv_a[i]
            else:
                if b.hi > a.lo:
                    intervals.append(RealSimpleRange(max(a.lo, b.lo), b.hi))
                j += 1
                if j >= nb:
                    break
                b = itv_b[j]
        return intervals

    @classmethod
    def _subtract_intervals(cls, itv_a, itv_b):
        intervals = []
        if not itv_a or not itv_b:
            return itv_a
        na = len(itv_a)
        nb = len(itv_b)
        i = 0
        j = 0
        a = itv_a[i]
        b = itv_b[j]
        while i < na and j < nb:
            if a.hi < b.hi:
                if a.hi > b.lo:
                    intervals.append(RealSimpleRange(a.lo, b.lo))
                else:
                    intervals.append(a)
                i += 1
                a = itv_a[i]
            else:
                if b.hi > a.lo:
                    intervals.append(RealSimpleRange(b.lo, a.lo))
                else:
                    intervals.append(b)
                j += 1
                b = itv_b[j]


    # union
    def __or__(self, b):
        new_range = RealRange()
        new_range.intervals = self._merge_intervals(self.intervals, b.intervals)
        return new_range

    # intersection
    def __and__(self, b):
        new_range = RealRange()
        new_range.intervals = self._intersect_intervals(self.intervals, b.intervals)
        return new_range

    # difference
    def __sub__(self, b):
        new_range = RealRange()
        new_range.intervals = self._intersect_intervals(self.intervals, b.intervals)
        return new_range

    # empty
    def __bool__(self):
        return bool(self.intervals)

    def __repr__(self):
        if not self.intervals:
            return "RealRange:\u03A6"
        return "RealRange:%s"%("U".join([str(itv) for itv in self.intervals]))

# a=RealRange([(0,1),(2,3),(4,5)])
# b=RealRange([(0,1),(2,3),(4,5)])
# print(a)
# # b=RealRange([(1,2),(3.1,3.3),(5,6)])
# print(b)
# print(a | b)
# print(a == b)
# print(a != b)
# print(~a)
# print(~a | b)
# print(~~a)
# print(~(~a | b) | a)

