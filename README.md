A quick-and-dirty proof of concept implementation of the `use` block described
in this video: https://www.youtube.com/watch?v=QM1iUe6IofM

This implementation has various shortcomings since it uses string matching
instead of a parser:
- If you use the word `use`, you might see "false positives" (lines
  incorrectly identified as the start of a `use` block). It isn't quite as bad
  as that: `use` must be a full word (e.g. `unused` and `dont_use_this()`
  won't trigger a `use` block) and the line must end with `:` in order to
  trigger a `use` block.
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
