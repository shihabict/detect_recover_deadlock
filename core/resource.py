class Resource:
    def __init__(self, rid):
        self.rid = rid
        self.allocated_to = None
        print(0)

    def __repr__(self):
        return f"Resource({self.rid}, allocated_to={self.allocated_to})"
