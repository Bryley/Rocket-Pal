"""
  _____            _        _     _____      _ 
 |  __ \          | |      | |   |  __ \    | |
 | |__) |___   ___| | _____| |_  | |__) |_ _| |
 |  _  // _ \ / __| |/ / _ \ __| |  ___/ _` | |
 | | \ \ (_) | (__|   <  __/ |_  | |  | (_| | |
 |_|  \_\___/ \___|_|\_\___|\__| |_|   \__,_|_| By Bryley
GitHub: https://github.com/Bryley/Rocket-Pal

This is my project of Rocket Pal! By Bryley.
This project is a school project and is a simple little fun addictive game. 

This is one of the 3 moudles created for this project.
Please note that the font and the GUI element designs are not mine.
Here is the link to the assets created by kenney:
    https://opengameart.org/content/ui-pack

Hope you enjoy the game.
"""
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

FPS = 60; #Frames per second
running = True;
SAVEPATH = "res/scores.txt"; #Stores the path to the saves file.

#Initiates my modules with constants.
GameObject.init(width, height, FPS);
GUI.init(width, height, FPS);
TextBox.init(width, height, FPS);

#Main screen that gets rendered onto.
screen = pygame.display.set_mode((width, height));

#The title above the screen.
pygame.display.set_caption("Rocket Pal - By Bryley");

#Clock used for reliable update per FPS
clock = pygame.time.Clock();

#Function originally made for 1st idea until game objective changed.
def createLevels():
    levels = [];
    level1 = GameObject.Level("Level 1", [], [width, height]);
    levels.append(level1);
    return levels;


#Class Games stores all the game data.
class Game:
    def __init__(self):
        
        self.score = 0;
        self.highscores = []; #List of highscores.

        self.levels = createLevels(); #List of levels (even though there is only one).
        self.level = self.levels[0];
        self.player = GameObject.Rocket(self);

        self.hud = GUI.HUD(self);
        self.mainMenuPanel = GUI.MainMenuPanel(self);
        self.setHighscorePanel = GUI.SetHighscorePanel(self);
        self.leaderBoardPanel = GUI.HighscoresPanel(self);

        self.camera = GameObject.Camera(self.level, self.player);

        
        # 0 = Main Menu, 1 = In-Game, 2 = Highscore, 3 = Set Highscore.
        self.state = 0;

        #Loads highscores from file.
        self.load();


    def render(self):

        if(self.state == 1): # In-Game
            self.camera.render(screen);
            self.hud.render(screen);

        elif(self.state == 0): # Main Menu
            self.mainMenuPanel.render(screen);

        elif(self.state == 3): # Set Highscore
            self.setHighscorePanel.render(screen);

        elif(self.state == 2): #Highscore
            self.leaderBoardPanel.render(screen);


