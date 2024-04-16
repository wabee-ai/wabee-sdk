from tempfile import NamedTemporaryFile

from semantix_agent_tools.files.file_handler import FileHandler


class TestFileHandler:
    def test_should_find_the_correct_separator_on_a_csv_file(self) -> None:
        sut = FileHandler()

        with NamedTemporaryFile() as f:
            f.write(b"x1,x2\na,1\nb,2\nc,3")
            f.seek(0)
            separator = sut.find_split_in_csv(f.name)

            assert separator == ","

    def test_should_find_the_correct_encoding_on_a_csv_file(self) -> None:
        sut = FileHandler()

        with NamedTemporaryFile() as f:
            f.write(b"x1,x2\na,1\nb,2\nc,3")
            f.seek(0)
            encoding = sut.find_encoding_csv(f.name)

            assert encoding == "ascii"
