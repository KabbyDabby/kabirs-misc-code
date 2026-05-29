from math import sqrt


class Pose:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mirror(self):
        return Pose(144 - self.x, self.y)


def distance(pose1, pose2):
    return sqrt((pose1.x - pose2.x) ** 2 + (pose1.y - pose2.y) ** 2)


class Constants:
    BLUE_GOAL_POSE = Pose(9, 132.5)


SHOOTER_OFFSET_X = -2.42


distances = [
    distance(Pose(44.41, 103.331), Constants.BLUE_GOAL_POSE) - SHOOTER_OFFSET_X,
    distance(Pose(54.74, 94.8), Constants.BLUE_GOAL_POSE) - SHOOTER_OFFSET_X,
    distance(Pose(64, 83.1), Constants.BLUE_GOAL_POSE) - SHOOTER_OFFSET_X,
    distance(Pose(77.17, 70.93), Constants.BLUE_GOAL_POSE) - SHOOTER_OFFSET_X,
    distance(Pose(106, 90.7), Constants.BLUE_GOAL_POSE) - SHOOTER_OFFSET_X,
    distance(Pose(131.66, 109.4), Constants.BLUE_GOAL_POSE) - SHOOTER_OFFSET_X,
    distance(Pose(75.84, 23.04), Constants.BLUE_GOAL_POSE) - SHOOTER_OFFSET_X,
]

for distance in distances:
    print(distance)
