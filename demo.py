# import pydevd
import types
import sys
import os
import traceback
from VarDumps import viewEntry


class CL:
    def __init__(self):
        self.s = "ab"
        self.n = 0
        self.a = 1
        self.d = {}

    def func(self, n):
        self.n = n
        print(n)


def main():
    a = (1, (2, (3, None)))
    b = a[1]
    cl = CL()
    cl.a = a
    cl.d['a'] = a
    cl.d['b'] = b

    st = set()
    st.add('a')
    st.add('b')
    st.add(a)
    st.add(b)

    viewEntry()
    return cl


if __name__ == "__main__":
    cl = main()
    # viewEntry()
