"""Test search."""
import inspect
import os
import sys
from typing import List


def extract_log_nr(
        log_lines: List[str], log_start_string: str,
        log_nr_search: int) -> List[str]:
    """Extract log."""
    start_split, end_split, next_log_nr_search = None, None, log_nr_search + 1
    for list_index, list_item in enumerate(log_lines):
        if list_item.count(f'{log_start_string}{log_nr_search} ') == 1:
            start_split = list_index
            break
    while end_split is None:
        for list_index, list_item in enumerate(log_lines):
            if list_item.count(
                    f'{log_start_string}{next_log_nr_search} ') == 1:
                end_split = list_index
                break
        next_log_nr_search += 1
        if next_log_nr_search - log_nr_search > 100:
            break
    new_log = log_lines[start_split:end_split]
    if start_split is None:
        new_log = log_lines[0:0]
    return new_log


if __name__ == '__main__':
    selected_path = os.path.dirname(os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))))
    search_stings = [
        'JESD 84a50000.axi-jesd204-rx:  0 0 0 0 0 0 0 0',
        'JESD 84a70000.axi-jesd204-rx:  0 0 0 0 0 0 0 0',
        'JESD 84a50000.axi-jesd204-rx:  Yes Yes Yes Yes Yes Yes Yes Yes',
        'JESD 84a70000.axi-jesd204-rx:  Yes Yes Yes Yes Yes Yes Yes Yes']
    expected_frequency = [2, 2, 4, 4]
    with open(f'{selected_path}/output.txt') as file_source:
        lines = file_source.readlines()
        last_run_log_lines = extract_log_nr(lines, 'run ', int(sys.argv[1]))
        for index, search_sting in enumerate(search_stings):
            COUNTED = 0
            for _, log_line in enumerate(last_run_log_lines):
                if log_line.count(search_sting) > 0:
                    COUNTED += 1
            if COUNTED == expected_frequency[index]:
                print(
                    f'{search_sting} found '
                    f'{expected_frequency[index]} time(s) as expected')
            else:
                print(
                    f'{search_sting} NOT found '
                    f'{expected_frequency[index]} time(s).')
                input('Press Enter to continue...')
