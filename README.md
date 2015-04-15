# Javascript Timers in Python

This module allows Python users to use `setTimeout()` and `setInterval()` in their code.

I have not implemented `setImmediate()` because the only way to recreate functionality would be to have a `clearImmediate()` function that terminated a running thread. Killing a running thread is inherently unsafe, and, despite being possible, I don't think it's a good idea to implement it.

All timers are cleared at program exit.

### Usage

```python
import jstimers
from time import sleep

ctr = 0
def increment():
    global ctr
    ctr += 1

# Will increment ctr every 0.5 seconds.
intervalID = jstimers.setInterval(increment, 500)

def test(name):
    global ctr
    print ("Hello %s, %d" % (name,ctr))

# Will run after 2 seconds. Should have ctr = 3
timeoutID = jstimers.setTimeout(test, 2000, "World")

sleep(5)
```