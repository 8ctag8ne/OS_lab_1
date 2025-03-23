import file_helper as fh

def get_sum(preffix_sum: list[int], l: int, r: int) -> int:
    l = max(l, 1)
    r = min(r, len(preffix_sum)-1)
    return preffix_sum[r] - preffix_sum[l-1]

def get_relative_sum(preffix_sum: list[int], l: int, r: int) -> int:
    l = max(l, 1)
    r = min(r, len(preffix_sum)-1)
    return (preffix_sum[r] - preffix_sum[l-1])/preffix_sum[-1]


def create_preffix_sum(original_list: list[int]) -> list[int]:
    preffix_sum = [0]+original_list.copy();

    for i in range(1, len(preffix_sum)):
        preffix_sum[i] += preffix_sum[i - 1]

    return preffix_sum;


def get_interval_with_min_count(preffix_sum: list[int], majority_coeff = 0.9):
    min_count = len(preffix_sum)
    res_l, res_r = 1, 1

    l, r = 1, 1
    for l in range(1, len(preffix_sum)):
        r = max(r, l)

        while r < len(preffix_sum)  and get_relative_sum(preffix_sum, l, r) < majority_coeff:
            r += 1;
        
        if r >= len(preffix_sum):
            break

        if get_relative_sum(preffix_sum, l, r) >= majority_coeff:
            if r - l + 1 < min_count:
                min_count = r - l + 1
                res_l = l
                res_r = r
    return (res_l, res_r)

def get_interval_with_min_range(preffix_sum: list[int], majority_coeff = 0.9):
    min_range = preffix_sum[-1]
    res_l, res_r = 1, 1

    l, r = 1, 1
    for l in range(1, len(preffix_sum)):
        r = max(r, l)

        while r < len(preffix_sum)  and get_relative_sum(preffix_sum, l, r) < majority_coeff:
            r += 1;
        
        if r >= len(preffix_sum):
            break

        if get_relative_sum(preffix_sum, l, r) >= majority_coeff:
            if get_sum(preffix_sum, l, r) < min_range:
                min_range = get_sum(preffix_sum, l, r);
                res_l = l
                res_r = r

    return (res_l, res_r)


def get_graph_values_for_min_range(input_list: list[int], majority_coeff = 0.9):
    input_list.sort()

    preffix_sum = create_preffix_sum(input_list)

    l, r = get_interval_with_min_range(preffix_sum, majority_coeff)
    result = []
    if (l > 1):
        result.append(get_relative_sum(preffix_sum, 1, l-1))
    result.append(get_relative_sum(preffix_sum, l, r))
    if (r < len(preffix_sum) - 1):
        result.append(get_relative_sum(preffix_sum, r + 1, len(preffix_sum) - 1))

    return result, input_list[l-1], input_list[r-1]


def get_graph_values_for_min_count(input_list: list[int], majority_coeff = 0.9):
    input_list.sort()

    preffix_sum = create_preffix_sum(input_list)

    l, r = get_interval_with_min_count(preffix_sum, majority_coeff)

    result = []
    relative_space = []
    if (l > 1):
        result.append(l-1)
        relative_space.append(get_relative_sum(preffix_sum, 1, l-1))
    result.append(r - l + 1)
    relative_space.append(get_relative_sum(preffix_sum, l, r))
    if (r < len(preffix_sum) - 1):
        result.append(len(preffix_sum) - r)
        relative_space.append(get_relative_sum(preffix_sum, r+1, len(preffix_sum) - 1))

    return result, l, r, relative_space

def get_answer(input_list: list[int], majority_coeff = 0.9):
    input_list.sort()

    preffix_sum = create_preffix_sum(input_list)

    l, r = get_interval_with_min_count(preffix_sum, majority_coeff)
    return f'Переважна більшість файлів ({get_relative_sum(preffix_sum, l, r)*100}%) має розміри у діапазоні від {input_list[l-1]} до {input_list[r-1]}'