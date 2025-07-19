import time


class PD:
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd
        self.last_time = time.time()
        self.curr_time = None
        self.last_error = 0

    def calculate(self, error):
        self.curr_time = time.time()
        d_error = (error - self.last_error) / (self.curr_time - self.last_time)
        self.last_error = error
        self.last_time = self.curr_time
        return self.kp * error + self.kd * d_error


kP = 0.01  # insert actual value
kD = 0.001  # insert actual value


def get_servo_angle(position):
    # insert mapping here
    # assuming degrees for now
    # make sure normalize to 0-360
    ...


def get_power(target_angle, current_angle):
    pd = PD(kP, kD)
    error, reversed = error_wrap(target_angle, current_angle)
    power = pd.calculate(error)
    return power if not reversed else -power


def error_wrap(target_angle, current_angle):
    wrapped_error_normal = abs((target_angle - current_angle + 180) % 360 - 180)
    wrapped_error_reverse = abs(
        (((target_angle + 180) % 360) - current_angle + 180) % 360 - 180
    )
    return (
        min(wrapped_error_normal, wrapped_error_reverse),
        lambda x: False if wrapped_error_normal <= wrapped_error_reverse else True,
    )  # returns a tuple of (error, reversed as boolean)
    # the idea here is that the reversed boolean is independent of whether it was reversed last time to make it simpler
