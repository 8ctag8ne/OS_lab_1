def try_parse_as_int(input: str):
    try:
        number = int(input)
        return (True, number);
    except:
        return (False, 0);

def get_sizes(filename: str) -> list[int]:
    size_list = []
    with open(filename) as file:

        for line in file:
            size = try_parse_as_int(line.split(",")[1])
            if size[0]:
                size_list.append(size[1])

    return size_list


STATS_FILENAME = "OS_lab_1/file_size_sys.csv"