# BrainFuck
Simple Brainfuck interpreter in python.
For Brainfuck information: https://en.wikipedia.org/wiki/Brainfuck

Stolen from: https://github.com/Thenerdstation/BrainFuck

## How to use:
You can use the Brainfuck program directly or import it as a library.

### For use as a library:
```python
import bf

# Accepts a single character and prints it back.
bf.execute(',.')
```

### For use directly:
```bash
$ ./bf.py <source_file.bf | code_string>
```
A source file should have a ".bf" extension.
A code string should be enclosed in quotation marks.

A simple "hello world" program has been added as an example.
### Example usage
```bash
$ ./bf.py HelloWorld.bf
Hello world!
```
