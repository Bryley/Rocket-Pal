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
    width = w;
    height = h;
    FPS = fps;

class Rocket:
    def __init__(self):
        self.pos = [100, 100];
        self.velocity = [0, 0];
        self.acceleration = [0, 0];
        self.ticksCounter = 0;
        self.scale = 0.25;

        self.image = pygame.image.load(rocketImagePath);

    def render(self, screen):
        newImg = pygame.transform.scale(self.image, (int(self.image.get_width()*self.scale), int(self.image.get_height()*self.scale)));

        screen.blit(newImg, self.pos);

    def update(self):

        self.ticksCounter += 1;
        # Run Every Second
        if(self.ticksCounter >= FPS):
            self.updatePosition();
            self.ticksCounter = 0;


    def updatePosition(self):
        self.velocity[0] += self.acceleration[0];
        self.velocity[1] += self.acceleration[1];


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
        self.scale = 0.5;
        self.level = level;
        self.rocket = rocket;

    def changePosition(self, pos):
        if(self.checkPos(pos)):
            self.pos = pos;

    def changeScale(self, scale):
        # Makes sure scale is not too big or too small.
        if(scale > 0 or self.level.surf.get_width()*scale>15000 or self.level.surf.get_height()*scale>15000):
            self.scale = scale;

    def checkPos(self, pos):
        #If position is less than 0 (out of the level).
        if(pos[0] < 0 and pos[1] < 0):
            return False;
        #Else if position of the camera is showing a part out of the screen.
        elif(pos[0]+width>self.level.width*self.scale and
         pos[1]+height>self.level.height*self.scale):
            return False;
        else:
            return True;

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
        pass; #TODO update to follow rocket.


