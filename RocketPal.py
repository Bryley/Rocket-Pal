import pygame;
import sys;
import os;
sys.path.append("res"); #Change path to the modules folder.
import GameObject;

#This centers the game window to  the middle of the monitor.
os.environ['SDL_VIDEO_CENTERED'] = '1';
#This initiates pygame.
pygame.init();

#Android aspect ratio is 16:10
width = 1200;
height = 750;

FPS = 30;
running = True;
mouseDown = False;

GameObject.init(width, height, FPS);

screen = pygame.display.set_mode((width, height));

pygame.display.set_caption("Rocket Pal - By Bryley");

clock = pygame.time.Clock();

def createLevels():
    levels = [];
    level1 = GameObject.Level("Level 1", [], [width, height]);  #TODO need to add objects.
    levels.append(level1);
    return levels;

class Game:

    def __init__(self):
        self.levels = createLevels();
        self.level = self.levels[0];
        self.player = GameObject.Rocket(self);

        self.camera = GameObject.Camera(self.level, self.player);

    def addPlanet(self, pos):
        self.camera.planet = GameObject.EarthPlanet(pos);

    def removePlanet(self):
        self.camera.planet = None;

    def updatePlanet(self, pos):
        if(self.camera.planet == None):
            self.addPlanet(pos);

        self.camera.planet.pos = pos;


game = Game();

#Called to render the game.
def render():
    screen.fill((255,255,255));
    game.camera.render(screen);

# Called to update the game.
def update():
    game.camera.update();


# Game Loop
while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False;
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            mouseDown = True;
            pos = event.pos;
            game.addPlanet(pos);
        elif(event.type == pygame.MOUSEBUTTONUP):
            mouseDown = False;
            pos = event.pos;
            game.removePlanet();
        elif(event.type == pygame.MOUSEMOTION):
            pos = event.pos;
            if(mouseDown):
                game.updatePlanet(pos);


    render();
    update();
    pygame.display.update(); #Update display.
    clock.tick(FPS);

pygame.quit();

"""
NTS:
 - Just fixed collision (sort of) using circles.
"""
