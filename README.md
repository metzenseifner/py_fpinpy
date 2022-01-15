# Description

This library provides a functional programming interface for Python.

# Result

The Result monad handles the three most common cases in
programming:

1. computation succeeded
2. computation failed
3. computation valid, but resulted in nothing

# Examples

```
from fpinpy import Result

startValue = Result.of(1).map(lambda x: x + 1).forEachOrFail(lambda x: print(x))
```

# Design

It is based on the work by Pierre-Yves Saumont in his books,
*Functional Programming in Java* (2017) and The Joy of Kotlin (2019).
