# Copyright (PHASE_MEAS) 2020-2021 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT,
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, INTELLECTUAL PROPERTY RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# type: ignore

import csv
import sys
from time import sleep
from typing import List

import adi
import log_utils
import matplotlib.pyplot as plt
import numpy as np


def measure_phase(chan0, chan1):
    assert len(chan0) == len(chan1)
    errorV = np.angle(chan0 * np.conj(chan1)) * 180 / np.pi
    error = np.mean(errorV)
    return error


if __name__ == "__main__":

    # Create radio
    RUN_EXTERNAL = True
    try:
        # check if external arguments are provided
        print(f'PRIMARY is set as {sys.argv[1]}')
        print(f'SECONDARY is set as {sys.argv[2]}')
        print(f'LOG_DIR is set as {sys.argv[3]}')
    except IndexError:
        # if external arguments are NOT provided (IndexError)
        # use the local defined ones
        PRIMARY = "ip:localhost"
        SECONDARY = "ip:10.48.65.96"
        START_TIME = log_utils.generate_file_timestamp()
        LOG_DIR = f'LOG_{START_TIME}'
        RUN_EXTERNAL = False
    else:
        # else use external provided arguments
        PRIMARY = sys.argv[1]
        SECONDARY = sys.argv[2]
        LOG_DIR = sys.argv[3]

    print(f'PRIMARY is set as: {PRIMARY}')
    print(f'SECONDARY is set as: {SECONDARY}')
    print(f'LOG_DIR is set as: {LOG_DIR}')
    print(f'RUN_EXTERNAL-{RUN_EXTERNAL}')

    # =========================================================================
    reg_value = []
    for index in range(2, 3):
        reg_value += [f'0x{index}'] * 10
    PRI_SOM = [f'iio_reg -u ip:localhost hmc7044 0x1A {value}'
               for value in reg_value]
    SEC_SOM = [f'iio_reg -u {SECONDARY} hmc7044 0x1A {value}'
               for value in reg_value]
    PRI_FMC8 = [f'iio_reg -u ip:localhost hmc7044-fmc 0x1A {value}'
                for value in reg_value]
    SEC_FMC8 = [f'iio_reg -u {SECONDARY} hmc7044-fmc 0x1A {value}'
                for value in reg_value]

    # PRI_SYS = PRI_SOM * int((int(LOG_DIR) / len(PRI_SOM)) + 1)
    # SEC_SYS = SEC_SOM * int((int(LOG_DIR) / len(SEC_SOM)) + 1)
    PRI_SYS = PRI_FMC8 * int((int(LOG_DIR) / len(PRI_FMC8)) + 1)
    SEC_SYS = SEC_FMC8 * int((int(LOG_DIR) / len(SEC_FMC8)) + 1)
    # =========================================================================
    reg_value = []
    # for index in range(25):  # 24 steps max
    # for index in range(0, 1):
    for index in range(0, 25, 6):  # 24 steps max
        reg_value += [hex(index)] * int(len(PRI_SOM))
    PRI_CAR_FINE_FMC8 = [f'iio_reg -u ip:localhost hmc7044-car 0x107 {value}'
                         for value in reg_value]
    SEC_CAR_FINE_FMC8 = [f'iio_reg -u {SECONDARY} hmc7044-car 0x107 {value}'
                         for value in reg_value]
    PRI_CAR_FINE_SOM = [f'iio_reg -u ip:localhost hmc7044-car 0xFD {value}'
                        for value in reg_value]
    SEC_CAR_FINE_SOM = [f'iio_reg -u {SECONDARY} hmc7044-car 0xFD {value}'
                        for value in reg_value]
    PRI_SYS_FINE = \
        PRI_CAR_FINE_FMC8 * int((int(LOG_DIR) / len(PRI_CAR_FINE_FMC8)) + 1)
    SEC_SYS_FINE = \
        SEC_CAR_FINE_FMC8 * int((int(LOG_DIR) / len(SEC_CAR_FINE_FMC8)) + 1)
    # PRI_SYS_FINE = \
    #     PRI_CAR_FINE_SOM * int((int(LOG_DIR) / len(PRI_CAR_FINE_SOM)) + 1)
    # SEC_SYS_FINE = \
    #     SEC_CAR_FINE_SOM * int((int(LOG_DIR) / len(SEC_CAR_FINE_SOM)) + 1)
    # =========================================================================
    reg_value = []
    # for index in range(2):  # 17 steps max
    # for index in range(12, 13):
    for index in range(18):  # 17 steps max
        reg_value += [hex(index)] * int(len(PRI_CAR_FINE_FMC8))
    PRI_CAR_COARSE_FMC8 = \
        [f'iio_reg -u ip:localhost hmc7044-car 0x108 {value}'
         for value in reg_value]
    SEC_CAR_COARSE_FMC8 = \
        [f'iio_reg -u {SECONDARY} hmc7044-car 0x108 {value}'
         for value in reg_value]
    PRI_CAR_COARSE_SOM = \
        [f'iio_reg -u ip:localhost hmc7044-car 0xFE {value}'
         for value in reg_value]
    SEC_CAR_COARSE_SOM = \
        [f'iio_reg -u {SECONDARY} hmc7044-car 0xFE {value}'
         for value in reg_value]
    PRI_SYS_COARSE = \
        PRI_CAR_COARSE_FMC8 * int(
            (int(LOG_DIR) / len(PRI_CAR_COARSE_FMC8)) + 1)
    SEC_SYS_COARSE = \
        SEC_CAR_COARSE_FMC8 * int(
            (int(LOG_DIR) / len(SEC_CAR_COARSE_FMC8)) + 1)
    # PRI_SYS_COARSE = \
    #     PRI_CAR_COARSE_SOM * int(
    #         (int(LOG_DIR) / len(PRI_CAR_COARSE_SOM)) + 1)
    # SEC_SYS_COARSE = \
    #     SEC_CAR_COARSE_SOM * int(
    #         (int(LOG_DIR) / len(SEC_CAR_COARSE_SOM)) + 1)
    # =========================================================================

    reg_value = []
    # for index in range(25):  # 24 steps max
    # for index in range(0, 1):
    for index in range(0, 25, 6):  # 24 steps max
        reg_value += [hex(index)] * int(len(PRI_SOM))
    PRI_CAR_FINE_FMC8_2 = [f'iio_reg -u ip:localhost hmc7044-car 0x125 {value}'
                           for value in reg_value]
    SEC_CAR_FINE_FMC8_2 = [f'iio_reg -u {SECONDARY} hmc7044-car 0x125 {value}'
                           for value in reg_value]
    PRI_CAR_FINE_SOM_2 = [f'iio_reg -u ip:localhost hmc7044-car 0xDF {value}'
                          for value in reg_value]
    SEC_CAR_FINE_SOM_2 = [f'iio_reg -u {SECONDARY} hmc7044-car 0xDF {value}'
                          for value in reg_value]
    PRI_SYS_FINE_2 = \
        PRI_CAR_FINE_FMC8_2 * \
        int((int(LOG_DIR) / len(PRI_CAR_FINE_FMC8_2)) + 1)
    SEC_SYS_FINE_2 = \
        SEC_CAR_FINE_FMC8_2 * \
        int((int(LOG_DIR) / len(SEC_CAR_FINE_FMC8_2)) + 1)
    # PRI_SYS_FINE_2 = \
    #     PRI_CAR_FINE_SOM_2 * \
    #     int((int(LOG_DIR) / len(PRI_CAR_FINE_SOM_2)) + 1)
    # SEC_SYS_FINE_2 = \
    #     SEC_CAR_FINE_SOM_2 * \
    #     int((int(LOG_DIR) / len(SEC_CAR_FINE_SOM_2)) + 1)
    # =========================================================================
    reg_value = []
    # for index in range(2):  # 17 steps max
    # for index in range(12, 13):
    # for index in range(14, 18):  # 17 steps max
    for index in range(18):  # 17 steps max
        reg_value += [hex(index)] * int(len(PRI_CAR_FINE_FMC8_2))
    PRI_CAR_COARSE_FMC8_2 = \
        [f'iio_reg -u ip:localhost hmc7044-car 0x126 {value}'
         for value in reg_value]
    SEC_CAR_COARSE_FMC8_2 = \
        [f'iio_reg -u {SECONDARY} hmc7044-car 0x126 {value}'
         for value in reg_value]
    PRI_CAR_COARSE_SOM_2 = \
        [f'iio_reg -u ip:localhost hmc7044-car 0xE0 {value}'
         for value in reg_value]
    SEC_CAR_COARSE_SOM_2 = \
        [f'iio_reg -u {SECONDARY} hmc7044-car 0xE0 {value}'
         for value in reg_value]
    PRI_SYS_COARSE_2 = \
        PRI_CAR_COARSE_FMC8_2 * int(
            (int(LOG_DIR) / len(PRI_CAR_COARSE_FMC8_2)) + 1)
    SEC_SYS_COARSE_2 = \
        SEC_CAR_COARSE_FMC8_2 * int(
            (int(LOG_DIR) / len(SEC_CAR_COARSE_FMC8_2)) + 1)
    # PRI_SYS_COARSE_2 = \
    #     PRI_CAR_COARSE_SOM_2 * int(
    #         (int(LOG_DIR) / len(PRI_CAR_COARSE_SOM_2)) + 1)
    # SEC_SYS_COARSE_2 = \
    #     SEC_CAR_COARSE_SOM_2 * int(
    #         (int(LOG_DIR) / len(SEC_CAR_COARSE_SOM_2)) + 1)
    # =========================================================================

    # Set to False when used without FMCOMMS8
    HAS_FMCOMMS8 = True

    LO_FREQ = 1000000000
    DDS_FREQ = 7000000

    primary_jesd = adi.jesd(PRIMARY)
    secondary_jesd = adi.jesd(SECONDARY)

    print("--Connecting to devices")
    multi = adi.adrv9009_zu11eg_multi(
        PRIMARY, [SECONDARY], primary_jesd,
        [secondary_jesd], fmcomms8=HAS_FMCOMMS8)

    multi._dma_show_arming = False
    multi._jesd_show_status = True
    multi._jesd_fsm_show_status = True
    multi._clk_chip_show_cap_bank_sel = True
    multi._resync_tx = True
    multi.rx_buffer_size = 2 ** 10

    multi.hmc7044_ext_output_delay(0, 1, 0)
    multi.hmc7044_ext_output_delay(2, 5, 0)

    multi.hmc7044_car_output_delay(2, 2, 0)
    multi.hmc7044_car_output_delay(3, 2, 0)

    # multi.hmc7044_set_cap_sel([14, 14, 14, 13, 13, 14, 13])

    if HAS_FMCOMMS8:
        enabled_channels = [0, 2, 4, 6]
        DDS_SINGLE_TONE_CHANNEL = 4
    else:
        enabled_channels = [0, 1, 2, 3]
        DDS_SINGLE_TONE_CHANNEL = 0

    multi.primary.rx_enabled_channels = enabled_channels

    for secondary in multi.secondaries:
        secondary.rx_enabled_channels = enabled_channels
        secondary.dds_single_tone(DDS_FREQ, 0.2, DDS_SINGLE_TONE_CHANNEL)

    multi.set_trx_lo_frequency(LO_FREQ)
    multi.primary.dds_single_tone(DDS_FREQ, 0.8)

    log = [[], [], [], [], [], [], []]

    ACQUISITION_CYCLES = 8  # (N)
    PHASE_MEAS = 7  # (C)
    ITERATIONS = 1  # (R)

    PLOT_TIME = False

    phase_meas = np.zeros([PHASE_MEAS, ACQUISITION_CYCLES])  # (rx)
    mean_phase_meas = np.zeros([PHASE_MEAS, ITERATIONS])  # (rx_m)
    variance_phase_meas = np.zeros([PHASE_MEAS, ITERATIONS])  # (rx_v)
    min_phase_meas = np.zeros([PHASE_MEAS, ITERATIONS])
    max_phase_meas = np.zeros([PHASE_MEAS, ITERATIONS])

    temperature_meas = np.zeros([8, ITERATIONS])
    hmc7044_regs = [['' for _ in range(ITERATIONS)] for _ in range(6)]
    temperature_meas_2 = np.zeros([8, ITERATIONS * 8])

    if HAS_FMCOMMS8:
        chan_desc = [
            "Across Chip (A) (C0-C1)",
            "Across FMC8 (A) (C0-C2)",
            "Across Chip (B) (C4-C5)",
            "Across FMC8 (B) (C4-C6)",
            "Across SoM (AB) (C0-C4)",
            "Across FMC8 (AB) (C2-C6)",
            "Across SoM-FMC8 (AB) (C0-C6)",
        ]
    else:
        chan_desc = [
            "Same Chip (A)",
            "Across Chip (A)",
            "Same Chip (B)",
            "Across Chip (B)",
            "Across SoM (AB)",
        ]

    RAW_DATA_DIR = 'RAW_DATA'

    log_data, log_data_imag = {}, {}

    for itr_index in range(ITERATIONS):
        print("\n\nIteration#", itr_index)
        multi._rx_initialized = False

        PLOT_TIME = True
        DATA_OFFSET = 400

        # PRYMARY SYSTEM ====================================================
        # log_utils.check_iio_data(PRI_SYS[int(LOG_DIR)])
        # print('primary fmc8 (reg 0x1A):')
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-fmc 0x1A').rstrip())

        # log_utils.check_iio_data(PRI_SYS_FINE[int(LOG_DIR)])
        # print('primary carrier sync fine (reg 0x107):')  # fine delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0x107').rstrip())
        # print('primary carrier sync fine (reg 0xFD):')  # fine delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0xFD').rstrip())

        # log_utils.check_iio_data(PRI_SYS_COARSE[int(LOG_DIR)])
        # print('primary carrier sync coarse (reg 0x108):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0x108').rstrip())
        # print('primary carrier sync coarse (reg 0xFE):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0xFE').rstrip())

        # log_utils.check_iio_data(PRI_SYS[int(LOG_DIR)])
        # print('primary som (reg 0x1A):')  # charge pump current som
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044 0x1A').rstrip())

        # log_utils.check_iio_data(PRI_SYS[int(LOG_DIR)])
        # print('primary fmc8 (reg 0x1A):')  # charge pump current som
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-fmc 0x1A').rstrip())

        # log_utils.check_iio_data(PRI_SYS_FINE_2[int(LOG_DIR)])
        # print('primary carrier sync fine (reg 0x107):')  # fine delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0x107').rstrip())
        # print('primary carrier sync fine (reg 0xFD):')  # fine delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0xFD').rstrip())
        # print('primary carrier sync fine (reg 0x125):')  # fine delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0x125').rstrip())
        # print('primary carrier sync fine (reg 0xDF):')  # fine delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0xDF').rstrip())

        # log_utils.check_iio_data(PRI_SYS_COARSE_2[int(LOG_DIR)])
        # print('primary carrier sync coarse (reg 0x108):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0x108').rstrip())
        # print('primary carrier sync coarse (reg 0xFE):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0xFE').rstrip())
        # print('primary carrier sync coarse (reg 0x126):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0x126').rstrip())
        # print('primary carrier sync coarse (reg 0xE0):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0xE0').rstrip())

        # SECONDARY SYSTEM ==================================================
        # print('secondary carrier (reg 0x1A):')  # charge pump current carrier
        # print(log_utils.check_iio_data(
        #     f'iio_reg -u {SECONDARY} hmc7044-car 0x1A').rstrip())

        # log_utils.check_iio_data(SEC_SYS_FINE[int(LOG_DIR)])
        # print('secondary carrier sync fine (reg 0x107):')  # fine delay
        # print(log_utils.check_iio_data(
        #     f'iio_reg -u {SECONDARY} hmc7044-car 0x107').rstrip())
        # print('secondary carrier sync fine (reg 0xFD):')  # fine delay
        # print(log_utils.check_iio_data(
        #     f'iio_reg -u {SECONDARY} hmc7044-car 0xFD').rstrip())

        # log_utils.check_iio_data(SEC_SYS_COARSE[int(LOG_DIR)])
        # print('secondary carrier sync coarse (reg 0x108):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     f'iio_reg -u {SECONDARY} hmc7044-car 0x108').rstrip())
        # print('secondary carrier sync coarse (reg 0xFE):')  # coarse delay
        # print(log_utils.check_iio_data(
        #     f'iio_reg -u {SECONDARY} hmc7044-car 0xFE').rstrip())

        # log_utils.check_iio_data(SEC_SYS[int(LOG_DIR)])
        # print('secondary som (reg 0x1A):')  # charge pump current som
        # print(log_utils.check_iio_data(
        #     f'iio_reg -u {SECONDARY} hmc7044 0x1A').rstrip())

        # log_utils.check_iio_data(SEC_SYS[int(LOG_DIR)])
        # print('secondary fmc8 (reg 0x1A):')  # charge pump current som
        # print(log_utils.check_iio_data(
        #     f'iio_reg -u {SECONDARY} hmc7044-fmc 0x1A').rstrip())

        # [0, 2, 4, 6][0, 2, 4, 6]
        # [0, 1, 2 ,3, 4, 5, 6, 7]

        # input('Set Scope, then ENTER to continue')
        # log_utils.check_iio_data(
        #     'iio_reg -u ip:localhost hmc7044-car 0x108 0x0')

        # input('Start Scope, then ENTER to continue')

        print(
            'iio_attr -D hmc7044-ext status',
            log_utils.check_iio_data(
                'iio_attr -D hmc7044-ext status').rstrip())

        print(
            'iio_attr -D hmc7044-car status',
            log_utils.check_iio_data(
                'iio_attr -D hmc7044-car status').rstrip())
        print(
            'iio_attr -D hmc7044 status',
            log_utils.check_iio_data(
                'iio_attr -D hmc7044 status').rstrip())
        print(
            'iio_attr -D hmc7044-fmc status',
            log_utils.check_iio_data(
                'iio_attr -D hmc7044-fmc status').rstrip())

        print(
            'iio_attr -D -u ip:10.48.65.98 hmc7044-car status',
            log_utils.check_iio_data(
                'iio_attr -D -u ip:10.48.65.98 hmc7044-car status').rstrip())
        print(
            'iio_attr -D -u ip:10.48.65.98 hmc7044 status',
            log_utils.check_iio_data(
                'iio_attr -D -u ip:10.48.65.98 hmc7044 status').rstrip())
        print(
            'iio_attr -D -u ip:10.48.65.98 hmc7044-fmc status',
            log_utils.check_iio_data(
                'iio_attr -D -u ip:10.48.65.98 hmc7044-fmc status').rstrip())

        for acq_index in range(ACQUISITION_CYCLES):
            received = multi.rx()

            # generate column names
            log_data["column_names"] = [
                f'channel_{index}' for index in range(len(received))]
            log_data_imag["column_names"] = [
                f'channel_{index}' for index in range(len(received))]
            # add column data
            received_real, received_imag = [], []
            for _, channel_raw_data in enumerate(received):
                received_real.append(channel_raw_data.real)
                received_imag.append(channel_raw_data.imag)
            log_data["column_data"] = received_real
            log_data_imag["column_data"] = received_imag
            # write data in log
            if RUN_EXTERNAL is True:
                log_utils.save_data(
                    log_data, f'test_{LOG_DIR}_{acq_index}',
                    f'{LOG_DIR}/{RAW_DATA_DIR}')
                log_utils.save_data(
                    log_data_imag, f'test-imag_{LOG_DIR}_{acq_index}',
                    f'{LOG_DIR}/{RAW_DATA_DIR}')
            else:
                log_utils.save_data(
                    log_data, f'test_{itr_index}_{acq_index}',
                    f'{LOG_DIR}/{RAW_DATA_DIR}')
                log_utils.save_data(
                    log_data_imag, f'test-imag_{itr_index}_{acq_index}',
                    f'{LOG_DIR}/{RAW_DATA_DIR}')

            phase_meas[0][acq_index] = measure_phase(
                received[0][DATA_OFFSET:], received[1][DATA_OFFSET:])
            phase_meas[1][acq_index] = measure_phase(
                received[0][DATA_OFFSET:], received[2][DATA_OFFSET:])
            phase_meas[2][acq_index] = measure_phase(
                received[4][DATA_OFFSET:], received[5][DATA_OFFSET:])
            phase_meas[3][acq_index] = measure_phase(
                received[4][DATA_OFFSET:], received[6][DATA_OFFSET:])
            phase_meas[4][acq_index] = measure_phase(
                received[0][DATA_OFFSET:], received[4][DATA_OFFSET:])
            phase_meas[5][acq_index] = measure_phase(
                received[2][DATA_OFFSET:], received[6][DATA_OFFSET:])
            phase_meas[6][acq_index] = measure_phase(
                received[0][DATA_OFFSET:], received[6][DATA_OFFSET:])

    ###########################################################################
            temperature_meas_2[0][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -c adrv9009-phy temp0 input')) / 1000
            temperature_meas_2[1][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -c adrv9009-phy-b temp0 input')) / 1000
            temperature_meas_2[2][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -c adrv9009-phy-c temp0 input')) / 1000
            temperature_meas_2[3][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -c adrv9009-phy-d temp0 input')) / 1000

            temperature_meas_2[4][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -u ' + SECONDARY +
                ' -c adrv9009-phy temp0 input')) / 1000
            temperature_meas_2[5][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -u ' + SECONDARY +
                ' -c adrv9009-phy-b temp0 input')) / 1000
            temperature_meas_2[6][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -u ' + SECONDARY +
                ' -c adrv9009-phy-c temp0 input')) / 1000
            temperature_meas_2[7][acq_index] = int(log_utils.check_iio_data(
                'iio_attr -u ' + SECONDARY +
                ' -c adrv9009-phy-d temp0 input')) / 1000
            temp_data, columns_names = [], []
            temp_data_names = [
                'adrv9009-phy', 'adrv9009-phy-b',
                'adrv9009-phy-c', 'adrv9009-phy-d',
                'adrv9009-phy__sec', 'adrv9009-phy-b__sec',
                'adrv9009-phy-c__sec', 'adrv9009-phy-d__sec']
            for list_index, list_element in enumerate(temperature_meas_2):
                temp_data.append(list_element)
                columns_names.append(f'{temp_data_names[list_index]}')
            meas_data = {"column_names": [], "column_data": []}
            meas_data["column_names"] = columns_names
            meas_data["column_data"] = temp_data
            log_utils.save_data(meas_data, 'temp_data_2', f'{LOG_DIR}')
    ###########################################################################

            if PLOT_TIME:
                plt.clf()
                if HAS_FMCOMMS8:
                    plt.plot(
                        received[0].real,
                        label=f"{acq_index} Chan0 SOM A")
                    plt.plot(
                        received[1].real,
                        label=f"{acq_index} Chan2 SOM A")
                    plt.plot(
                        received[2].real,
                        label=f"{acq_index} Chan4 SOM A FMC8")
                    plt.plot(
                        received[4].real,
                        label=f"{acq_index} Chan0 SOM B")
                    plt.plot(
                        received[6].real,
                        label=f"{acq_index} Chan4 SOM B FMC8")
                else:
                    plt.plot(
                        received[0].real, label=f"{acq_index} Chan0 SOM A")
                    plt.plot(
                        received[1].real, label=f"{acq_index} Chan1 SOM A")
                    plt.plot(
                        received[2].real, label=f"{acq_index} Chan2 SOM A")
                    plt.plot(
                        received[4].real, label=f"{acq_index} Chan0 SOM B")
                    plt.plot(
                        received[6].real, label=f"{acq_index} Chan2 SOM B")
                plt.legend()
                plt.draw()
                plt.pause(0.1)

        # input('Set the Scope for acquisition, then ENTER to continue')
        # for _ in range(5):
        #     log_utils.check_iio_data(
        #         'iio_attr -q -d hmc7044-ext sysref_request 1')
        # input('Save data from Scope, then ENTER to continue')

        for m_index in range(PHASE_MEAS):
            mean_phase_meas[m_index][itr_index] = np.mean(phase_meas[m_index])
            min_phase_meas[m_index][itr_index] = \
                abs(min(phase_meas[m_index]) - np.mean(phase_meas[m_index]))
            max_phase_meas[m_index][itr_index] = \
                abs(max(phase_meas[m_index]) - np.mean(phase_meas[m_index]))
            variance_phase_meas[m_index][itr_index] = np.var(
                phase_meas[m_index])
            log[m_index].append(mean_phase_meas[m_index])

        phase_data, columns_names = [], []
        for list_index, list_element in enumerate(mean_phase_meas):
            phase_data.append(list_element)
            phase_data.append(min_phase_meas[list_index])
            phase_data.append(max_phase_meas[list_index])
            columns_names.append(f'{chan_desc[list_index]}')
            columns_names.append(f'{chan_desc[list_index]} min')
            columns_names.append(f'{chan_desc[list_index]} max')

        meas_data = {"column_names": [], "column_data": []}
        meas_data["column_names"] = columns_names
        meas_data["column_data"] = phase_data
        log_utils.save_data(meas_data, 'phase_data', f'{LOG_DIR}')

###############################################################################
        temperature_meas[0][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -c adrv9009-phy temp0 input')) / 1000
        temperature_meas[1][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -c adrv9009-phy-b temp0 input')) / 1000
        temperature_meas[2][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -c adrv9009-phy-c temp0 input')) / 1000
        temperature_meas[3][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -c adrv9009-phy-d temp0 input')) / 1000

        temperature_meas[4][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -u ' + SECONDARY +
            ' -c adrv9009-phy temp0 input')) / 1000
        temperature_meas[5][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -u ' + SECONDARY +
            ' -c adrv9009-phy-b temp0 input')) / 1000
        temperature_meas[6][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -u ' + SECONDARY +
            ' -c adrv9009-phy-c temp0 input')) / 1000
        temperature_meas[7][itr_index] = int(log_utils.check_iio_data(
            'iio_attr -u ' + SECONDARY +
            ' -c adrv9009-phy-d temp0 input')) / 1000
        temp_data, columns_names = [], []
        temp_data_names = [
            'adrv9009-phy', 'adrv9009-phy-b',
            'adrv9009-phy-c', 'adrv9009-phy-d',
            'adrv9009-phy__sec', 'adrv9009-phy-b__sec',
            'adrv9009-phy-c__sec', 'adrv9009-phy-d__sec']
        for list_index, list_element in enumerate(temperature_meas):
            temp_data.append(list_element)
            columns_names.append(f'{temp_data_names[list_index]}')
        meas_data = {"column_names": [], "column_data": []}
        meas_data["column_names"] = columns_names
        meas_data["column_data"] = temp_data
        log_utils.save_data(meas_data, 'temp_data', f'{LOG_DIR}')
###############################################################################
        hmc7044_regs[0][itr_index] = log_utils.check_iio_data(
            'iio_reg hmc7044 0x8c').rstrip()
        hmc7044_regs[1][itr_index] = log_utils.check_iio_data(
            'iio_reg hmc7044-fmc 0x8c').rstrip()
        hmc7044_regs[2][itr_index] = log_utils.check_iio_data(
            'iio_reg hmc7044-car 0x8c').rstrip()

        hmc7044_regs[3][itr_index] = log_utils.check_iio_data(
            'iio_reg -u ' + SECONDARY + ' hmc7044 0x8c').rstrip()
        hmc7044_regs[4][itr_index] = log_utils.check_iio_data(
            'iio_reg -u ' + SECONDARY + ' hmc7044-fmc 0x8c').rstrip()
        hmc7044_regs[5][itr_index] = log_utils.check_iio_data(
            'iio_reg -u ' + SECONDARY + ' hmc7044-car 0x8c').rstrip()
        hmc7044_regs_data, columns_names = [], []
        hmc7044_regs_data_names = [
            'hmc7044', 'hmc7044-fmc', 'hmc7044-car',
            'hmc7044__sec', 'hmc7044-fmc__sec', 'hmc7044-car__sec']
        for list_index, list_element in enumerate(hmc7044_regs):
            hmc7044_regs_data.append(list_element)
            columns_names.append(f'{hmc7044_regs_data_names[list_index]}')
        meas_data = {"column_names": [], "column_data": []}
        meas_data["column_names"] = columns_names
        meas_data["column_data"] = hmc7044_regs_data
        log_utils.save_data(meas_data, 'hmc7044_regs_data', f'{LOG_DIR}')
###############################################################################

        print("###########")
        for meas_index in range(PHASE_MEAS):
            print("%s:\t %f" % (
                chan_desc[meas_index],
                mean_phase_meas[meas_index][itr_index]))
        print("###########")

        if PLOT_TIME:
            plt.clf()
            if HAS_FMCOMMS8:
                plt.plot(received[0].real, label="Chan0 SOM A")
                plt.plot(received[1].real, label="Chan2 SOM A")
                plt.plot(received[2].real, label="Chan4 SOM A FMC8")
                plt.plot(received[4].real, label="Chan0 SOM B")
                plt.plot(received[6].real, label="Chan4 SOM B FMC8")
            else:
                plt.plot(received[0].real, label="Chan0 SOM A")
                plt.plot(received[1].real, label="Chan1 SOM A")
                plt.plot(received[2].real, label="Chan2 SOM A")
                plt.plot(received[4].real, label="Chan0 SOM B")
                plt.plot(received[6].real, label="Chan2 SOM B")
            plt.legend()
            plt.draw()
            plt.pause(2)

        if RUN_EXTERNAL is not True:
            plt.clf()
            x_axis = np.array(range(0, itr_index + 1))

            for meas_index in range(PHASE_MEAS):
                plt.errorbar(
                    x_axis, mean_phase_meas[meas_index][x_axis],
                    yerr=variance_phase_meas[meas_index][x_axis],
                    label=chan_desc[meas_index])
                # plt.errorbar(
                #     x_axis, mean_phase_meas[meas_index][x_axis],
                #     yerr=0, label=chan_desc[meas_index])
            plt.xlim([-1, x_axis[-1] + 1])
            plt.xlabel("Measurement Index")
            plt.ylabel("Phase Difference (Degrees)")
            plt.legend()
            plt.draw()
            plt.pause(0.1)

    # input("Press ENTER to continue...")
    print(log)
    fields = []
    for meas_index in range(PHASE_MEAS):
        fields.append(np.sum(log[meas_index]) / len(log[meas_index]))
        fields.append(np.min(log[meas_index]))
        fields.append(np.max(log[meas_index]))
    with open(r"log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
