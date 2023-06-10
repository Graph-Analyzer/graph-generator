class Edge:
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end


class _Node:
    def __init__(self, label: str, x: float, y: float):
        self.label = label
        self.x = x
        self.y = y


class _Edge:
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
