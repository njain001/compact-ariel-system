from random import randint
import time

class MyPerson:
    ## A class for tracking an individual person's movement and attributes in a tracking system.
    
    tracks = []  # Static list shared by all instances to track multiple persons

    def __init__(self, i, xi, yi, max_age):
        ## Constructor for initializing a new person instance.
        # @param i: Integer representing the ID for the person.
        # @param xi: Integer representing the initial X-coordinate.
        # @param yi: Integer representing the initial Y-coordinate.
        # @param max_age: Integer representing the maximum age before track is discarded.
        self.i = i               # ID for the person
        self.x = xi              # X-coordinate
        self.y = yi              # Y-coordinate
        self.tracks = []         # Track movement history of this person
        self.R = randint(0, 255) # Random color assigned to the person for identification in visualization
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.done = False        # Flag to mark if tracking is done
        self.state = '0'         # State of the person (e.g., moving, stationary)
        self.age = 0             # Age of the track (used for timing out old tracks)
        self.max_age = max_age   # Maximum age after which the track is discarded
        self.dir = None          # Direction of movement

    def getRGB(self):
        ## Returns the RGB color of the person.
        # @return A tuple representing the RGB color (R, G, B).
        return (self.R, self.G, self.B)

    def getTracks(self):
        ## Returns the list of tracks (positions) of the person.
        # @return A list of (x, y) positions representing the movement history.
        return self.tracks

    def getId(self):
        ## Returns the ID of the person.
        # @return The integer ID of the person.
        return self.i

    def getState(self):
        ## Returns the current state of the person.
        # @return A string representing the state ('0' for moving, '1' for stationary).
        return self.state

    def getDir(self):
        ## Returns the current direction of movement.
        # @return A string representing the direction ('up', 'down', or None).
        return self.dir

    def getX(self):
        ## Returns the current X-coordinate.
        # @return The integer X-coordinate of the person.
        return self.x

    def getY(self):
        ## Returns the current Y-coordinate.
        # @return The integer Y-coordinate of the person.
        return self.y

    def updateCoords(self, xn, yn):
        ## Updates the coordinates of the person and resets the age.
        # @param xn: Integer for the new X-coordinate.
        # @param yn: Integer for the new Y-coordinate.
        # This method updates the person's current position to the new coordinates and resets the age.
        self.age = 0
        self.tracks.append([self.x, self.y]) # Add current position to tracks
        self.x = xn
        self.y = yn

    def setDone(self):
        ## Marks the tracking as done.
        # This method sets the 'done' flag to True.
        self.done = True

    def timedOut(self):
        ## Checks if the tracking is marked as done.
        # @return True if tracking is done, False otherwise.
        return self.done

    def going_UP(self, mid_start, mid_end):
        ## Determines if the person is moving up across a defined line.
        # @param mid_start: Integer defining the start of the middle line.
        # @param mid_end: Integer defining the end of the middle line.
        # @return True if moving up across the line, False otherwise.
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end:
                    self.state = '1'
                    self.dir = 'up'
                    return True
        return False

    def going_DOWN(self, mid_start, mid_end):
        ## Determines if the person is moving down across a defined line.
        # @param mid_start: Integer defining the start of the middle line.
        # @param mid_end: Integer defining the end of the middle line.
        # @return True if moving down across the line, False otherwise.
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start:
                    self.state = '1'
                    self.dir = 'down'
                    return True
        return False

    def age_one(self):
        ## Increments the age of the track and marks done if it exceeds max_age.
        # This method increases the age of the track by one and checks if it's past its max_age.
        # @return True if the age is incremented, False otherwise.
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True


class MultiPerson:
    ## A class for tracking a group of persons, managing them as a single entity.

    def __init__(self, persons, xi, yi):
        ## Constructor for initializing a group of persons.
        # @param persons: A list of MyPerson instances representing the individuals in the group.
        # @param xi: Integer representing the initial X-coordinate of the group.
        # @param yi: Integer representing the initial Y-coordinate of the group.
        # The constructor initializes the MultiPerson with a list of persons and initial coordinates.
        self.persons = persons   # List of person instances in the group
        self.x = xi              # X-coordinate of the group
        self.y = yi              # Y-coordinate of the group
        self.tracks = []         # Track movement history of the group
        self.R = randint(0, 255) # Random color assigned to the group for identification
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.done = False        # Flag to mark if tracking of the group is done
