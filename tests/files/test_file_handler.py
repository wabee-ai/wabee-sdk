from tempfile import NamedTemporaryFile

from semantix_agent_tools.files.file_handler import FileHandler


class TestFileHandler:
    def test_should_find_the_correct_separator_on_a_csv_file(self) -> None:
        sut = FileHandler()

        with NamedTemporaryFile() as f:
            f.write(b"x1,x2\na,1\nb,2\nc,3")
            separator = sut.find_split_in_csv(f.name)

            assert separator == ","
