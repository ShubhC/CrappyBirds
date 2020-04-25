import os
import Utils
from enum import Enum
from PIL import Image
import Constants
import pygame

class GameObjectCorner(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class GameObject(object):
    def __init__(self, xCoordinate, yCoordinate, objectWidth, objectHeight, imageBasePath, imageName):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.imagePath = Utils.generateResizedImage(imageBasePath, 
                                                    imageName, 
                                                    objectWidth,
                                                    objectHeight)
        if objectWidth == -1 or objectHeight == -1:
           self.objectWidth = 38
           self.objectHeight = 30
        else:
           self.objectWidth = objectWidth
           self.objectHeight = objectHeight

        self.hitbox = (xCoordinate, 
                       yCoordinate, 
                       xCoordinate + self.objectWidth, 
                       yCoordinate + self.objectHeight)

    def delImage(self):
        self.removeImg(self.imagePath)

    def removeImg(self, image_path):
        os.remove(image_path)
        # check if file exists or not
        if os.path.exists(image_path) is False:
            return True

    def display(self, window):
        coordinates = (self.xCoordinate, self.yCoordinate)
        loadedImage = pygame.image.load(self.imagePath)
        window.blit( loadedImage, coordinates)

class Bird(GameObject):
    def __init__(self, xCoordinate, yCoordinate, objectWidth, objectHeight, imageBasePath, imageName):        
        super().__init__(xCoordinate, yCoordinate, objectWidth, objectHeight, imageBasePath, imageName)

    def changeCoordinate(self, changeBy):
        self.yCoordinate += changeBy

    def display(self, window):
        displayXCoordinate = self.xCoordinate
        displayYCoordinate = self.yCoordinate

        if displayYCoordinate > Constants.BIRD_Y_COORDINATE_MAX:
            displayYCoordinate = Constants.BIRD_Y_COORDINATE_MAX
        
        if displayYCoordinate < Constants.BIRD_Y_COORDINATE_MIN:
            displayYCoordinate = Constants.BIRD_Y_COORDINATE_MIN
        
        coordinates = (displayXCoordinate, displayYCoordinate)
        loadedImage = pygame.image.load(self.imagePath)
        window.blit( loadedImage, coordinates)

