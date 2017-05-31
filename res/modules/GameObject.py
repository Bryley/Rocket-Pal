"""
This is Game Objects File

"""

import pygame;
import os;
import math;
import random;

width = 0;
height = 0;
FPS = 0;

rocketImagePath = "res/sprites/rocket.png";
backgroundImagePath = "res/sprites/background.png";

def init(w, h, fps):

    global FPS,width,height;
    width = w;
    height = h;
    FPS = fps;

#Converts pixels to meters.
def toMeters(pixels):
    rate = 12; #1 meter = [rate] pixels;
    if(type(pixels) is list or type(pixels) is tuple):
         return [pixels[0]/rate, pixels[1]/rate];
    else:
         return pixels/rate;

#Converts meters to pixels.
def toPixels(meters):
    rate = 12; #1 meter = [rate] pixels;
    if(type(meters) is list or type(meters) is tuple):
         return [meters[0]*rate, meters[1]*rate];
    else:
         return meters*rate;

class Star:
    def __init__(self):

        self.scale = 1;

        image = pygame.image.load("res/sprites/star.png");

        self.image = pygame.transform.scale(image, (int(image.get_width()*self.scale),
            int(image.get_height()*self.scale)));

        self.radius = self.image.get_width()/2;

        self.pos = self.generateRandomPos();

    def render(self, screen):
        #Sets pos to top left.
        newPos = (self.pos[0]-self.image.get_width()/2, self.pos[1]-self.image.get_height()/2);

        screen.blit(self.image, newPos);

    def setNewPos(self):
        self.pos = self.generateRandomPos();

    def generateRandomPos(self):
        minX = self.radius;
        maxX = width-self.radius;

        minY = self.radius;
        maxY = height-self.radius;

        xPos = random.randint(minX, maxX);
        yPos = random.randint(minY, maxY);

        return [xPos, yPos];

class Planet:
    def __init__(self, pos, imgPath):
        self.imgPath = imgPath;
        self.scale = 1;
        
        self.pos = pos;

        image = pygame.image.load(self.imgPath);

        self.image = pygame.transform.scale(image, (int(image.get_width()*self.scale),
            int(image.get_height()*self.scale)));
        self.radius = self.image.get_width()/2;

    def render(self, screen):
        #Sets position to top left.
        newPos = (self.pos[0]-self.image.get_width()/2, self.pos[1]-self.image.get_height()/2);

        screen.blit(self.image, newPos);


    def update(self):
        pass;

    def getMiddlePos(self):
        return (self.pos);

#Planet Types:
class EarthPlanet:
    def __init__(self, pos):
        self.planet = Planet(pos, "res/sprites/earth.png");

    def render(self, screen):
        self.planet.render(screen);

#TODO add obsticle planets.

