# timepy

[![Build Status](https://travis-ci.org/daniil-omelchenko/timepy.svg?branch=master)](https://travis-ci.org/daniil-omelchenko/timepy)
[![Coverage Status](https://coveralls.io/repos/github/daniil-omelchenko/timepy/badge.svg?branch=master)](https://coveralls.io/github/daniil-omelchenko/timepy?branch=master)
[![PyPI version](https://badge.fury.io/py/timepy.svg)](https://badge.fury.io/py/timepy)

The simplest ever library for measuring time of python code execution.

## Installation

```bash
pip install timepy
```

## How to use

```python
from timepy import Timer
```

### It's simple:

```python
t = Timer()

t.start()
# Your code which you want to measure
t.stop()
print(t.total_time)
```

You can give a name fro your timer:

```python
t = Timer('My second timer')
```

### Keep every moment you want

You can

```python
t = Timer()
t.start()
# Some heavy work 1
t.commit('Work 1 is done')
# Some heave work 2
t.commit('Work 2 is done')
t.stop()

print(t.events)

# will output:
# [<TimerStarted: 0.0 s>,
#  <TimerCommitted: 10.0 s (Work 1 is done)>,
#  <TimerCommitted: 20.0 s (Work 2 is done)>,
#  <TimerStopped: 20.001 s>]

```

### Measure your iterations

```python
t = Timer()
t.start
for i in some_list:
    # do heavy work
    t.lap()
t.stop()

print(t.laps[0])      # <Lap 0: 123 s>
print(t.laps)         # see all laps
print(t.average_lap)  # average lap duration
```
