from __future__ import print_function
import msgpackrpc #install as admin: pip install msgpack-rpc-python
import numpy as np #pip install numpy

class MsgpackMixin:
    def __repr__(self):
        from pprint import pformat
        return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)

    def to_msgpack(self, *args, **kwargs):
        return self.__dict__

    @classmethod
    def from_msgpack(cls, encoded):
        obj = cls()
        ww = encoded.items()
        #obj.__dict__ = {k.decode('utf-8'): (from_msgpack(v.__class__, v) if hasattr(v, "__dict__") else v) for k, v in encoded.items()}
        for k, v in encoded.items():
            if (isinstance(v, dict) and hasattr(getattr(obj, k).__class__, 'from_msgpack')):
                obj.__dict__[k] = getattr(getattr(obj, k).__class__, 'from_msgpack')(v)
            else:
                obj.__dict__[k] = v
                
        #obj.__dict__ = { k : (v if not isinstance(v, dict) else getattr(getattr(obj, k).__class__, "from_msgpack")(v)) for k, v in encoded.items()}
        #return cls(**msgpack.unpack(encoded))
        return obj


class ImageType:    
    Scene = 0
    DepthPlanner = 1
    DepthPerspective = 2
    DepthVis = 3
    DisparityNormalized = 4
    Segmentation = 5
    SurfaceNormals = 6
    Infrared = 7

class DrivetrainType:
    MaxDegreeOfFreedom = 0
    ForwardOnly = 1
    
class LandedState:
    Landed = 0
    Flying = 1

class Vector3r(MsgpackMixin):
    x_val = np.float32(0)
    y_val = np.float32(0)
    z_val = np.float32(0)

    def __init__(self, x_val = np.float32(0), y_val = np.float32(0), z_val = np.float32(0)):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val


class Quaternionr(MsgpackMixin):
    w_val = np.float32(0)
    x_val = np.float32(0)
    y_val = np.float32(0)
    z_val = np.float32(0)

    def __init__(self, x_val = np.float32(0), y_val = np.float32(0), z_val = np.float32(0), w_val = np.float32(1)):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val
        self.w_val = w_val

class Pose(MsgpackMixin):
    position = Vector3r()
    orientation = Quaternionr()

    def __init__(self, position_val = Vector3r(), orientation_val = Quaternionr()):
        self.position = position_val
        self.orientation = orientation_val

class Twist(MsgpackMixin):
    linear = Vector3r()
    angular = Vector3r()

    def __init__(self, linear_val = Vector3r(), angular_val = Vector3r()):
        self.linear = linear_val
        self.angular = angular_val

class CollisionInfo(MsgpackMixin):
    has_collided = False
    normal = Vector3r()
    impact_point = Vector3r()
    position = Vector3r()
    penetration_depth = np.float32(0)
    time_stamp = np.float32(0)
    object_name = ""
    object_id = -1

class GeoPoint(MsgpackMixin):
    latitude = 0.0
    longitude = 0.0
    altitude = 0.0

class YawMode(MsgpackMixin):
    is_rate = True
    yaw_or_rate = 0.0
    def __init__(self, is_rate = True, yaw_or_rate = 0.0):
        self.is_rate = is_rate
        self.yaw_or_rate = yaw_or_rate

class RCData(MsgpackMixin):
    timestamp = 0
    pitch, roll, throttle, yaw = (0.0,)*4 #init 4 variable to 0.0
    switch1, switch2, switch3, switch4 = (0,)*4
    switch5, switch6, switch7, switch8 = (0,)*4
    is_initialized = False
    is_valid = False
    def __init__(self, timestamp = 0, pitch = 0.0, roll = 0.0, throttle = 0.0, yaw = 0.0, switch1 = 0,
                 switch2 = 0, switch3 = 0, switch4 = 0, switch5 = 0, switch6 = 0, switch7 = 0, switch8 = 0, is_initialized = False, is_valid = False):
        self.timestamp = timestamp
        self.pitch = pitch 
        self.roll = roll
        self.throttle = throttle 
        self.yaw = yaw 
        self.switch1 = switch1 
        self.switch2 = switch2 
        self.switch3 = switch3 
        self.switch4 = switch4 
        self.switch5 = switch5
        self.switch6 = switch6 
        self.switch7 = switch7 
        self.switch8 = switch8 
        self.is_initialized = is_initialized
        self.is_valid = is_valid

class ImageRequest(MsgpackMixin):
    camera_name = '0'
    image_type = ImageType.Scene
    pixels_as_float = False
    compress = False

    def __init__(self, camera_name, image_type, pixels_as_float = False, compress = True):
        # todo: in future remove str(), it's only for compatibility to pre v1.2
        self.camera_name = str(camera_name)
        self.image_type = image_type
        self.pixels_as_float = pixels_as_float
        self.compress = compress


class ImageResponse(MsgpackMixin):
    image_data_uint8 = np.uint8(0)
    image_data_float = np.float32(0)
    camera_position = Vector3r()
    camera_orientation = Quaternionr()
    time_stamp = np.uint64(0)
    message = ''
    pixels_as_float = np.float32(0)
    compress = True
    width = 0
    height = 0
    image_type = ImageType.Scene

