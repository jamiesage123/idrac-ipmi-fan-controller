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
            results.append(
                list(map(lambda value: value.strip(), line.split("|")))
            )

        return results

    """
    Get a specific value by key
    """

    def get(self, key):
        for line in self.tabbedTable:
            if len(line) > 1 and line[0] == key:
                if len(line) == 2:
                    # Key => value set up, return the value
                    return line[1]
                else:
                    # Key => multiple values, return all values as a list
                    values = line.copy()
                    del values[0]
                    return values
        return None

    """
    Get all items
    """

    def all(self):
        return self.tabbedTable