#These navagate to different panels/screens
    def goToMainMenu(self):
        self.state = 0;
        TextBox.activeBox = None; # Disable TextBox.


    def showLeaderboards(self):
        self.state = 2;
        TextBox.activeBox = None; # Disable TextBox.


    def goToSetHighscorePanel(self):
        self.state = 3;
        self.setHighscorePanel.setupButtons();
        TextBox.activeBox = None; # Disables TextBox.


    def handleMouseDown(self, pos):
        if(self.state == 1): #Ingame
            self.addPlanet(pos);
       

    def handleMouseUp(self, pos):
        if(self.state == 1): #In-game
            self.removePlanet();
        elif(self.state == 0): #Main menu
            self.mainMenuPanel.handleClick(pos);

        elif(self.state == 3): #Set Highscore.
            self.setHighscorePanel.handleClick(pos);

        elif(self.state == 2): #Highscore.
            self.leaderBoardPanel.handleClick(pos);


    #Used for searching through data.
    def getTopScores(self, params=""):
        newList = [];
        
        #Checks for partial match.
        if(params != "" and params != None):
            for score in self.highscores:
                if(score.name.lower().startswith(params.lower())):
                    newList.append(score);

        else:
            newList = self.highscores;

           #Return the last 5 elements of the list (Top 5 as the list is ordered from lowest to highest).
        return newList[::-1][:5];


    def handleMouseHover(self, pos):
        if(self.state == 0): #Main Menu.
            self.mainMenuPanel.handleHover(pos);

        elif(self.state == 3): #Set Highscore.
            self.setHighscorePanel.handleHover(pos);

        elif(self.state == 2): #Highscore
            self.leaderBoardPanel.handleHover(pos);
        

    def addPlanet(self, pos):
        self.camera.planet = GameObject.EarthPlanet(pos);


    def removePlanet(self):
        self.camera.planet = None;


    #Adds a number to the current score ingame.
    def addScore(self, score=1):
        self.camera.level.star.setNewPos();
        self.score += score;


    #Sorts new highscores into an already ordered list. (Insertion sort).
    def addNewScore(self, name, score=None):

        if(score == None):
            score = self.score;

        highscore = Highscore(name, score);

        added = False; #If the score was added.
        count = 0;
        for hs in self.highscores:
            if(hs.score > score):
                self.highscores.insert(count, highscore);
                added = True;
                break;

            count += 1;

        if(added == False):
            self.highscores.append(highscore);


    def updatePlanet(self, pos):
        if(self.camera.planet == None):
            self.addPlanet(pos);

        self.camera.planet.pos = pos;


    #Resets the game.
    def reset(self):
        self.camera.reset();
        self.startGame();


    #Called to start the game.
    def startGame(self):
        self.state = 1;
        self.score = 0;


    #Called every FPS.
    def update(self):
        if(self.state == 1): #In-Game
            self.camera.update();

        elif(self.state == 0): #Main Menu.
            pass;

        elif(self.state == 2): #Highsccores panel.
            self.leaderBoardPanel.update();

        elif(self.state == 3): #Set Highscores Panel.
            self.setHighscorePanel.update();


    #Used for saving of highscores to file.
    def save(self):
        saveFile = open(SAVEPATH, "w");

        #Empties file.
        saveFile.truncate();

        saveFile.write("#This is the saves file for the scores. Please do not mess with it.\n");

        for score in self.highscores:
            saveFile.write(score.name + ":" + str(score.score) + "\n");

        saveFile.close();


    #Used for loading of the scores file.
    def load(self):
        saveFile = open(SAVEPATH, "r");

        contents = saveFile.readlines();

        for line in contents:
            if(line.startswith("#") == False): #If it starts with a '#' then it is a comment.
                if(":" in line): #If it contains a :.
                    data = line.split(":");

                    self.addNewScore(data[0], int(data[1]));

        saveFile.close();



#Class stores info for a particular highscore.
class Highscore:
    def __init__(self, name, score):
        self.name = name;
        self.score = score;


#Instance of game object.
game = Game();

#Called to render the game.
def render():
    
    #Stores background image in Surface object called img.
    img = pygame.image.load("res/sprites/menu.png");
    screen.blit(img, (0,0)); #Adds to screen.

    game.render();


# Called to update the game.
def update():
    game.update();


# Game Loop
while(running):
    #Loop through events in game.
    for event in pygame.event.get():
        #If the 'X' button in the top left (top right for mac) is pressed.
        if(event.type == pygame.QUIT):
            running = False;

        #If the mouse is clicked.
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            pos = event.pos;
            game.handleMouseDown(pos);

        #If the mouse is unclicked.
        elif(event.type == pygame.MOUSEBUTTONUP):
            pos = event.pos;
            game.handleMouseUp(pos);

        #If the mouse moves.
        elif(event.type == pygame.MOUSEMOTION):
            pos = event.pos;
            game.handleMouseHover(pos);

        #If a key is pressed.
        elif(event.type == pygame.KEYDOWN):
            key = event.key;
            TextBox.handlePressDown(key);

        #If a key is released.
        elif(event.type == pygame.KEYUP):
            key = event.key;
            TextBox.handlePressUp(key);


    render();
    update();
    pygame.display.update(); #Update display.
    clock.tick(FPS); #Makes this loop occur every FPS.


#Game saves scores to file.
game.save();
#Pygame quits.
pygame.quit();
