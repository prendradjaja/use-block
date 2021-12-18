A quick-and-dirty proof of concept implementation of the `use` block described
in this video: https://www.youtube.com/watch?v=QM1iUe6IofM

This implementation has various shortcomings since it uses string matching
instead of a parser:
- If `use` is used as a variable or function name, you might see "false
  positives."
- The start of a `use` block must be a single line (no line continuation).
- Comments and multiline strings are not recognized (so `use` blocks inside
  these are not ignored).
- Possibly cryptic error messages for all of the above.

Note to future self: Probably don't sink a ton of time into fixing these --
better to do this properly. Maybe moshmosh, maybe extend the Python parser.

### What is this?

The `use` block is similar to an [IIFE][iife]: It allows arguments to be
passed in and can return a value. The difference is that the `use` block
(unlike the IIFE) does **not** see its enclosing scope.

Example:

```
$ cat simple.py
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
```

```
$ python3 main.py simple.py
def _use_block_0(b):
    result = b + 1
    try:
        result += d
    except NameError:
        pass
    return result

def example():
    a = 1
    b = 2
    d = 999
    c = _use_block_0(b)
    print(a, b, c)
example()
```

```
$ python3 main.py simple.py | python3
1 2 3
```

[iife]: https://en.wikipedia.org/wiki/Immediately_invoked_function_expression
