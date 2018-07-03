#!/usr/bin/env python
"""BrainFuck interpreter, in python.

From: https://github.com/Thenerdstation/BrainFuck

You can use the Brainfuck program directly or import it as a library.
A simple "hello world" .bf file is included as an example.

For use as a library
====================
  #!/usr/bin/env python
  import bf
  # Accepts a single character keyboard input and prints it back.
  bf.execute(',.')

For use directly in shell (bash, for example):
=========================
  $ ./bf.py <source_file.bf | "code_string">

A source file should have a ".bf" extension.
  $ ./bf.py HelloWorld.bf
  Hello world!

A code string should be enclosed in quotation marks.
  $ ./bf.py ",."
  a
  a$
"""
from __future__ import print_function
from __future__ import unicode_literals


import sys


VALID_CODE_CHARS = '<>,.+-[]'
MEMORY_CELLS = 30000  # as defined by Urban Meuller, who made BrainFuck


# In case you done goof
class CompileException(Exception):
    """Compile Exception
    """
    pass


class RuntimeException(Exception):
    """Runtime Exception
    """
    pass


def _get_getch():
    """Get the implementation of getch() relevant for the system.

    Allows user to input one character, without needing return or enter.

    Returns:
        getch() implementation, as a function.
    """
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch
    # POSIX system. Create and return a getch that manipulates the tty.
    import tty
    def _getch():
        descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(descriptor)
        try:
            tty.setraw(descriptor)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(descriptor, termios.TCSADRAIN, old_settings)
        return char
    return _getch


def execute(code):
    """Interpret the code.

    Args:
        code: Code string to execute.

    Returns:
        Integer exit status; 0 for clean execution, non-zero otherwise.
        Currently only returns 0, throwing exceptions on errors.
    """
    getch = _get_getch()
    # strip all of the non executable characters
    code = ''.join(char for char in code if char in VALID_CODE_CHARS)
    # Initialize loops
    brace_count = 0
    loop_stack = []  # queue for while loop jump 'pointers'
    loop_lookup = {}  # dictionary to store all looping pointers.
    for index, char in enumerate(code):
        if char == '[':
            brace_count += 1
            loop_stack.append(index)
        elif char == ']':
            brace_count -= 1
            start = loop_stack.pop()
            loop_lookup[index] = start - 1
            loop_lookup[start] = index
        if brace_count < 0:
            raise CompileException('Mismatched braces at %s.' % index)
    if brace_count:
        raise CompileException('Missing close brace.')
    # run the code
    memory = [0] * MEMORY_CELLS
    mem_ptr = 0  # points to current block of memory
    code_ptr = 0  # points to current executable byte
    while code_ptr != len(code):
        # increment block
        if code[code_ptr] == '+':
            memory[mem_ptr] += 1
            if memory[mem_ptr] >= 256:
                raise RuntimeException('Integer Overflow')
        # decrement block
        elif code[code_ptr] == '-':
            memory[mem_ptr] -= 1
            if memory[mem_ptr] < 0:
                raise RuntimeException('Integer Underflow')
        # move pointer one block to the right
        elif code[code_ptr] == '>':
            mem_ptr += 1
            if mem_ptr > MEMORY_CELLS:
                raise RuntimeException('Over memory bounds')
        # move pointer one block to the left
        elif code[code_ptr] == '<':
            mem_ptr -= 1
            if mem_ptr < 0:
                raise RuntimeException('Under memory bounds')
        # write character
        elif code[code_ptr] == '.':
            sys.stdout.write(chr(memory[mem_ptr]))
        # read character
        elif code[code_ptr] == ',':
            memory[mem_ptr] = ord(getch())
            #memory[mem_ptr] = ord(sys.stdin.read(1))
        # loop start
        elif code[code_ptr] == '[':
            if memory[mem_ptr] == 0:
                code_ptr = loop_lookup[code_ptr]
        # loop ending
        elif code[code_ptr] == ']':
            code_ptr = loop_lookup[code_ptr]
        code_ptr += 1
    return 0


def main():
    """Direct execution function.
    """
    if '.bf' in sys.argv[1]:
        try:
            file_handle = open(sys.argv[1])
            code = file_handle.read()
        except IOError:
            RuntimeException('Could not read file "%s"' % sys.argv[1])
    else:
        code = sys.argv[1]
    execute(code)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:')
        print('    %s <source_file.bf | "code_string">' % sys.argv[0])
        sys.exit()
    sys.exit(main())
