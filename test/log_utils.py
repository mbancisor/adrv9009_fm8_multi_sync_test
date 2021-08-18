"""Log utils."""

import datetime
from os import makedirs, popen

import pandas as pd


def generate_file_timestamp() -> str:
    """Generate timestamp."""
    crt_time = datetime.datetime.now()
    hour, minute, second = crt_time.hour, crt_time.minute, crt_time.second
    year, month, day = crt_time.year, crt_time.month, crt_time.day
    timestamp = f'{day}-{month}-{year}_{hour}-{minute}-{second}'
    return timestamp


def save_data(
        input_data: dict, file_input: str, subdirectory: str = '') -> None:
    """Save data."""
    try:
        makedirs(subdirectory)
    except FileExistsError:
        pass
    data = {}
    for column_index, column_name in enumerate(input_data["column_names"]):
        data[column_name] = input_data["column_data"][column_index]
    current_data_frame = pd.DataFrame(data=data)
    current_data_frame.to_csv(f'{subdirectory}/{file_input}.csv', index=False)


def check_iio_data(command: str) -> str:
    """Check iio data."""
    stream = popen(command).read()
    return stream


if __name__ == "__main__":

    log_data = {
        "column_names": ['col 1', 'col 2', 'col 3'],
        "column_data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    }

    START_TIME = generate_file_timestamp()
    LOG_DIR = f'LOG_{START_TIME}'
    DATA_DIR = 'DATA_DIR'

    for iteration_index in range(2):
        save_data(log_data, f'test_{iteration_index}', f'{LOG_DIR}/{DATA_DIR}')
