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

def example1():
    # - two parameters
    # - no return
    # - dedent past initial level
    a = 1
    b = 2
    use a, b:
        c = b + 1
        print(a, b, c)

def example2():
    # ignores enclosing scope
    a = 99
    use:
        try:
            print(a)
        except NameError:
            pass
        print(1, 2, 3)

def example3():
    # empty line inside block should be handled correctly
    a, b, c = use:
        my_list = [1, 2, 3]

        return my_list
    print(a, b, c)

def example4():
    # named use block
    a = 3
    a, b, c = use my_range(a):
        if a == 1:
            return [1]
        else:
            return my_range(a - 1) + [a]
    print(a, b, c)

def example5():
    # named use block with no params
    a, b, c = use my_range2():
        return [1, 2, 3]
    print(a, b, c)

def example6():
    # named use block with multiple params
    a = 1
    b = 2
    c = use get_c(a, b):
        return a + b
    print(a, b, c)

example0()
example1()
example2()
example3()
example4()
example5()
example6()
