import pygame;
import sys;
import os;
sys.path.append("res"); #Change path to the modules folder.
from modules import GameObject;
from modules import GUI;
from modules import TextBox;

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
GUI.init(width, height, FPS);
TextBox.init(width, height, FPS);

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
        
        self.score = 0;

        self.levels = createLevels();
        self.level = self.levels[0];
        self.player = GameObject.Rocket(self);
        self.hud = GUI.HUD(self);
        self.mainMenuPanel = GUI.MainMenuPanel(self);
        self.setHighscorePanel = GUI.SetHighscorePanel(self);
        self.leaderBoardPanel = GUI.HighscoresPanel(self);

        self.highscores = [];

        
        # 0 = Main Menu, 1 = In-Game, 2 = Highscore, 3 = Set Highscore.
        self.state = 0;

        self.camera = GameObject.Camera(self.level, self.player);


    def render(self):
        screen.fill((0, 0, 0));

        if(self.state == 1): # In-Game
            self.camera.render(screen);
            self.hud.render(screen);

        elif(self.state == 0): # Main Menu
            self.mainMenuPanel.render(screen);

        elif(self.state == 3): # Set Highscore
            self.setHighscorePanel.render(screen);

        elif(self.state == 2):
            self.leaderBoardPanel.render(screen);


    def goToMainMenu(self):
        self.state = 0;

    def showLeaderboards(self):
        self.state = 2;

    def handleMouseDown(self, pos):
        if(self.state == 1):
            self.addPlanet(pos);
       
    def handleMouseUp(self, pos):
        if(self.state == 1):
            self.removePlanet();
        elif(self.state == 0):
            self.mainMenuPanel.handleClick(pos);

        elif(self.state == 3):
            self.setHighscorePanel.handleClick(pos);

        elif(self.state == 2):
            self.leaderBoardPanel.handleClick(pos);


    def getTopScores(self, params=""):
        return [Highscore("p1", 5),Highscore("p2", 1),Highscore("p3", 7), Highscore("p4", 206), Highscore("p5", -15)]; # DEBUG


    def handleMouseHover(self, pos):
        if(self.state == 0):
            self.mainMenuPanel.handleHover(pos);

        elif(self.state == 3):
            self.setHighscorePanel.handleHover(pos);

        elif(self.state == 2):
            self.leaderBoardPanel.handleHover(pos);
        

    def addPlanet(self, pos):
        self.camera.planet = GameObject.EarthPlanet(pos);


    def removePlanet(self):
        self.camera.planet = None;


    def addScore(self, score=1):
        self.camera.level.star.setNewPos();
        self.score += score;


    def addNewScore(self, name):
        # Find correct spot in highscores list as it is ordered. (Insertion sort).
        #TODO.
        self.highscores.append(Highscore(name, self.score));


    def updatePlanet(self, pos):
        if(self.camera.planet == None):
            self.addPlanet(pos);

        self.camera.planet.pos = pos;


    def reset(self):
        self.camera.reset();
        self.score = 0;
        #TODO add saving of highscore and stuff.


    def startGame(self):
        self.state = 1;


    def update(self):
        if(self.state == 1):
            self.camera.update();

        elif(self.state == 0):
            pass;

        elif(self.state == 3):
            self.setHighscorePanel.update();


class Highscore:
    def __init__(self, name, score):
        self.name = name;
        self.score = score;


game = Game();

#Called to render the game.
def render():
    screen.fill((255,255,255));
    game.render();

# Called to update the game.
def update():
    game.update();


# Game Loop
while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False;
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            pos = event.pos;
            game.handleMouseDown(pos);

        elif(event.type == pygame.MOUSEBUTTONUP):
            pos = event.pos;
            game.handleMouseUp(pos);

        elif(event.type == pygame.MOUSEMOTION):
            pos = event.pos;
            game.handleMouseHover(pos);

        elif(event.type == pygame.KEYDOWN):
            key = event.key;
            TextBox.handlePressDown(key);

        elif(event.type == pygame.KEYUP):
            key = event.key;
            TextBox.handlePressUp(key);


    render();
    update();
    pygame.display.update(); #Update display.
    clock.tick(FPS);

pygame.quit();

