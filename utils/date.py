from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"


def str_to_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, DATE_FORMAT)


def date_to_str(date: datetime) -> str:
    return date.strftime(DATE_FORMAT)
