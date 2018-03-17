# from collections import namedtuple
from recordclass import recordclass

Node = recordclass("Node", [
    "t",
    "children",
    "padding",
    "room_indexes",
    "orientation",
    "order",
    "score",
])


