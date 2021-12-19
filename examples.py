def example0():
    # - one parameter
    # - has return
    # - dedent to initial level
    a = 1
    b = 2
    c = use b:
        result = b + 1
        return result
    print(a, b, c)
example0()

def example1():
    # - two parameters
    # - no return
    # - dedent past initial level
    a = 1
    b = 2
    use a, b:
        c = b + 1
        print(a, b, c)
example1()

def example2():
    # no parameters: should raise exception
    a = 99
    use:
        try:
            print(a)
        except NameError:
            pass
        print(1, 2, 3)
example2()

def example3():
    # empty line inside block should be handled correctly
    a, b, c = use:
        my_list = [1, 2, 3]

        return my_list
    print(a, b, c)
example3()
