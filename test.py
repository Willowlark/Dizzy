class Test:
    pass

class Foo:
    pass

if __name__ == '__main__':
    import sys
    import inspect
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    print(clsmembers)