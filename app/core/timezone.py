from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


def now_kst() -> datetime:
    """Return current datetime in KST."""
    return datetime.now(KST)


def today_kst():
    """Return today's date in KST."""
    return now_kst().date()
