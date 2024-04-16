from collections import Counter


class FileHandler:
    def find_split_in_csv(self, file_path: str) -> str:
        with open(file_path, "r", encoding="unicode_escape") as file:
            first_line = file.readline()
            possible_delimiters = [",", "\t", ";", "|"]
            delimiter_count: Counter = Counter()

            for delim in possible_delimiters:
                delimiter_count[delim] = first_line.count(delim)

            split_char = delimiter_count.most_common(1)[0][0]
            return split_char
