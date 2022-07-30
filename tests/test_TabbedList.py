from facades.parsers.TabbedList import TabbedList


def tests_tabbed_list_get():
    str = """
        Foo    :    Bar
        Zoo    :    123
    """
    assert TabbedList(str).get('Foo') == "Bar"
    assert TabbedList(str).get('Zoo') == "123"


def tests_tabbed_list_get_none():
    str = """
        Foo    :    Bar
        Zoo    :    123
    """
    assert TabbedList(str).get('Bad') is None


def tests_tabbed_list_get_bad_format():
    str = """
        Foo
        Zoo    :    123
        Boo    :    123    :   456
    """
    assert TabbedList(str).get('Zoo') == "123"
    assert TabbedList(str).get('Foo') is None
    assert TabbedList(str).get('Boo') is None


def tests_tabbed_list_all():
    str = """
        Foo    :    Bar
        Zoo    :    123
    """
    assert type(TabbedList(str).all()) is list
