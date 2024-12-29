from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"


def date_to_str(date: datetime) -> str:
    return date.strftime(DATE_FORMAT)


def iso_str_date_to_date(date: str) -> str:
    return datetime.fromisoformat(date).strftime(DATE_FORMAT)
