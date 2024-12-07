# Python Notes

# Day 7

- you can have recursive generators, but they can be a little tricky.
  in particular, you probably want more imperative code since list
  comprehensions are in tension with them a little

# Day 6

- you can ignore parts of a tuple in an assignment with underscore

- modulus operator is '%' as you would expect

- pyrite type checking can use 'is None' checks to aid type inference

# Day 5

- python 3 sort functions take a 'key function' which generates a sort key for
  each item. Python 2 allowed a 'compare' function. There is a helper in
  functools to generate a key function from a compare function.

  - how does this work? how can this work? don\'t we have to create some
    synthetic key scale?
    [https://stackoverflow.com/questions/32752739/how-does-the-functools-cmp-to-key-function-work]

- there is a useful list of itertools recipes:
  https://docs.python.org/3/library/itertools.html#itertools-recipes
  - which includes flatten...
  - see also: https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/recipes.html

# Day 4

- str -> list is list(str), not s.split('')

- was reminded (on one abortive attempt to build all paths) that python list
  assignment gives two names to the list
  - use `a = b[:]` as an idiomatic copy
  - there is also a `.copy()` method

# Day 3

- Python has sum types!

- There is a newer alternative to NamedTuple - dataclasses.

- Regex/findall will return tuples if there are capturing groups in the regex.

- Test object type with `type(x) is Foo`.

- We need to write `flatten`

# Day 2

- We have `all` and `any` in base language.

# Day 1

- We need to write `transpose`
