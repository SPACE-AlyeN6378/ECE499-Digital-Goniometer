 # SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
 #
 # SPDX-License-Identifier: Unlicense
import time
import board
# import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)

from adafruit_bno08x.i2c import BNO08X_I2C

def sensor_init(i2c):

    while True:
        try:
            bno = BNO08X_I2C(i2c)
            print("BNO085 Sensor Connection Successful!!!")
            return bno
        except ValueError as e:
            print("Connection not found: ", e, "| RETRYING...")
            time.sleep(1)


# Initialize the built-in STEMMA QT board

def i2c_init():
    while True:
        time.sleep(2)
        try:
            i2c = board.STEMMA_I2C()
            print("I2C Initialized!!!")
            return i2c
        
        except RuntimeError as e:
            print("I2C init failed, retrying...", e)
    


def check_address():
    while not i2c.try_lock():
        pass

    addresses = [hex(device_address) for device_address in i2c.scan()]

    # Check for connection
    while True:
        print(
            "I2C addresses found:",
            addresses
        )
        time.sleep(1)

        if '0x9' in addresses or '0x4a' in addresses:
            print("Address found!")
            break
            
        addresses = [hex(device_address) for device_address in i2c.scan()]

    i2c.unlock()

def safe_enable_feature(bno, feature, feature_name):
    while True:
        try:
            bno.enable_feature(feature)
            print(f"Enabled {feature_name}")
            return
        
        except Exception as e:
            print(f"Failed to enable {feature_name}: {e}")
            time.sleep(1)


i2c = i2c_init()
check_address()
bno = sensor_init(i2c)

safe_enable_feature(bno, BNO_REPORT_ROTATION_VECTOR, "Rotation Vector")

while True:
    time.sleep(0.5)

    quat_i, quat_j, quat_k, quat_real = bno.quaternion      # pylint:disable=no-member
    print("I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real))


        