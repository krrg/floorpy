from collections import namedtuple

Node = namedtuple("Node", [
    "t",
    "children",
    "padding",
    "room_indexes",
    "orientation",
    "order",
])
