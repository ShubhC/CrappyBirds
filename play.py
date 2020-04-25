import pygame
import Constants
import Utils
import random
import GameObjectLoader
from collections import deque
from GameObject import GameObject
from GameObject import Bird

def displayGameObject(window, gameObject):
    loadedImage = pygame.image.load(gameObject.imagePath)
    coordinates = (gameObject.xCoordinate,gameObject.yCoordinate)
    window.blit( loadedImage, coordinates)

def updateCoordinates(pipes, vel):
    for i in range(0, len(pipes)):
        northPipe, southPipe = pipes[i]
        
        northPipe.xCoordinate -= vel 
        southPipe.xCoordinate -= vel

def removeCoordinatesToLeftOfWindow(pipes, pipeWidth):
    while len(pipes) > 0:
        northPipe, _ = pipes[0]        
        if northPipe.xCoordinate < 0:
            northPipe.delImage()
            pipes.popleft()
            continue
        break    
    return pipes

def generateNewPipePair(pipeXCoordinate, northPipeHeight, groundYCoordinate, pipeWidth, gapBetweenPipes):    
    # generate north pipe
    newNorthPipeX = pipeXCoordinate
    newNorthPipeY = 0
    newNorthPipeWidth = pipeWidth
    newNorthPipeHeight = northPipeHeight
    newNorthPipe = GameObject(newNorthPipeX, newNorthPipeY, 
                              newNorthPipeWidth, newNorthPipeHeight,
                              Constants.BASE_PATH, Constants.PIPE_NORTH_NAME)

    # generate south pipe
    newSouthPipeX = pipeXCoordinate
    newSouthPipeY = newNorthPipeHeight + gapBetweenPipes
    newSouthPipeWidth = pipeWidth
    newSouthPipeHeight = groundYCoordinate - (gapBetweenPipes + newNorthPipeHeight)  
    newSouthPipe = GameObject(newSouthPipeX, newSouthPipeY, 
                              newSouthPipeWidth, newSouthPipeHeight,
                              Constants.BASE_PATH, Constants.PIPE_SOUTH_NAME)

    return (newNorthPipe, newSouthPipe)

def initializePipes(pipes):
    for i in range(0,len(Constants.INITIAL_NORTH_PIPES_X)):
        newPipePairs = generateNewPipePair(Constants.INITIAL_NORTH_PIPES_X[i],
                                           Constants.INITIAL_NORTH_PIPES_HEIGHT[i],
                                           Constants.GROUND_Y_COORDINATE,
                                           Constants.PIPE_WIDTH,
                                           Constants.GAP_BETWEEN_PIPES)
        pipes.append(newPipePairs)

def initGame():
    ##### load objects #####
    # load background
    global background 
    background = GameObject(0, 0, Constants.WINDOW_SIZE_WIDTH,Constants.WINDOW_SIZE_HEIGHT, Constants.BASE_PATH, Constants.BACKGROUND_IMAGE_NAME)

    global flyingBird 
    flyingBird = Bird(200,200,-1, -1,Constants.BASE_PATH, Constants.FLYING_BIRD_IMAGE_NAME)
    global bird 
    bird = Bird(200,200,-1,-1,Constants.BASE_PATH, Constants.BIRD_IMAGE_NAME)

    global pipes 
    pipes = deque()
    initializePipes(pipes)

    global playIsOn 
    playIsOn = True

    global isCollision 
    isCollision = False
    
    global iterationNumber 
    iterationNumber = 0

    global isJump 
    isJump = False
    
    global jump 
    jump = Constants.JUMP_DISTANCE

    global score
    score = 0

pygame.init()
pygame.font.init()

##### set display window and text ######
window = pygame.display.set_mode((Constants.WINDOW_SIZE_WIDTH, 
                                  Constants.WINDOW_SIZE_HEIGHT))
pygame.display.set_caption(Constants.WINDOW_DISPLAY_TEXT)

#### fonts ###
# define the RGB value for white, 
#  green, blue colour . 
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
gameOverTextFont = pygame.font.Font(Constants.EIGHT_BIT_MADNESS_FILE, 65)
scoreAfterGameOverTextFont = pygame.font.Font(Constants.EIGHT_BIT_MADNESS_FILE, 40)
scoreTextFont = pygame.font.Font(Constants.EIGHT_BIT_MADNESS_FILE, 65)

