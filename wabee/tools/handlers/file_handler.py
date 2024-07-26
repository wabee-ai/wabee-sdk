import os
from collections import Counter

import chardet


class FileHandler:
    __files_url: str

    def __init__(self) -> None:
        self.__files_url = os.getenv(
            "WABEE_AGENT_API",
            "https://{agent_name}.wabee.ai/core/v1/files",
        )

    def find_split_in_csv(self, file_path: str) -> str:
        with open(file_path, "r", encoding="unicode_escape") as file:
            first_line = file.readline()
            possible_delimiters = [",", "\t", ";", "|"]
            delimiter_count: Counter = Counter()

            for delim in possible_delimiters:
                delimiter_count[delim] = first_line.count(delim)

            split_char = delimiter_count.most_common(1)[0][0]
            return split_char

    def find_encoding_csv(self, file_path: str) -> str | None:
        with open(file_path, "rb") as rawdata:
            result = chardet.detect(rawdata.read(4096))
        return result["encoding"]

    def get_outputfile_path(
        self, run_path: str, path: str, session_id: str = ""
    ) -> str:
        if "outputs/" in path:
            return os.path.join(run_path, path)
        else:
            return os.path.join(run_path, "outputs", session_id, path)

    def mount_file_url(self, run_path: str, file_path: str, agent_name: str) -> str:
        return self.__files_url.format(agent_name=agent_name) + file_path.replace(
            run_path, ""
        )
