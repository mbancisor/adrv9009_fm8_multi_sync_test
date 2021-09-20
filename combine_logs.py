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
    AQ_TEMP_LOG_NAME = 'temp_data_2.csv'
    all_logs = [
        'output.txt', 'log_jesd.txt', 'log_dmesg.txt',
        'log_jesd_slave.txt', 'log_dmesg_slave.txt']

    # if os.path.exists(f'./COMBINED_LOGS/{PHASE_LOG_NAME}'):
    #     os.remove(f'./COMBINED_LOGS/{PHASE_LOG_NAME}')

    if os.path.exists('./COMBINED_LOGS'):
        shutil.rmtree('./COMBINED_LOGS')

    pathlib.Path('./COMBINED_LOGS').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./COMBINED_LOGS/RAW_DATA').mkdir(parents=True, exist_ok=True)
    pathlib.Path(
        './COMBINED_LOGS/DIAGNOSTICS').mkdir(parents=True, exist_ok=True)

    search_logs_list = [
        PHASE_LOG_NAME, TEMP_LOG_NAME, REG_LOG_NAME, AQ_TEMP_LOG_NAME]

    for _, current_log_name in enumerate(search_logs_list):
        dirs = find_log_files(current_log_name)
        path_str_list = [
            pathlib.Path(current_path_item) for current_path_item in natsorted(
                [str(current_path_item) for current_path_item in dirs])]
        valid_dataset_path: List[pathlib.Path] = []

        if int(path_str_list[-1].name) != len(path_str_list) - 1:
            for dir_to_add in range(int(path_str_list[-1].name)):
                if not pathlib.Path.exists(pathlib.Path(f'{dir_to_add}')):
                    print(f'Missing {dir_to_add}')
                    pathlib.Path(
                        f'./{dir_to_add}').mkdir(parents=True, exist_ok=True)
                    pathlib.Path(
                        f'./{dir_to_add}/RAW_DATA').mkdir(
                            parents=True, exist_ok=True)
        else:
            nr_of_raw_data_files: List[int] = []
            for dir_to_scan in range(int(path_str_list[-1].name)):
                COUNT = 0
                for current_file_path in pathlib.Path(
                        f'./{dir_to_scan}/RAW_DATA').glob("*.csv"):
                    COUNT += 1
                nr_of_raw_data_files.append(COUNT)
                if len(nr_of_raw_data_files) > 1:
                    if nr_of_raw_data_files[-1] != nr_of_raw_data_files[0]:
                        print(
                            'Missing raw data file(s) from directory '
                            f'{dir_to_scan}')
                        for current_file_path in pathlib.Path(
                                f'./{dir_to_scan}').glob("*.csv"):
                            os.remove(current_file_path)

        if int(path_str_list[-1].name) == len(path_str_list) - 1:
            print(
                'Main data set is consistent, contain all expected '
                f'{current_log_name} logs')
        else:
            print(
                'Data set is NOT consistent, missing data from '
                f'{int(path_str_list[-1].name) - (len(path_str_list) - 1)} '
                'folder(s):')
            for _, log_name in enumerate(
                    [PHASE_LOG_NAME, TEMP_LOG_NAME, REG_LOG_NAME,
                     AQ_TEMP_LOG_NAME]):
                dirs = find_log_files(log_name)
                path_str_list = [
                    pathlib.Path(current_path_item) for current_path_item in
                    natsorted(
                        [str(current_path_item) for
                         current_path_item in dirs])]
                for dir_name_to_search in range(int(path_str_list[-1].name)):

                    if not pathlib.Path.exists(
                            pathlib.Path(f'{dir_name_to_search}/{log_name}')):
                        print(
                            f'Add dummy {log_name} file inside '
                            f'directory {dir_name_to_search}')
                        phase_data_frame = pd.read_csv(f"0/{log_name}")
                        phase_data_frame[:] = 0
                        pd.concat([phase_data_frame]).to_csv(
                            f'./{dir_name_to_search}/{log_name}', index=False)

                        for current_file_path in pathlib.Path(
                                './0/RAW_DATA').glob("*.csv"):
                            raw_data_frame = pd.read_csv(
                                f"0/RAW_DATA/{current_file_path.name}")
                            raw_data_frame[:] = 0
                            file_name = pathlib.Path(current_file_path).name
                            splited = file_name.split('_')
                            dummy_raw_path = \
                                f'./{dir_name_to_search}/RAW_DATA/' + \
                                f'{splited[0]}_{int(dir_name_to_search)}_' + \
                                f'{splited[2]}'
                            print(f'Add dummy {dummy_raw_path}')
                            pd.concat([raw_data_frame]).to_csv(
                                dummy_raw_path, index=False)

    dirs = find_log_files(PHASE_LOG_NAME)
    path_str_list = [
        pathlib.Path(current_path_item) for current_path_item in natsorted(
            [str(current_path_item) for current_path_item in dirs])]
    valid_dataset_path = []

    RESTART_INDEX, CYCLE_RUN = 0, len(path_str_list)
    phase_frames, temp_trames, reg_frames, aq_temp_trames = [], [], [], []
    while CYCLE_RUN >= 1:
        try:
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

                if pathlib.Path.exists(
                        pathlib.Path(
                            f'{current_path}/'
                            f'diag_report_run_{current_path}.tar.bz2')):
                    shutil.copyfile(
                        f'{current_path}/'
                        f'diag_report_run_{current_path}.tar.bz2',
                        './COMBINED_LOGS/DIAGNOSTICS/'
                        f'diag_report_run_{current_path}.tar.bz2')

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

                if pathlib.Path.exists(
                        pathlib.Path(f'{current_path}/{AQ_TEMP_LOG_NAME}')):
                    aq_temp_trames.append(
                        pd.read_csv(f"{current_path}/{AQ_TEMP_LOG_NAME}"))

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

            if pathlib.Path.exists(
                    pathlib.Path(
                        f'{valid_dataset_path[0]}/{AQ_TEMP_LOG_NAME}')):
                all_temp_data_frame = pd.read_csv(
                    f"{valid_dataset_path[0]}/{AQ_TEMP_LOG_NAME}")
                all_temp_data_frame[:] = 0
                aq_temp_trames.append(all_temp_data_frame)

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

    if pathlib.Path.exists(
            pathlib.Path(f'{valid_dataset_path[0]}/{AQ_TEMP_LOG_NAME}')):
        pd.concat(aq_temp_trames).to_csv(
            f'./COMBINED_LOGS/{AQ_TEMP_LOG_NAME}', index=False)

    pathlib.Path('./COMBINED_LOGS/RAW_DATA_tmp').mkdir(
        parents=True, exist_ok=True)
    shutil.move('./COMBINED_LOGS/RAW_DATA', './COMBINED_LOGS/RAW_DATA_tmp')
    shutil.move('./COMBINED_LOGS/RAW_DATA_tmp', './COMBINED_LOGS/RAW_DATA')
    shutil.make_archive(
        './COMBINED_LOGS/RAW_DATA', 'zip', './COMBINED_LOGS/RAW_DATA')
    shutil.rmtree('./COMBINED_LOGS/RAW_DATA')

    parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    try:
        for _, log_name in enumerate(all_logs):
            shutil.copy(os.path.join(parent_path, log_name), './COMBINED_LOGS')
    except FileNotFoundError:
        pass
