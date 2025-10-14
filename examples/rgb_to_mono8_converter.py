#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class RgbToMono8Converter(Node):
    def __init__(self):
        super().__init__('rgb_to_mono8_converter')
        
        self.bridge = CvBridge()
        
        # Subscribers for left and right camera RGB images
        self.left_rgb_sub = self.create_subscription(
            Image, 
            '/drone1/camera_left/color/image_raw', 
            self.left_rgb_callback, 
            10
        )
        
        self.right_rgb_sub = self.create_subscription(
            Image, 
            '/drone1/camera_right/color/image_raw', 
            self.right_rgb_callback, 
            10
        )
        
        # Publishers for mono8 images
        self.left_mono_pub = self.create_publisher(
            Image, 
            '/drone1/camera_left/image_mono', 
            10
        )
        
        self.right_mono_pub = self.create_publisher(
            Image, 
            '/drone1/camera_right/image_mono', 
            10
        )
        
        self.get_logger().info('RGB to Mono8 converter node started')
    
    def left_rgb_callback(self, msg):
        self.convert_and_publish(msg, self.left_mono_pub, 'left')
    
    def right_rgb_callback(self, msg):
        self.convert_and_publish(msg, self.right_mono_pub, 'right')
    
    def convert_and_publish(self, rgb_msg, mono_pub, camera_name):
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, desired_encoding='bgr8')
            
            # Convert BGR to grayscale (mono8)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Convert back to ROS Image message
            mono_msg = self.bridge.cv2_to_imgmsg(gray_image, encoding='mono8')
            
            # Copy header information (timestamp, frame_id)
            mono_msg.header = rgb_msg.header
            
            # Publish mono8 image
            mono_pub.publish(mono_msg)
            
        except Exception as e:
            self.get_logger().error(f'Error converting {camera_name} image: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    converter = RgbToMono8Converter()
    
    try:
        rclpy.spin(converter)
    except KeyboardInterrupt:
        pass
    finally:
        converter.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
