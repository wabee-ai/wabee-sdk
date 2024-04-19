from semantix_agents.tools.handlers.date_handler import DateHandler


class TestDateHandler:
    def test_should_return_the_current_timestamp_in_unix_timestamp(self) -> None:
        sut = DateHandler()

        assert isinstance(sut.get_timestamp(), int)
