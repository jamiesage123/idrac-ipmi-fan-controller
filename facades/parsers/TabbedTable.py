class TabbedTable:
    """
    Represents a facade for parsing IPMI Tool tabbed table output
    For example:
    Foo    |    Bar    |    123 
    Mar    |    Zoo    |    456 
    """

    def __init__(self, input):
        self.tabbedTable = self.parse(input)

    """
    Parse a tabbed table
    """
    def parse(self, input):
        results = []

        for line in input.splitlines():
            results.append(list(map(lambda value: value.strip(), line.split("|"))))
        
        return results

    """
    Get a specific value by key
    """
    def get(self, key):
        for line in self.tabbedTable:
            if (line[0] == key):
                return line[1]
        return None

    """
    Get all items
    """
    def all(self):
        return self.tabbedTable
