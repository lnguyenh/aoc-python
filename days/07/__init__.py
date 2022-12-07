class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = {}
        self.children = {}
        self.total_size = None

    def add_file(self, filename, size):
        self.files[filename] = size

    def add_child(self, directory_name):
        self.children[directory_name] = Directory(directory_name, self)

    def __str__(self):
        return f"Dir {self.name} [{self.files}] [{self.children}]"

    @property
    def files_size(self):
        return sum([size for _, size in self.files.items()])

    @property
    def children_size(self):
        return sum([child.get_total_size() for _, child in self.children.items()])

    def get_total_size(self):
        if self.total_size is None:
            self.total_size = self.files_size + self.children_size
        return self.total_size

    def get_part_1_value(self):
        current = self.total_size if self.total_size <= 100000 else 0
        return current + sum(
            [child.get_part_1_value() for _, child in self.children.items()]
        )

    def would_free_enough(self, to_free):
        return self.total_size >= to_free

    def get_part_2_value(self, to_free):
        values = [self.total_size] + [
            child.get_part_2_value(to_free)
            for _, child in self.children.items()
            if child.would_free_enough(to_free)
        ]
        return min(values)


def process_input(blob):
    lines = iter(blob.split("\n"))
    next(lines)
    root = Directory("/", None)
    current = root
    for line in lines:
        if line == "$ ls":
            continue
        line_items = line.split(" ")
        if len(line_items) == 2:
            value, name = line_items
            if value == "dir":
                current.add_child(name)
            else:
                current.add_file(name, int(value))
        else:
            _, instruction, name = line_items
            if instruction == "cd":
                if name == "..":
                    current = current.parent
                else:
                    current = current.children[name]
    return root


def do_part_1(root):
    root.get_total_size()
    return root.get_part_1_value()


def do_part_2(root):
    to_free = 30000000 - (70000000 - root.total_size)
    return root.get_part_2_value(to_free)
