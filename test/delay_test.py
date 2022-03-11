from os import popen

import log_utils

for index in range(18):
    value = hex(index)
    log_utils.check_iio_data(
        f'iio_reg -u ip:localhost hmc7044-car 0x126 {value}')

    print('primary car (reg 0x126):', end=" ")
    print(log_utils.check_iio_data(
        'iio_reg -u ip:localhost hmc7044-car 0x126').rstrip())

    input('Run the Wiki script, then press ENTER to continue')

    log_utils.check_iio_data(
        'iio_attr -q -d hmc7044-ext sysref_request 1')

    input('Save data from Scope, then press ENTER to continue')

log_utils.check_iio_data('iio_reg -u ip:localhost hmc7044-car 0x126 0x0')


# for index in range(18):
#     value = hex(index)
#     log_utils.check_iio_data(
#         f'iio_reg -u ip:localhost hmc7044-car 0x108 {value}')
#
#     print('primary car (reg 0x108):', end=" ")
#     print(log_utils.check_iio_data(
#         'iio_reg -u ip:localhost hmc7044-car 0x108').rstrip())
#
#     input('Run the Wiki script, then press ENTER to continue')
#
#     log_utils.check_iio_data(
#         'iio_attr -q -d hmc7044-ext sysref_request 1')
#
#     input('Save data from Scope, then press ENTER to continue')
#
# log_utils.check_iio_data('iio_reg -u ip:localhost hmc7044-car 0x108 0x0')


# for index in range(1, 16):
#     value = hex(index)
#     log_utils.check_iio_data(
#         f'iio_reg -u ip:localhost hmc7044-car 0x1A {value}')
#
#     print('primary car (reg 0x1A):', end=" ")
#     print(log_utils.check_iio_data(
#         'iio_reg -u ip:localhost hmc7044-car 0x1A').rstrip())
#
#     input('Run the Wiki script, then press ENTER to continue')
#
#     log_utils.check_iio_data(
#         'iio_attr -q -d hmc7044-ext sysref_request 1')
#
#     input('Save data from Scope, then press ENTER to continue')
#
# log_utils.check_iio_data('iio_reg -u ip:localhost hmc7044-car 0x1A 0xf')
