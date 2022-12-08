GIVEN_FILE_NAME = "given_7.txt"
INPUT_FILE_NAME = "input_7.txt"


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name: str = name
        self.size: int = size

    def __repr__(self) -> str:
        return "- {} (file, size={})".format(self.name, self.size)


class Directory:
    def __init__(self, name: str = None, parent_directory: "Directory" = None) -> None:
        self.name: str = name if name is not None else ""
        self.parent_directory: Directory = parent_directory
        self.sub_directories: list[Directory] = []
        self.files: list[File] = []
        self.total_size: int = None
        self.total_size_outdated: bool = True

    def add_sub_directory(self, directory: "Directory") -> None:
        self.sub_directories.append(directory)
        self.total_size_outdated = True

    def add_file(self, file: File) -> None:
        self.files.append(file)
        self.total_size_outdated = True

    def get_subdirectory_by_name(self, name: str) -> "Directory":
        return next(filter(lambda dir: dir.name == name, self.sub_directories), None)

    def get_total_size(self) -> int:
        total_size: int = 0
        for sub_directory in self.sub_directories:
            total_size += sub_directory.get_total_size()
        for file in self.files:
            total_size += file.size
        self.total_size = total_size
        self.total_size_outdated = False
        return total_size

    def __hash__(self):
        # horrible hash, doesn't allow for same directory name chain to exist beyond depth of 2
        parent_directory_name = (
            "" if self.parent_directory is None else self.parent_directory.name
        )
        return hash(parent_directory_name + self.name)

    def __repr__(self) -> str:
        return "- {} (dir)".format(self.name)


class Solver:
    COMMAND_PREFIX = "$ "
    CHANGE_DIRECTORY_COMMAND = "cd "
    LIST_FILES_COMMAND = "ls"
    ROOT_DIRECTORY_DENOTION = "/"
    PARENT_DIRECTORY_DENOTION = ".."
    DIRECTORY_PREFIX = "dir "

    def parse_file(self, input_file_name: str) -> Directory:
        root_directory: Directory = Directory()
        current_directory: Directory = None
        is_within_list_files_command: bool = False
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                is_command: bool = (
                    stripped_line[: len(self.COMMAND_PREFIX)] == self.COMMAND_PREFIX
                )
                if is_command:
                    is_within_list_files_command = False
                    command = stripped_line[len(self.COMMAND_PREFIX) :]
                    is_change_directory_command: bool = (
                        command[: len(self.CHANGE_DIRECTORY_COMMAND)]
                        == self.CHANGE_DIRECTORY_COMMAND
                    )
                    is_list_files_command: bool = (
                        command[: len(self.LIST_FILES_COMMAND)]
                        == self.LIST_FILES_COMMAND
                    )
                    if is_change_directory_command:
                        directory_raw: str = command[
                            len(self.CHANGE_DIRECTORY_COMMAND) :
                        ]
                        if directory_raw == self.ROOT_DIRECTORY_DENOTION:
                            current_directory = root_directory
                        elif directory_raw == self.PARENT_DIRECTORY_DENOTION:
                            current_directory = current_directory.parent_directory
                        else:
                            current_directory = (
                                current_directory.get_subdirectory_by_name(
                                    directory_raw
                                )
                            )
                    elif is_list_files_command:
                        is_within_list_files_command = True
                elif is_within_list_files_command:
                    is_directory: bool = (
                        stripped_line[: len(self.DIRECTORY_PREFIX)]
                        == self.DIRECTORY_PREFIX
                    )
                    if is_directory:
                        directory_raw: str = stripped_line[len(self.DIRECTORY_PREFIX) :]
                        current_directory.add_sub_directory(
                            Directory(directory_raw, current_directory)
                        )
                    else:
                        file_size_raw, file_name_raw = stripped_line.split()
                        current_directory.add_file(
                            File(file_name_raw, int(file_size_raw))
                        )
        return root_directory

    def get_directories(
        self,
        root_directory: Directory,
        minimum_size: int = None,
        maximum_size: int = None,
    ):
        list_of_directories: list["Directory"] = []
        visited_directories: set["Directory"] = set([root_directory])
        directories_to_visit: list["Directory"] = root_directory.sub_directories
        for directory in directories_to_visit:
            visited_directories.add(directory)
            for sub_directory in directory.sub_directories:
                if sub_directory not in visited_directories:
                    directories_to_visit.append(sub_directory)
            directory_size: int = directory.get_total_size()
            if (maximum_size is None or directory_size <= maximum_size) and (
                minimum_size is None or directory_size >= minimum_size
            ):
                list_of_directories.append(directory)
        return list_of_directories


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        root_directory = solver.parse_file(input_file_name)
        directories: list["Directory"] = solver.get_directories(
            root_directory, None, 100000
        )
        total_size: int = sum(directory.get_total_size() for directory in directories)
        return total_size

    def test_given_1(self):
        total_size = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(total_size, 95437)

    def test_input_1(self):
        total_size = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(total_size, 1989474)

    def solve_2(self, input_file_name: str) -> int:
        TOTAL_SPACE_AVAILABLE: int = 70000000
        UNUSED_SPACE_NEEDED: int = 30000000
        solver = Solver()
        root_directory = solver.parse_file(input_file_name)
        current_unused_space: int = (
            TOTAL_SPACE_AVAILABLE - root_directory.get_total_size()
        )
        minimum_space_to_free: int = UNUSED_SPACE_NEEDED - current_unused_space
        directories: list["Directory"] = solver.get_directories(
            root_directory, minimum_space_to_free, None
        )
        directories.sort(key=lambda dir: dir.get_total_size())
        total_size = directories[0].get_total_size()
        return total_size

    def test_given_2(self):
        total_size = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(total_size, 24933642)

    def test_input_2(self):
        total_size = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(total_size, 1111607)


unittest.main(exit=False)
