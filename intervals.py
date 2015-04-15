import threading
import atexit

def test():
    """Test function. Prints "Hello World". Returns None"""
    print "Hello World"
    
def noop():
    """Test function. Does nothing."""
    pass

# Contains a list of active timeouts
timeouts = {}
# Contains a list of active intervals
intervals = {}

# Internally used counters.
_interval_ctr = 0
_timeout_ctr = 0

def _new_interval_id():
    """Used internally to return the next available interval ID."""
    global _interval_ctr
    _interval_ctr += 1
    return _interval_ctr

def _new_timeout_id():
    """Used internally to return the next available timeout ID."""
    global _timeout_ctr
    _timeout_ctr += 1
    return _timeout_ctr

def setTimeout(f,time):
    """Creates a Timer event that runs the function 'f' after 'time' (in milliseconds) duration.
    
    f: function to be called
    time: time in milliseconds after which f will be called.
    
    Returns: Timeout ID. Used by clearTimeout() to clear the timeout.
    """
    id = _new_timeout_id()
    def f_major():
        f()
        try:
            del timeouts[id]
        except KeyError:
            pass
    t = threading.Timer(1.0*time/1000,f_major)
    timeouts[id] = t
    t.start()
    return id

def setInterval(f,time):
    """Creates a Timer event that runs the function 'f' every 'time' milliseconds till cancelled.
    
    f: function to be called
    time: time in milliseconds after which f will be repeatedly called.
    
    Returns: Interval ID. Used by clearInterval() to clear the interval.
    """
    id = _new_interval_id()
    def f_major():
        f()
        t = threading.Timer(1.0*time/1000,f_major)
        intervals[id] = t
        t.start()
    t = threading.Timer(1.0*time/1000,f_major)
    intervals[id] = t
    t.start()
    return id

def clearInterval(id):
    """Cancels the Interval event with the specified ID."""
    intervals[id].cancel()
    try:
        del intervals[id]
    except KeyError:
        pass

def clearTimeout(id):
    """Cancels the Timeout event with the specified ID."""
    timeouts[id].cancel()
    try:
        del timeouts[id]
    except KeyError:
        pass

@atexit.register
def clearAll():
    """Clears all intervals/timeouts. Runs on exit."""
    for id in intervals:
        clearInterval(id)
    for id in timeouts:
        clearTimeout(id)


if __name__ == "__main__":
    print ("""Usage:
        
        import intervals
        
        id = intervals.setInterval(intervals.test, 2000)
        intervals.clearInterval(id)
    """)