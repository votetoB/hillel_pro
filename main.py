def n_merge(l):
    ...
    # M
    # for element in l: O(N)
    #     do_smth()  #  O(1)
    #     find_minimum(l)  # O(N)
    #     find_minimum_tree(l)  # O(logN)

    # O(N^2)
    #
    # do_smth_else(l)  # O(N)
    # # O(1)


class A:

    def __getattr__(self, item):
        return A.my_dict[item]

    my_dict = {
        'weight': 50
    }

    def __init__(self, **kwargs):
        print("initializing with", **kwargs)

    @classmethod
    def my_constructor(cls, **kwargs):
        print(f"I am creating an object of class {cls.__name__}")
        return cls(**kwargs)

a = A()

x = a.weight

y = set()

x |= y

x = dict()

x[(3, 4)] = 4
x[A()] = 5


x[4] = 5

x = {
    "abc": 4,
    "abd": 7,
    "abe": "vasya",
    "abf": None,
    "abg": None,
}


import queue




"""
-10 "abc" 4
-9  "abd" 7
-8  "abe" "vasya"
-7 "abf" None
...
0 "abg" None
...
9
10
"""