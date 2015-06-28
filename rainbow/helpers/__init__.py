def monkeypatch():
    from .dates import rrule_to_string

    from dateutil.rrule import rrule
    setattr(rrule, '__str__', rrule_to_string)
