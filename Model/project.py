

class Project:
    def __init__(self, name, status, view_state, description):
        self.name = name
        self.status = status
        self.view_state = view_state
        self.description = description

    def __repr__(self):
        return "%s:%s;%s;%s" % (self.name, self.status, self.view_state, self.description)

    def __eq__(self, other):
        return (self.name == other.name and self.status == other.status and self.view_state == other.view_state and
                (self.description == other.description or self.description is None or other.description is None))