class CarControls(MsgpackMixin):
    throttle = np.float32(0)
    steering = np.float32(0)
    brake = np.float32(0)
    handbrake = False
    is_manual_gear = False
    manual_gear = 0
    gear_immediate = True

    def __init__(self, throttle = 0, steering = 0, brake = 0, 
        handbrake = False, is_manual_gear = False, manual_gear = 0, gear_immediate = True):
        self.throttle = throttle
        self.steering = steering
        self.brake = brake
        self.handbrake = handbrake
        self.is_manual_gear = is_manual_gear
        self.manual_gear = manual_gear
        self.gear_immediate = gear_immediate


    def set_throttle(self, throttle_val, forward):
        if (forward):
            is_manual_gear = False
            manual_gear = 0
            throttle = abs(throttle_val)
        else:
            is_manual_gear = False
            manual_gear = -1
            throttle = - abs(throttle_val)

class KinematicsState(MsgpackMixin):
    position = Vector3r()
    orientation = Quaternionr()
    linear_velocity = Vector3r()
    angular_velocity = Vector3r()
    linear_acceleration = Vector3r()
    angular_acceleration = Vector3r()

class EnvironmentState(MsgpackMixin):
    position = Vector3r()
    geo_point = GeoPoint()
    gravity = Vector3r()
    air_pressure = np.float32(0)
    temperature = np.float32(0)
    air_density = np.float32(0)

class CarState(MsgpackMixin):
    speed = np.float32(0)
    gear = 0
    rpm = np.float32(0)
    maxrpm = np.float32(0)
    handbrake = False
    collision = CollisionInfo();
    kinematics_estimated = KinematicsState()
    timestamp = np.uint64(0)

class MultirotorState(MsgpackMixin):
    collision = CollisionInfo();
    kinematics_estimated = KinematicsState()
    gps_location = GeoPoint()
    timestamp = np.uint64(0)
    landed_state = LandedState.Landed
    rc_data = RCData()

class CameraInfo(MsgpackMixin):
    pose = Pose()
    fov = -1

class LidarData(MsgpackMixin):
    point_cloud = 0.0
    time_stamp = np.uint64(0)
    pose = Pose()

class AddAngularForce(MsgpackMixin):
    force_name = ''
    link_name = ''
    axis = Vector3r()

    def __init__(self, force_name_val = '', link_name_val = '', axis_val = Vector3r()):
        self.force_name = force_name_val
        self.link_name = link_name_val
        self.axis = axis_val

class AddLinearForce(MsgpackMixin):
    force_name = ''
    link_name = ''
    application_point = Vector3r()
    axis = Vector3r()

    def __init__(self, force_name_val = '', link_name_val = '', application_point_val = Vector3r(), axis_val = Vector3r()):
        self.force_name = force_name_val
        self.link_name = link_name_val
        self.application_point = application_point_val
        self.axis = axis_val

class UpdateForceMagnitude(MsgpackMixin):
    force_name = ''
    magnitude = 0.0

    def __init__(self, force_name_val = '', magnitude_val = 0.0):
        self.force_name = force_name_val
        self.magnitude = magnitude_val

class LinkInformation(MsgpackMixin):
    link_name = ''
    link_relative_pose = Pose()
    link_relative_twist = Twist()

    def __init__(self, link_name_val = '', link_relative_pose_val = Pose(), link_relative_twist_val = Twist()):
        self.link_name = link_name_val
        self.link_relative_pose = link_relative_pose_val
        self.link_relative_twist = link_relative_twist_val

class UrdfBotState(MsgpackMixin):
    link_information = []
    kinematics_estimated = KinematicsState()
    controlled_motion_component_states = {}

    def __init__(self, link_information_val = [], kinematics_estimated_val = KinematicsState(), controlled_motion_component_states = {}):
        self.link_information = link_information_val
        self.kinematics_estimated = kinematics_estimated_val
        self.controlled_motion_component_states = controlled_motion_component_states

class UrdfBotControlledMotionComponentControlSignal(MsgpackMixin):
    component_name = ''
    control_signal_values = {}

    def __init__(self, component_name = '', control_signal_values = {}):
        self.component_name = component_name
        self.control_signal_values = control_signal_values

class CameraPose(MsgpackMixin):
    camera_name = ''
    translation = Vector3r()
    rotation = Quaternionr()

    def __init__(self, camera_name, translation, rotation):
        self.camera_name = camera_name
        self.translation = translation
        self.rotation = rotation

class RayCastRequest(MsgpackMixin):
    position = Vector3r()
    direction = Vector3r()
    reference_frame_link = ''
    through_blocking = False
    persist_seconds = 0

    def __init__(self, position, direction, reference_frame_link, through_blocking, persist_seconds):
        self.position = position
        self.direction = direction
        self.reference_frame_link = reference_frame_link
        self.through_blocking = through_blocking
        self.persist_seconds = persist_seconds

class RayCastHit:
    collided_actor_name = ''
    hit_point = Vector3r()
    hit_normal = Vector3r()

    def __init__(self, collided_actor_name = '', hit_point = Vector3r(), hit_normal = Vector3r()):
        self.collided_actor_name = collided_actor_name
        self.hit_point = hit_point
        self.hit_normal = hit_normal

class RayCastResponse(MsgpackMixin):
    hits = []
    def __init__(self, hits = []):
        self.hits = hits

class DrawableShape(MsgpackMixin):
    reference_frame_link = ''
    type = 0
    shape_params = []

    def __init__(self, reference_frame_link, type, shape_params):
        self.reference_frame_link = reference_frame_link
        self.type = type
        self.shape_params = shape_params

class DrawableShapeRequest(MsgpackMixin):
    shapes = {}
    persist_unmentioned = False

    def __init__(self, shapes = {}, persist_unmentioned = False):
        self.shapes = shapes
        self.persist_unmentioned = persist_unmentioned
