#!/usr/bin/env python
from em7180 import EM7180_Master
import rospy
from sensor_msgs.msg import MagneticField

MAG_RATE = 100  # Hz
ACCEL_RATE = 200  # Hz
GYRO_RATE = 200  # Hz
BARO_RATE = 50  # Hz
Q_RATE_DIVISOR = 3  # 1/3 gyro rate


def main():
    rospy.init_node('em7180')
    publisher = rospy.Publisher('imu/mag', MagneticField, queue_size=10)
    rate = rospy.Rate(10)

    em7180 = EM7180_Master(MAG_RATE, ACCEL_RATE, GYRO_RATE, BARO_RATE, Q_RATE_DIVISOR)

    # Start the EM7180 in master mode
    if not em7180.begin():
        print(em7180.getErrorString())
        exit(1)

    while not rospy.is_shutdown():
        em7180.checkEventStatus()
        if em7180.gotError():
            print('ERROR: ' + em7180.getErrorString())
            exit(1)

        if em7180.gotMagnetometer():
            mx, my, mz = em7180.readMagnetometer()
            magnetic_vector = MagneticField()

            magnetic_vector.header.stamp = rospy.Time.now()
            magnetic_vector.header.frame_id = "magnetic_vector"

            magnetic_vector.magnetic_field.x = mx
            magnetic_vector.magnetic_field.y = my
            magnetic_vector.magnetic_field.z = mz

            magnetic_vector.magnetic_field_covariance = [700, 0, 0, 0, 700, 0, 0, 0, 700]

            publisher.publish(magnetic_vector)

        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
