from __future__ import annotations

import datetime
from calendar import monthrange


class DateDelta:
    def __init__(self, years: int = 0, quarters: int = 0, months: int = 0):
        """Initialize with years, quarters, and/or months."""
        self.years = years
        self.quarters = quarters
        self.months = months

    def _adjust_date(
        self, dt: datetime.datetime, direction: int = 1
    ) -> datetime.datetime:
        """Adjust date for month-end and invalid days, preserving time."""
        # Convert quarters to months (1 quarter = 3 months)
        total_months = direction * (
            self.years * 12 + self.quarters * 3 + self.months
        )
        new_month = dt.month + total_months
        # Handle year and month overflow
        year, month = divmod(new_month - 1, 12)
        new_year = dt.year + year
        new_month = month + 1
        # Cap day to the last day of the month (handles Feb 29, etc.)
        last_day = monthrange(new_year, new_month)[1]
        new_day = min(dt.day, last_day)
        # Preserve time components
        return datetime.datetime(
            new_year,
            new_month,
            new_day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
        )

    def __add__(self, other: datetime.datetime) -> datetime.datetime:
        """Support DateDelta + datetime."""
        if not isinstance(other, datetime.datetime):
            raise TypeError('Can only add DateDelta to datetime object')
        return self._adjust_date(other, direction=1)

    def __radd__(self, other: datetime.datetime) -> datetime.datetime:
        """Support datetime + DateDelta."""
        return self.__add__(other)

    def __sub__(self, other: datetime.datetime) -> datetime.datetime:
        """Support DateDelta - datetime (not typical, but included for symmetry)."""
        if not isinstance(other, datetime.datetime):
            raise TypeError('Can only subtract datetime from DateDelta')
        return self._adjust_date(other, direction=-1)

    def __rsub__(self, other: datetime.datetime) -> datetime.datetime:
        """Support datetime - DateDelta."""
        if not isinstance(other, datetime.datetime):
            raise TypeError('Can only subtract DateDelta from datetime')
        return self._adjust_date(other, direction=-1)

    def __repr__(self) -> str:
        return f'DateDelta(years={self.years}, quarters={self.quarters}, months={self.months})'
