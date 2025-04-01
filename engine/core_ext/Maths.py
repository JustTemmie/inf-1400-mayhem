from pyglet.math import Vec3, Mat3
import math

class Maths:
    radian_degree = 0.0174532925


    def get_rotation_matrix(entity):
        # Create rotation matrices for pitch, yaw, and roll
        pitch_matrix = Maths.create_rotation_matrix(entity.rotation.x, Vec3(1, 0, 0))
        yaw_matrix = Maths.create_rotation_matrix(entity.rotation.y, Vec3(0, 1, 0))
        roll_matrix = Maths.create_rotation_matrix(entity.rotation.z, Vec3(0, 0, 1))
        # Combine the matrices to get the final rotation matrix
        
        return pitch_matrix @ yaw_matrix @ roll_matrix

    def create_rotation_matrix(angle, axis) -> Mat3:
        # Create a rotation matrix for a given angle and axis
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        one_minus_cos = 1 - cos_theta
        x, y, z = axis.x, axis.y, axis.z
        return Mat3(
            Vec3(cos_theta + x * x * one_minus_cos, x * y * one_minus_cos - z * sin_theta, x * z * one_minus_cos + y * sin_theta),
            Vec3(y * x * one_minus_cos + z * sin_theta, cos_theta + y * y * one_minus_cos, y * z * one_minus_cos - x * sin_theta),
            Vec3(z * x * one_minus_cos - y * sin_theta, z * y * one_minus_cos + x * sin_theta, cos_theta + z * z * one_minus_cos))