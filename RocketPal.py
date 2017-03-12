import pygame;
import sys;
sys.path.append("res"); #Change path to the modules folder.
import GameObject;

pygame.init();

width = 1000;
height = 600;
FPS = 30;
running = True;

GameObject.init(width, height, FPS);

screen = pygame.display.set_mode((width, height));

pygame.display.set_caption("Rocket Pal - By Bryley");

clock = pygame.time.Clock();

def createLevels():
    levels = [];
    level1 = GameObject.Level("Level 1", [], [10000, 1000], [5, 0]);  #TODO need to add objects.
    levels.append(level1);
    return levels;

class Game:

    def __init__(self):
        self.levels = createLevels();
        self.level = self.levels[0];
        self.player = GameObject.Rocket();

        self.camera = GameObject.Camera(self.level, self.player);

game = Game();

#Called to render the game.
def render():
    screen.fill((255,255,255));
    game.camera.render(screen);

# Called to update the game.
def update():
    game.player.update();
    game.camera.update();

# Game Loop
while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False;
        elif(event.type == pygame.KEYDOWN):
            key = event.key;
            if(key == pygame.K_z):
                game.camera.scale += 0.25;
                print(game.camera.scale);
            elif(key == pygame.K_x):
                game.camera.scale -= 0.25;
                print(game.camera.scale);
        elif(event.type == pygame.KEYUP):
            key = event.key;
            if(key == pygame.K_z or key == pygame.K_x):
                #game.camera.scale = 0;
                pass;


    render();
    update();
    pygame.display.update(); #Update display.
    clock.tick(FPS);

pygame.quit();
