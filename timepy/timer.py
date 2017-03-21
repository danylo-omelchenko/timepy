"""The simplest ever library for measuring time of python code execution."""
from datetime import datetime


class Timer:
    """Timer provide ability to measure execution time."""

    def __init__(self, name='no name'):
        """Crete new timer.

        Args:
            name (str): Name of the timer.
        """
        timers.append(self)
        self.name = name
        self.events = []
        self.laps = []
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start the timer.

        It will reset the timer.
        """
        self.start_time = datetime.now()
        self.events = []
        self.laps = []
        self.end_time = None
        self.events.append(TimerStarted(self.start_time, self.start_time))

    def lap(self):
        """Lap time from previous lap, timer start or timer commit."""
        lap_time = datetime.now()
        lap_index = len(self.laps)
        last_lap = [
            e.time
            for e in self.events
            if e.type in [TimerStarted, TimerLapped, TimerCommitted]
            ][-1]
        lap_duration = (lap_time - last_lap).total_seconds()
        lap = Lap(lap_index, lap_duration)
        self.laps.append(lap)
        self.events.append(TimerLapped(lap, self.start_time, lap_time))

    def commit(self, message):
        """Commit time point while timer is working.

        Args:
            message (str): Message associated with time point.
        """
        now = datetime.now()
        self.events.append(TimerCommitted(message, self.start_time, now))

    def stop(self):
        """Stop the timer."""
        self.end_time = datetime.now()
        self.events.append(TimerStopped(self.start_time, self.end_time))

    @property
    def total_time(self):
        """Duration from timer start to end in seconds."""
        return (self.end_time - self.start_time).total_seconds()

    @property
    def average_lap(self):
        """Average lap duration of the timer."""
        return sum(l.duration for l in self.laps) / len(self.laps)

    def __str__(self):
        """Convert to string."""
        return "Timer '{name}'".format(name=self.name)

    def __repr__(self):
        """Represent the instance."""
        return '<{}>'.format(self)


class Lap:
    """Timer's lap."""

    def __init__(self, index, duration):
        """Create new Lap object.

        Args:
            index (int): Index of lap in lap collection.
            duration (float): Duration of the lap in seconds.
        """
        self.index = index
        self.duration = duration

    def __str__(self):
        """Convert to string."""
        return 'Lap {index}: {duration} s'.format(
            index=self.index,
            duration=self.duration)

    def __repr__(self):
        """Represent the instance."""
        return '<{}>'.format(self)


class TimerEvent:
    """Base class of timer events."""

    def __init__(self, start_time, current_time):
        """Create instance of TimerEvent object.

        Args:
            start_time (datetime): Time when timer started.
            current_time (datetime): Time when current event occurred.
        """
        self.start_time = start_time
        self.time = current_time

    @property
    def type(self):
        """Type of timer event instance.

        Returns:
            type: type of instance.
        """
        return type(self)

    @property
    def relative_time(self):
        """Time from timer started in seconds."""
        return (self.time - self.start_time).total_seconds()

    def __str__(self):
        """Convert to string."""
        return '{type}: {time} s'.format(
            type=self.type.__name__,
            time=self.relative_time)

    def __repr__(self):
        """Represent the instance."""
        return '<{}>'.format(self)


class TimerStarted(TimerEvent):
    """Event occurred when timer starts."""


class TimerStopped(TimerEvent):
    """Event occurred when timer stops."""


class TimerCommitted(TimerEvent):
    """Event occurred when commit method called."""

    def __init__(self, message, *args):
        """Create new TimerCommitted object.

        Args:
            message (str): message associated with commit event.
            args (*): TimerEvent arguments.
        """
        super().__init__(*args)
        self.message = message

    def __str__(self):
        """Convert to string."""
        return '{type}: {time} s ({message})'.format(
            type=self.type.__name__,
            time=self.relative_time,
            message=self.message)


class TimerLapped(TimerEvent):
    """Event occurred when lap method called."""

    def __init__(self, lap, *args):
        """Create new TimerLapped object.

        Args:
            lap (Lap): Lap object for current lap event.
            args (*): TimerEvent arguments.
        """
        super().__init__(*args)
        self.lap = lap

    def __str__(self):
        """Convert to string."""
        return '{type}: {time} s ({lap})'.format(
            type=self.type.__name__,
            time=self.relative_time,
            lap=self.lap)


class TimerCollection(list):
    """Collection of timers."""

    def filter_by_name(self, pattern):
        """Get all timers which name contains pattern.

        Args:
            pattern (str): filtering pattern.

        Returns:
            list: List of timers or empty list.
        """
        return [t for t in self if pattern in t.name]

    def get_all_by_name(self, name):
        """Get all timers which name exactly equals given name.

        Args:
            name (str): name for search.

        Returns:
            list: List of timers or empty list.
        """
        return [t for t in self if t.name == name]

    def get_first_by_name(self, name):
        """Get first timer which name exactly equals given name.

        Args:
            name (str): name for search.

         Returns:
            Timer: timer or None.
        """
        res = self.get_all_by_name(name)
        if res:
            return res[0]


timers = TimerCollection()
