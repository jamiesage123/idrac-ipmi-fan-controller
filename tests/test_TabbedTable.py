from facades.parsers.TabbedTable import TabbedTable


def tests_tabbed_table_get():
    table = TabbedTable("""
        Foo    |    Bar
        Zoo    |    123
        Bob    |    123    |   789
    """)
    assert table.get('Foo') == "Bar"
    assert table.get('Zoo') == "123"
    assert type(table.get('Bob')) is list
    assert table.get('Bob')[0] == "123"
    assert table.get('Bob')[1] == "789"


def tests_tabbed_table_get_none():
    table = TabbedTable("""
        Foo    |    Bar
        Zoo    |    123
    """)
    assert table.get('Bad') is None


def tests_tabbed_table_get_bad_format():
    table = TabbedTable("""
        Foo
        Zoo    |    123
    """)
    assert table.get('Zoo') == "123"
    assert table.get('Foo') is None


def tests_tabbed_table_all():
    table = TabbedTable("""
        Foo    |    Bar
        Zoo    |    123
    """)
    assert type(table.all()) is list
