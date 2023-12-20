from random import randint
import time

class MyPerson:
    # Static list shared by all instances to track multiple persons
    tracks = []

    def __init__(self, i, xi, yi, max_age):
        # Constructor for initializing a new person instance
        self.i = i               # ID for the person
        self.x = xi              # X-coordinate
        self.y = yi              # Y-coordinate
        self.tracks = []         # Track movement history of this person
        # Random color assigned to the person for identification in visualization
        self.R = randint(0, 255) 
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.done = False        # Flag to mark if tracking is done
        self.state = '0'         # State of the person (e.g., moving, stationary)
        self.age = 0             # Age of the track (used for timing out old tracks)
        self.max_age = max_age   # Maximum age after which the track is discarded
        self.dir = None          # Direction of movement

    def getRGB(self):
        # Returns the RGB color of the person
        return (self.R, self.G, self.B)

    def getTracks(self):
        # Returns the list of tracks (positions) of the person
        return self.tracks

    def getId(self):
        # Returns the ID of the person
        return self.i

    def getState(self):
        # Returns the current state of the person
        return self.state

    def getDir(self):
        # Returns the current direction of movement
        return self.dir

    def getX(self):
        # Returns the current X-coordinate
        return self.x

    def getY(self):
        # Returns the current Y-coordinate
        return self.y

    def updateCoords(self, xn, yn):
        # Updates the coordinates of the person and resets the age
        self.age = 0
        self.tracks.append([self.x, self.y]) # Add current position to tracks
        self.x = xn
        self.y = yn

    def setDone(self):
        # Marks the tracking as done
        self.done = True

    def timedOut(self):
        # Checks if the tracking is marked as done
        return self.done

    def going_UP(self, mid_start, mid_end):
        # Determines if the person is moving up across a defined line
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end:
                    # Update state and direction if crossing the line
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False

    def going_DOWN(self, mid_start, mid_end):
        # Determines if the person is moving down across a defined line
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start:
                    # Update state and direction if crossing the line
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False

    def age_one(self):
        # Increments the age of the track and marks done if it exceeds max_age
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True

class MultiPerson:
    def __init__(self, persons, xi, yi):
        # Constructor for initializing a group of persons
        self.persons = persons   # List of person instances in the group
        self.x = xi              # X-coordinate of the group
        self.y = yi              # Y-coordinate of the group
        self.tracks = []         # Track movement history of the group
        # Random color assigned to the group for identification
        self.R = randint(0, 255)
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.done = False        # Flag to mark if tracking of the group is done
