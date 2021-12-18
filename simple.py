def example():
    a = 1
    b = 2
    d = 999
    c = use b:
        result = b + 1
        try:
            result += d
        except NameError:
            pass
        return result
    print(a, b, c)
example()
