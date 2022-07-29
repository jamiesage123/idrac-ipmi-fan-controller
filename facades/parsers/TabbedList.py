class TabbedList:
    """
    Represents a facade for parsing IPMI Tool tabbed list output
    For example:
    Foo  :  Bar
    Zoo  :  456
    """

    def __init__(self, input):
        self.tabbedList = self.parse(input)

    """
    Parse a tabbed list
    """
    def parse(self, input):
        results = []

        for line in input.splitlines():
            results.append(list(map(lambda value: value.strip(), line.split(":"))))
        
        return results

    """
    Get a specific value by key
    """
    def get(self, key):
        for line in self.tabbedList:
            if (len(line) == 2 and line[0] == key):
                return line[1]
        return None

    """
    Get all items
    """
    def all(self):
        return self.tabbedList
