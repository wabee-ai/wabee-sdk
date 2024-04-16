from datetime import datetime


class DateHandler:
    def get_timestamp(self) -> int:
        return int(datetime.now().timestamp())