class Rocket:
    def __init__(self, game):
        self.pos = [50, 25]; #in meters. (Also is coordinates of the middle of the rocket).
        self.velocity = [0, 0]; #in meters per second.
        self.acceleration = [0, 0]; #in meters per second per second.
        self.scale = 1;
        self.radius = 40;

        self.game = game;

        image = pygame.image.load(rocketImagePath);

        self.image = pygame.transform.scale(image, (int(image.get_width()*self.scale),
            int(image.get_height()*self.scale)));

    def render(self, screen):
        #Sets new position so it is in the center of the rocket.
        newPos = (int(toPixels(self.pos[0])-self.image.get_width()/2),
                int(toPixels(self.pos[1])-self.image.get_height()/2));

        screen.blit(self.image, newPos);


    def update(self, planet, star):
        if(planet != None):
            self.calculateAcceleration(planet.planet);
        else:
             self.acceleration = [0, 0];

        self.updatePosition();

        if(self.checkDeath(planet)):
            self.game.reset();

        if(self.checkStarCollision(star)):
            self.game.addScore();


    def checkStarCollision(self, star):
        pos = toPixels(self.pos);

        distance = math.sqrt((star.pos[0]-pos[0])**2 + (star.pos[1]-pos[1])**2 );
        radiusSum = self.radius+star.radius;

        if(distance < radiusSum):
            return True;
        else:
            return False;

    def checkDeath(self, planet):
        #pos = rocket pos in pixels.
        pos = (toPixels(self.pos[0]), toPixels(self.pos[1]));

        #Out of screen.
        if(pos[0]-self.image.get_width()*self.scale/2 < 0 or pos[0]+self.image.get_width()*self.scale/2 > width):
            return True;
        if(pos[1]-self.image.get_height()*self.scale/2 < 0 or pos[1]+self.image.get_height()*self.scale/2 > height):
            return True;

        #Collision detection. # Done with distance between objects has to be greater than planet radius + rocket radius.
        if(planet != None):
            middlePos = planet.planet.getMiddlePos();
            distance = math.sqrt(( (pos[0]) - middlePos[0] )**2 + ( (pos[1]) - middlePos[1] )**2);

            if(planet.planet.radius + self.radius > distance):
                #Collision detected.
                return True;

        return False;


    def reset(self, pos, vel):
        self.pos = pos;
        self.velocity = vel;
        self.acceleration = [0, 0];

    def calculateAcceleration(self, planet):
        #These are 2 of the sides of the triangle.
        x = toMeters(planet.pos[0])-self.pos[0];
        y = toMeters(planet.pos[1])-self.pos[1];

        G = 6670; #Gravitational Constant. (Should be 6.67x10^-14 but has been changed to 6.67x10^3 so planets mass (10^17 kg) is included in equation to reduce lag.)

        #This is the hypotenuse of the triangle.
        #This is also the acceleration due to gravity equations used in physics. (G has planets mass included in formula)
        a = G/(x**2+y**2);

        #Angle is the angle of rocket relative to center of planet.
        angle = abs(math.atan(y/x));
        #TODO change angle of rocket from this angle value.

        #Find the signs (positive or negative) of the 2 adjacent sides of the triangle.
        xSign = 1;
        #Make sure x doesn't equal 0 (otherwise a runime error will occur).
        if(x != 0):
             #This will make xSign either equal 1 or -1.
             xSign = x/abs(x);

        ySign = 1;
        #Make sure y doesn't equal 0 (otherwise a runime error will occur).
        if(y != 0):
             #This will make ySign either equal 1 or -1.
             ySign = y/abs(y);

        #Split the acceleration into 2 components (x and y).
        accX = xSign * math.cos(angle) * a;

        accY = ySign * math.sin(angle) * a;

        self.acceleration = [accX, accY];


    #Updates the rockets position and velocity.
    def updatePosition(self):
        seconds = 1/FPS; #This is the change in time between each update.
        self.pos[0] += self.velocity[0]*seconds;
        self.pos[1] += self.velocity[1]*seconds;
        self.velocity[0] += self.acceleration[0]*seconds;
        self.velocity[1] += self.acceleration[1]*seconds;


class Level:
    def __init__(self, name, levelObjects, size=[width, height], pos=[5, 5], vel=[0, 0]):
        self.levelObjects = levelObjects;
        self.name = name; #Name of the level.

        self.size = size;
        #The surface of the object.
        self.surf = pygame.Surface(size);

        self.star = Star();

        #For reset:
        self.constantObjects = levelObjects;
        self.rocketPos = pos;
        self.rocketVel = vel;

    def render(self, screen):
        #Load background image.
        self.surf.blit(pygame.image.load(backgroundImagePath), (0,0));
        #TODO scale image to level size.

        #Render objects in level.
        for object in self.levelObjects:
            object.render(self.surf);

        self.star.render(self.surf);

        screen.blit(self.surf, (0, 0)); #Add to screen.


    def update(self):

        for object in self.levelObjects:
            object.update(FPS);

    def reset(self, camera):
        self.levelObjects = self.constantObjects;
        camera.rocket.reset(list(self.rocketPos), list(self.rocketVel));
        self.star.setNewPos();

#Some functions within class are not needed and are obsolete.
class Camera:
    def __init__(self, level, rocket, planet=None):
        self.pos = [0, 0];
        self.scale = 1;
        self.level = level;
        self.rocket = rocket;
        self.planet = planet; #Camera will follow planet when it exists.

        self.velocity = [0, 0];
        self.trackingSpeed = 100; #As percentage

    def changeScale(self, scale):
        # Makes sure scale is not too big or too small.
        if(scale < 0 or self.level.surf.get_width()*scale > 15000 or self.level.surf.get_height()*scale > 15000):
            self.scale = scale;

    def render(self, screen):

        surf = self.level.surf.copy();
        #Render Level using camera settings scale and position.
        self.level.render(surf);

        #Render planet (if exists)
        if(self.planet != None):
            self.planet.render(self.level.surf);

        self.rocket.render(self.level.surf);
        #Scale level.
        levelSurf = pygame.transform.smoothscale(self.level.surf,
                (int(self.level.surf.get_width()*self.scale),
                  int(self.level.surf.get_height()*self.scale)));

        #Screen surface. # CHANGED pos to 0, 0 after desiding class is obsolite.
        screen.blit(levelSurf, pygame.Rect((0, 0), (width, height)));

    def update(self):
        self.rocket.update(self.planet, self.level.star);
        self.level.update();

    def reset(self):
        self.planet = None;
        self.level.reset(self);

