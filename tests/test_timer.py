"""Tests for timer.py."""
from datetime import datetime
import time

from timepy import Lap
from timepy import Timer
from timepy import TimerCollection
from timepy import TimerCommitted
from timepy import TimerEvent
from timepy import TimerLapped
from timepy import TimerStarted
from timepy import TimerStopped


def test_lap():
    """Test Lap class."""
    lap = Lap(0, 1)
    assert lap.index == 0
    assert lap.duration == 1
    assert str(lap) == 'Lap 0: 1 s'
    assert lap.__repr__() == '<Lap 0: 1 s>'


def test_event():
    """Test TimerEvent class."""
    event = TimerEvent(
        datetime(2017, 1, 1, 12, 0),
        datetime(2017, 1, 1, 12, 1))
    assert event.type == TimerEvent
    assert event.relative_time == 60.0
    assert str(event) == 'TimerEvent: 60.0 s'
    assert event.__repr__() == '<TimerEvent: 60.0 s>'


def test_event_0():
    """Test TimerEvent class."""
    event = TimerEvent(datetime(2017, 1, 1), datetime(2017, 1, 1))
    assert event.type == TimerEvent
    assert event.relative_time == 0.0
    assert str(event) == 'TimerEvent: 0.0 s'
    assert event.__repr__() == '<TimerEvent: 0.0 s>'


def test_timer_started():
    """Test TimerStarted class."""
    event = TimerStarted(datetime(2017, 1, 1), datetime(2017, 1, 1))
    assert event.type == TimerStarted
    assert event.relative_time == 0.0
    assert str(event) == 'TimerStarted: 0.0 s'
    assert event.__repr__() == '<TimerStarted: 0.0 s>'


def test_timer_stopped():
    """Test TimerStopped class."""
    event = TimerStopped(datetime(2017, 1, 1), datetime(2017, 1, 1))
    assert event.type == TimerStopped
    assert event.relative_time == 0.0
    assert str(event) == 'TimerStopped: 0.0 s'
    assert event.__repr__() == '<TimerStopped: 0.0 s>'


def test_timer_committed():
    """Test for TimerCommitted class."""
    event = TimerCommitted(
        'message', datetime(2017, 1, 1), datetime(2017, 1, 1))
    assert event.type == TimerCommitted
    assert event.relative_time == 0.0
    assert str(event) == 'TimerCommitted: 0.0 s (message)'
    assert event.__repr__() == '<TimerCommitted: 0.0 s (message)>'
    assert event.message == 'message'


def test_timer_lapped():
    """Test for TimerLapped class."""
    event = TimerLapped(Lap(2, 1), datetime(2017, 1, 1), datetime(2017, 1, 1))
    assert event.type == TimerLapped
    assert event.relative_time == 0.0
    assert str(event) == 'TimerLapped: 0.0 s (Lap 2: 1 s)'
    assert event.__repr__() == '<TimerLapped: 0.0 s (Lap 2: 1 s)>'
    assert event.lap.index == 2
    assert event.lap.duration == 1


def test_timer_create():
    """Test for Timer class."""
    t = Timer('name')
    assert t.name == 'name'
    assert t.start_time is None
    assert t.end_time is None
    assert t.laps == []
    assert t.events == []


def test_timer_start():
    """Test for Timer class."""
    t = Timer('name')
    t.start()
    assert t.start_time is not None
    assert t.end_time is None
    assert t.laps == []
    assert len(t.events) == 1
    assert t.events[0].type == TimerStarted


def test_timer_stop():
    """Test for Timer class."""
    t = Timer('name')
    t.start()
    time.sleep(0.01)
    t.stop()
    assert t.end_time > t.start_time
    assert t.laps == []
    assert len(t.events) == 2
    assert t.events[0].type == TimerStarted
    assert t.events[1].type == TimerStopped
    assert t.total_time > 0


def test_timer_commit():
    """Test for Timer class."""
    t = Timer('name')
    t.start()
    time.sleep(0.01)
    t.commit('message')
    assert t.events[0].relative_time < t.events[1].relative_time
    assert t.start_time is not None
    assert t.end_time is None
    assert t.laps == []
    assert len(t.events) == 2
    assert t.events[0].type == TimerStarted
    assert t.events[1].type == TimerCommitted
    assert t.events[1].message == 'message'


def test_timer_lap():
    """Test for Timer class."""
    t = Timer('name')
    t.start()
    t.lap()
    t.stop()
    assert t.start_time < t.end_time
    assert t.laps == [t.events[1].lap]
    assert len(t.events) == 3
    assert t.events[0].type == TimerStarted
    assert t.events[1].type == TimerLapped
    assert t.events[2].type == TimerStopped
    assert t.average_lap == t.laps[0].duration


def test_timer_no_name():
    """Test for Timer class."""
    t = Timer()
    assert t.name == 'no name'


def test_timer_str():
    """Test for Timer class."""
    t = Timer()
    assert str(t) == "Timer 'no name'"


def test_timer_repr():
    """Test for Timer class."""
    t = Timer()
    assert t.__repr__() == "<Timer 'no name'>"


def test_timer_collection_filter_by_name():
    """Test for TimerCollection.filter_by_name."""
    tc = TimerCollection([
        Timer('timer1'),
        Timer('timer2'),
        Timer('timer3'),
        Timer('other name')])

    assert len(tc.filter_by_name('timer')) == 3


def test_timer_collection_get_first_by_name():
    """Test for TimerCollection.get_first_by_name."""
    tc = TimerCollection([
        Timer('timer1'),
        Timer('timer2'),
        Timer('timer2'),
        Timer('timer3'),
        Timer('other name')])

    assert tc.get_first_by_name('timer2').name == 'timer2'


def test_timer_collection_get_all_by_name():
    """Test for TimerCollection.get_all_by_name."""
    tc = TimerCollection([
        Timer('timer1'),
        Timer('timer2'),
        Timer('timer2'),
        Timer('timer3'),
        Timer('other name')])

    assert len(tc.get_all_by_name('timer2')) == 2
