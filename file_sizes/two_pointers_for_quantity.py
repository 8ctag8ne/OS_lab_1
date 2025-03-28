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

def get_file_percentage(total_count: int, l: int, r: int):
    return (r - l + 1) / total_count

def get_interval_with_min_borders(input_list: list[int], majority_coeff = 0.9):
    preffix_sum = create_preffix_sum(input_list)
    total_count = len(preffix_sum) - 1
    min_range = total_count
    res_l, res_r = 1, 1


    l, r = 1, 1
    for l in range(1, len(preffix_sum)):
        r = max(r, l)

        while r < len(input_list)  and get_file_percentage(total_count, l, r) < majority_coeff:
            r += 1;
        
        if r >= len(input_list):
            break

        if get_file_percentage(total_count, l, r) >= majority_coeff:
            if r < len(input_list) and input_list[r] - input_list[l] + 1 < min_range:
                min_range = input_list[r] - input_list[l] + 1
                res_l = l
                res_r = r

    return (res_l, res_r)


def get_graph_values_for_min_borders(input_list: list[int], majority_coeff = 0.9):
    input_list.sort()

    preffix_sum = create_preffix_sum(input_list)

    l, r = get_interval_with_min_borders(input_list, majority_coeff)
    result = []
    if (l > 1):
        result.append(get_relative_sum(preffix_sum, 1, l-1))
    result.append(get_relative_sum(preffix_sum, l, r))
    if (r < len(preffix_sum) - 1):
        result.append(get_relative_sum(preffix_sum, r + 1, len(preffix_sum) - 1))

    return result, input_list[l-1], input_list[r-1]

def get_answer(input_list: list[int], majority_coeff = 0.9):
    input_list.sort()

    l, r = get_interval_with_min_borders(input_list, majority_coeff)
    return f'Переважна більшість файлів ({get_file_percentage(len(input_list), l, r)*100}%) має розміри у діапазоні від {input_list[l-1]} до {input_list[r-1]}'


input_list = fh.get_sizes(fh.STATS_FILENAME)
print(get_answer(input_list))


