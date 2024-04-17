from tempfile import NamedTemporaryFile

from semantix_agent_tools.handlers.file_handler import FileHandler


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

    def test_should_build_the_file_path_for_storing_outputs(self) -> None:
        sut = FileHandler()

        assert (
            sut.get_outputfile_path("run_path", "path", "session_id")
            == "run_path/outputs/session_id/path"
        )
        assert (
            sut.get_outputfile_path("run_path", "outputs/path", "session_id")
            == "run_path/outputs/path"
        )

    def test_should_mount_file_url_based_on_the_file_path(self) -> None:
        sut = FileHandler()

        assert (
            sut.mount_file_url("run_path", "/file_path", "agent_name")
            == "https://agent_name.ml.semantixhub.com/v1/files/file_path"
        )