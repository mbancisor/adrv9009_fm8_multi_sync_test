"""Combine log data."""

import os
import pathlib
import shutil
from typing import List

import pandas as pd
from natsort import natsorted


def find_log_files(main_log_file: str) -> List[pathlib.Path]:
    """List all directorys."""
    valid_paths = []
    for path in pathlib.Path("./").iterdir():
        if path.is_dir():
            for _ in path.glob(f"{main_log_file}"):
                valid_paths.append(path)
    return valid_paths


if __name__ == '__main__':
    PHASE_LOG_NAME = 'phase_data.csv'
    TEMP_LOG_NAME = 'temp_data.csv'
    REG_LOG_NAME = 'hmc7044_regs_data.csv'

    if os.path.exists(f'./COMBINED_LOGS/{PHASE_LOG_NAME}'):
        os.remove(f'./COMBINED_LOGS/{PHASE_LOG_NAME}')

    pathlib.Path('./COMBINED_LOGS').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./COMBINED_LOGS/RAW_DATA').mkdir(parents=True, exist_ok=True)
    dirs = find_log_files(PHASE_LOG_NAME)
    path_str_list = [
        pathlib.Path(current_path_item) for current_path_item in natsorted(
            [str(current_path_item) for current_path_item in dirs])]
    phase_frames, temp_trames, reg_frames = [], [], []
    valid_dataset_path: List[pathlib.Path] = []
    RESTART_INDEX, CYCLE_RUN = 0, len(path_str_list)
    while CYCLE_RUN >= 1:
        try:
            # add datasets in a separate list
            for cycle_index, current_path in enumerate(path_str_list):
                phase_frames.append(
                    pd.read_csv(f"{current_path}/{PHASE_LOG_NAME}"))
                temp_trames.append(
                    pd.read_csv(f"{current_path}/{TEMP_LOG_NAME}"))
                reg_frames.append(
                    pd.read_csv(f"{current_path}/{REG_LOG_NAME}"))
                if len(valid_dataset_path) != 1:
                    valid_dataset_path.append(current_path)
                CYCLE_RUN -= 1

                for current_file_path in pathlib.Path(
                        f'./{current_path}/RAW_DATA').glob("*.csv"):
                    file_name = pathlib.Path(current_file_path).name
                    file_name_iteration = file_name.split('_')[1]
                    dir_name = pathlib.Path(current_path).name
                    if int(str(file_name_iteration)) == int(str(dir_name)):
                        shutil.copyfile(
                            current_file_path,
                            f"./COMBINED_LOGS/RAW_DATA/{file_name}")
                    else:
                        splited = file_name.split('_')
                        shutil.copyfile(
                            current_file_path,
                            "./COMBINED_LOGS/RAW_DATA/" +
                            f"{splited[0]}_{int(dir_name)}_{splited[2]}")

        except pd.errors.EmptyDataError:
            # if empty logs, remove that path, add 0 data and continue
            print(f"No data found at '{current_path}', add 0 data...")

            phase_data_frame = pd.read_csv(
                f"{valid_dataset_path[0]}/{PHASE_LOG_NAME}")
            phase_data_frame[:] = 0
            phase_frames.append(phase_data_frame)

            temp_data_frame = pd.read_csv(
                f"{valid_dataset_path[0]}/{TEMP_LOG_NAME}")
            temp_data_frame[:] = 0
            temp_trames.append(temp_data_frame)

            reg_data_frame = pd.read_csv(
                f"{valid_dataset_path[0]}/{REG_LOG_NAME}")
            reg_data_frame[:] = 0
            reg_frames.append(reg_data_frame)

            RESTART_INDEX = cycle_index
        path_str_list = path_str_list[RESTART_INDEX + 1:]
        if len(path_str_list) == 0:
            break
    pd.concat(phase_frames).to_csv(
        f'./COMBINED_LOGS/{PHASE_LOG_NAME}', index=False)
    pd.concat(temp_trames).to_csv(
        f'./COMBINED_LOGS/{TEMP_LOG_NAME}', index=False)
    pd.concat(reg_frames).to_csv(
        f'./COMBINED_LOGS/{REG_LOG_NAME}', index=False)
