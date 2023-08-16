import rclpy
# from rclpy.node import Node
# import numpy as np
# from sensor_msgs.msg import LaserScan

# #GAUSSIAN NOISE PARAMETERS
# STD = 0.01
# MEAN = 0.01

# class LidarNode(Node):

#     def __init__(self):
#         super().__init__('Lidar Node')
#         # timer_period = 0.01  # seconds
#         # self.timer = self.create_timer(timer_period, self.timer_callback)
#         self.subscription = self.create_subscription(
#             LaserScan,
#             '/scan_ideal',
#             self.listener_callback,
#             10)
#         # self.subscription  # prevent unused variable warning
        
#         self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        
#         self.raw_measurements = LaserScan()

#     def listener_callback(self, msg):
#         self.raw_meas = msg
#         self.noisy_meas = self.raw_meas
#         self.noisy_meas.range = np.random.normal(self.raw_meas.range+MEAN, 0.2*STD)
#         self.get_logger().info('I heard: "%s"' % msg.data)
#         self.publisher_.publish(self.noisy_meas)
#         self.get_logger().info('Publishing: "%s"' % self.noisy_meas)



def main(args=None):
    rclpy.init(args=args)

    # lidar = LidarNode()

    # rclpy.spin(lidar)

    # # Destroy the node explicitly
    # # (optional - otherwise it will be done automatically
    # # when the garbage collector destroys the node object)
    # lidar.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


