#!/usr/bin/env python
"""BrainFuck interpreter, in python.

From: https://github.com/Thenerdstation/BrainFuck
"""
from __future__ import print_function
from __future__ import unicode_literals


import sys


# In case you done goof
class CompileException(Exception):
    """Comptile Exception
    """
    pass


class RuntimeException(Exception):
    """Runtime Exception
    """
    pass


def run(code):
    """Interpret the code.

    Args:
        code: Code string to execute.
    """
    # strip all of the non executable characters
    code = ''.join(c for c in code if c in '<>,.+-[]')

    # make sure while loops are correct
    brace_count = 0
    loop_stack = [] # queue for while loop jump 'pointers'
    loop_lookup = {} # dictionary to store the while loop jumps
    ## TODO: Convert this into:  for char, index in enumerate(code):
    for index in range(len(code)):
        if code[index] == '[':
            brace_count += 1
            loop_stack.append(index)
        elif code[index] == ']':
            brace_count -= 1
            # all looping pointers are stored in this dictionary.
            # since python dictionaries are O(1), this is the easiest option
            start = loop_stack.pop()
            loop_lookup[index] = start - 1
            loop_lookup[start] = index
        if brace_count < 0:
            raise CompileException('ERROR: Miss matched braces.')
    if brace_count:
        raise CompileException('ERROR: Expected another ] somewhere.')

    # Alright, lets start the actual program
    memory = [0]*30000 # as defined by Urban Meuller, who made BrainFuck
    mem_ptr = 0 # points to current block of memory
    ## TODO: Convert this into:  for char, index in enumerate(code):
    code_ptr = 0 # points to current executable byte
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
            if mem_ptr > 30000:
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
            memory[mem_ptr] = ord(sys.stdin.read(1))
        # loop start
        elif code[code_ptr] == '[':
            if memory[mem_ptr] == 0:
                code_ptr = loop_lookup[code_ptr]
        # loop ending
        elif code[code_ptr] == ']':
            code_ptr = loop_lookup[code_ptr]
        code_ptr += 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python BrainFuck.py <brain_fuck_source>')
        sys.exit()
    try:
        file_handle = open(sys.argv[1])
    except IOError:
        print('Error reading file "%s"' % sys.argv[1])
        sys.exit()
    code = file_handle.read()
    sys.exit(run(code))
