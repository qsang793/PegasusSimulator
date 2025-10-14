#!/usr/bin/env python3
"""
Camera Data Subscriber for Pegasus Simulator
Subscribes to camera topics published by ROS2 backend
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        
        # Initialize CV Bridge
        self.bridge = CvBridge()
        
        self.window_name = "Pegasus Camera"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 800, 600)

        # Subscribers for camera data
        self.image_sub = self.create_subscription(
            Image,
            '/drone1/camera/color/image_raw',
            self.image_callback,
            10
        )
        
        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            '/drone1/camera/color/camera_info',
            self.camera_info_callback,
            10
        )
        
        self.get_logger().info('Camera subscriber initialized')
        
    def image_callback(self, msg):
        """Process incoming camera images"""
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            cv2.imshow(self.window_name, cv_image)
            key = cv2.waitKey(1) & 0xFF

            if key in (ord('q'), 27): 
                self.get_logger().info("Quit requested by user.")
                cv2.destroyAllWindows()
                rclpy.shutdown()  
                return
            
            self.get_logger().info(f'Received image: {cv_image.shape}')
            
        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')
    
    def camera_info_callback(self, msg):
        timestamp = msg.header.stamp

        """Process camera info"""
        self.get_logger().info(f'IMU Timestamp: {timestamp.sec}.{timestamp.nanosec:09d}')
        self.get_logger().info(f'Camera Info - Width: {msg.width}, Height: {msg.height}')
        self.get_logger().info(f'K matrix: {msg.k}')

def main(args=None):
    rclpy.init(args=args)
    
    camera_subscriber = CameraSubscriber()
    
    try:
        rclpy.spin(camera_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        camera_subscriber.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