background = None
flyingBird = None
bird = None
pipes = None
playIsOn = None
isCollision = None 
iterationNumber = None
isJump = None
jump = None
score = None
lastPipeCrossed = None

initGame()

while 1 == 1:

    iterationNumber += 1
    pygame.time.delay(Constants.UPDATE_WINDOW_TIME)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playIsOn = False
    keys = pygame.key.get_pressed()

    if not playIsOn:
        if keys[pygame.K_SPACE]:
            initGame()
        continue

    if keys[pygame.K_SPACE]:
        jump = Constants.JUMP_DISTANCE
        isJump = True

    if isJump:
        if jump >= -1 * Constants.JUMP_DISTANCE:
            neg = 1
            if jump < 0:
                neg = -1
            #bird.yCoordinate -= ( jump ** 2 ) * 0.600 * neg
            bird.changeCoordinate(-1 * ( jump ** 2 ) * 0.600 * neg)
            jump -= 1

            bird.changeCoordinate(-1 * Constants.GRAVITY_FALL_DISTANCE)
            #bird.yCoordinate -= Constants.GRAVITY_FALL_DISTANCE
        else:
            jump = Constants.JUMP_DISTANCE
            isJump = False

    bird.changeCoordinate(Constants.GRAVITY_FALL_DISTANCE)
    #bird.yCoordinate += Constants.GRAVITY_FALL_DISTANCE

    while len(pipes) < 10:
        newNorthPipeHeight = random.randint(Constants.MIN_HEIGHT_OF_PIPE, 
                                Constants.GROUND_Y_COORDINATE-(Constants.MIN_HEIGHT_OF_PIPE+Constants.GAP_BETWEEN_PIPES))
        newSouthPipeHeight = Constants.GROUND_Y_COORDINATE - (Constants.GAP_BETWEEN_PIPES + newNorthPipeHeight)

        latestNorthPipe, _ = pipes[-1]
        latestPipeX = latestNorthPipe.xCoordinate
        
        pipes.append(generateNewPipePair(latestPipeX + Constants.NEXT_PIPE_ADDITION_GAP,
                                            newNorthPipeHeight,
                                            Constants.GROUND_Y_COORDINATE,
                                            Constants.PIPE_WIDTH,
                                            Constants.GAP_BETWEEN_PIPES))

    background.display(window)

    if isJump:
        flyingBird.xCoordinate = bird.xCoordinate
        flyingBird.yCoordinate = bird.yCoordinate
        flyingBird.display(window)
    else:
        bird.display(window)

    updateCoordinates(pipes, Constants.VELOCITY_OF_PIPES)
    removeCoordinatesToLeftOfWindow(pipes, Constants.PIPE_WIDTH)

    for northPipe, southPipe in pipes:            
        if northPipe.xCoordinate >= 0 & northPipe.xCoordinate < 500:

            northPipe.display(window)
            southPipe.display(window)

            # Check for collisions
            if not isCollision:
                if isJump:
                    isCollision = Utils.isCollision(flyingBird, northPipe, southPipe, Constants.BIRD_Y_COORDINATE_MIN, Constants.BIRD_Y_COORDINATE_MAX)
                else:
                    isCollision = Utils.isCollision(bird, northPipe, southPipe, Constants.BIRD_Y_COORDINATE_MIN, Constants.BIRD_Y_COORDINATE_MAX)
            
            # Increment score
            if (northPipe.xCoordinate + Constants.PIPE_WIDTH) <=  bird.xCoordinate and \
               (northPipe.xCoordinate + Constants.PIPE_WIDTH) >= (bird.xCoordinate - Constants.GAP_TO_COUNT_SCORE) and \
               not(lastPipeCrossed is northPipe):
                lastPipeCrossed = northPipe
                score += 1
        else:
            break

    if isCollision:
        gamOverText = gameOverTextFont.render('Game Over!', False, blue)
        window.blit(gamOverText,(130,150))
        scoreText = scoreAfterGameOverTextFont.render('Score: ' + str(score), False, blue)
        window.blit(scoreText, (200, 200))
        playIsOn = False
    else:
        scoreText = scoreTextFont.render(str(score), False, blue)
        window.blit(scoreText, (200, 10))

    pygame.display.update()