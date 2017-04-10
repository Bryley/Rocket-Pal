"""
This is Game Objects File

"""

import pygame;
import os;

width = 0;
height = 0;
FPS = 0;

rocketImagePath = "res/sprites/rocket.png";

def init(w, h, fps):

    global FPS,width,height;
    width = w;
    height = h;
    FPS = fps;

#Converts pixels to meters.
def toMeters(pixels):
    rate = 12; #1 meter = [rate] pixels;
    if(type(pixels) is list or type(pixels) is tuple):
         return (pixels[0]/rate, pixels[1]/rate);
    else:
         return pixels/rate;

#Converts meters to pixels.
def toPixels(meters):
    rate = 12; #1 meter = [rate] pixels;
    if(type(meters) is list or type(meters) is tuple):
         return (meters[0]*rate, meters[1]*rate);
    else:
         return meters*rate;


class Planet:
      def __init__(self, mass, pos, imgPath):
          self.mass = mass;
          self.imgPath = imgPath;

          self.pos = pos;


class Rocket:
    def __init__(self):
        self.pos = [5, 5]; #in meters.
        self.velocity = [0, 0]; #in meters per second.
        self.acceleration = [10, 5]; #in meters per second per second.
        self.scale = 0.05;

        self.image = pygame.image.load(rocketImagePath);

    def render(self, screen):
        #Scales the image so that the rocket is smaller.
        newImg = pygame.transform.scale(self.image, (int(self.image.get_width()*self.scale), int(self.image.get_height()*self.scale)));

        #Sets new position so it is in the center of the rocket.
        newPos = (toPixels(self.pos[0])-newImg.get_width()/2, toPixels(self.pos[1])-newImg.get_height()/2);
        screen.blit(newImg, newPos);

    def update(self):
        self.updatePosition();

    #Updates the rockets position and velocity.
    def updatePosition(self):
        seconds = 1/FPS; #This is the change in time between each update.
        self.pos[0] += self.velocity[0]*seconds;
        self.pos[1] += self.velocity[1]*seconds;
        self.velocity[0] += self.acceleration[0]*seconds;
        self.velocity[1] += self.acceleration[1]*seconds;


class Level:
    def __init__(self, name, levelObjects, size=[1000, 1000], velocity=[0, 0]):
        self.levelObjects = levelObjects;
        self.name = name; #Name of the level.
        #The surface of the object.
        self.size = size;
        self.surf = pygame.Surface(size);

    def render(self, screen):
        #Temporary. DEBUG.
        pygame.draw.rect(self.surf, (150, 0, 0), pygame.Rect(0, 0, self.size[0], self.size[1]));
        pygame.draw.rect(self.surf, (0, 200, 0), pygame.Rect(30, 30, self.size[0]-60, self.size[1]-60));

        for object in self.levelObjects:
            object.render(self.surf);

        screen.blit(self.surf, (0, 0)); #Add to screen.


    def update(self):
        for object in self.levelObjects:
            object.update(FPS);


class Camera:
    def __init__(self, level, rocket):
        self.pos = [0, 0];
        self.scale = 1;
        self.level = level;
        self.rocket = rocket;

    def changePosition(self, pos):
        self.pos = pos;

    def changeScale(self, scale):
        # Makes sure scale is not too big or too small.
        if(scale < 0 or self.level.surf.get_width()*scale > 15000 or self.level.surf.get_height()*scale > 15000):
            self.scale = scale;

    #Validate Position to return new position.
    def validatePos(self, pos):
        posX = pos[0];
        posY = pos[1];

        levelWidth = self.level.size[0];
        levelHeight = self.level.size[1];

        #If position is less than 0 (out of the level).
        if(pos[0] < 0):
            posX = 0;

        if(pos[1] < 0):
            posY = 0;

        #If position is greater than levelwidth times levelscale (out of level).
        if(pos[0]+width > levelWidth*self.scale):
            posX = (levelWidth*self.scale)-width;

        if(pos[1]+height > levelHeight*self.scale):
            posY = (levelHeight*self.scale)-height;

        #Return new position. (negative because it is relative to the level).
        return (-posX, -posY);

    def render(self, screen):

        surf = self.level.surf.copy();
        #Render Level using camera settings scale and position.
        self.level.render(surf);

        self.rocket.render(self.level.surf);
        #Scale level.
        levelSurf = pygame.transform.smoothscale(self.level.surf, (int(self.level.surf.get_width()*self.scale),
                  int(self.level.surf.get_height()*self.scale)));
        #Screen surface.
        screen.blit(levelSurf, pygame.Rect(self.pos, (width, height)));

    def update(self):
        rocketPos = toPixels(self.rocket.pos);

        #Finds new camera position (is negative because it is relative to level).
        cameraPos = self.validatePos( (rocketPos[0]-width/2, rocketPos[1]-height/2) );

        self.changePosition(cameraPos);
        print(self.pos);
        print(str(rocketPos) + "\n");


