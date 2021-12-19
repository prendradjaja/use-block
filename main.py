import sys
import re
import itertools
from types import SimpleNamespace as obj


def main():
    f = open(sys.argv[1])
    indent_string = '    '
    current_use = None
    uses = []

    lines = f.readlines()
    lines = itertools.chain(lines, [''])

    program_lines = []

    for lineno, line in enumerate(lines, start=1):
        line = line.rstrip('\n')
        if line.strip() == '':
            continue
        indent_level, line = parse_indentation(line, indent_string)
        parsed = parse_use_start(line)
        if parsed.is_use_start:
            if current_use:
                raise Exception("Nested use block not supported")
            current_use = parsed
            current_use.indent_level = indent_level
            current_use.body = []
        elif current_use:
            if indent_level > current_use.indent_level:  # Inside 'use'
                lineobj = obj(
                    text = line,
                    relative_indent_level = indent_level - current_use.indent_level,
                )
                current_use.body.append(lineobj)
            else:  # End of 'use'
                program_lines.append(generate_use_call(current_use, indent_string))
                program_lines.append(indent(line, indent_level, indent_string))
                uses.append(current_use)
                current_use = None
        else:
            program_lines.append(indent(line, indent_level, indent_string))

    for use in uses:
        print(generate_use_definition(use, indent_string), end='')
    if uses:
        print()

    for line in program_lines:
        print(line)


def generate_use_call(use, indent_string):
    # if use.assignment_target:
    # else:
    line = f'_use_block_{use.id}({", ".join(use.parameters)})'
    if use.assignment_target:
        line = use.assignment_target + ' = ' + line
    return indent(line, use.indent_level, indent_string)


def generate_use_definition(use, indent_string):
    result = f'def _use_block_{use.id}({", ".join(use.parameters)}):\n'
    for lineobj in use.body:
        result += indent(lineobj.text, lineobj.relative_indent_level, indent_string) + '\n'
    return result


def parse_indentation(line, indent_string):
    '''
    >>> indent_string = '    '
    >>> parse_indentation('x = 1', indent_string)
    (0, 'x = 1')
    >>> parse_indentation('    x = 1', indent_string)
    (1, 'x = 1')
    >>> parse_indentation('        x = 1', indent_string)
    (2, 'x = 1')
    '''
    level = 0
    while line.startswith(indent_string):
        level += 1
        line = line[len(indent_string):]
    return level, line


def indent(line, indent_level, indent_string):
    return (indent_string * indent_level) + line


def parse_use_start(line):
    match = re.search(r'\buse\b', line)
    if line.endswith('use:'):
        parameters = []
    elif line.endswith(':') and match:
        after_match = line[match.end():].strip()
        after_match = after_match[:-1]  # remove ':'
        parameters = [p.strip() for p in after_match.split(',')]
    else:
        return obj(is_use_start = False)

    before_match = line[:match.start()].strip()
    if before_match.endswith('='):
        assignment_target = before_match[:-1].strip()
    else:
        assignment_target = None

    return obj(
        is_use_start = True,
        id = next(ids),
        parameters = parameters,
        assignment_target = assignment_target
    )
ids = itertools.count()


if __name__ == '__main__':
    main()
