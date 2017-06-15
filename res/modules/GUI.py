"""
This is the GUI file in charge of GUIs
"""

import pygame;
import sys;

sys.path.append("res"); #Change path to the modules folder.
from modules import TextBox;

width = 0;
height = 0;
FPS = 0;

pygame.font.init();

smallFont = pygame.font.Font("res/other_assets/kenvector_future.ttf", 10)
mediumFont = pygame.font.Font("res/other_assets/kenvector_future.ttf", 30);
fontColor = (0, 0, 0);

# List of buttons in-game so I can check for mouse inputs for all.
buttons = [];

def init(w, h, fps):
    global FPS,width,height;
    width = w;
    height = h;
    FPS = fps;


class HighscoresPanel:
    def __init__(self, game):
        self.size = (width-40, height-40);

        self.game = game;
        self.title = Label("Leaderboard", (100, 50), 50, self);
        
        self.searchLabel = Label("Search:", (width-450, 65), 30, self, True);
        self.searchBar = TextBox.TextBox(pygame.Rect((width-450, 100), (300, 60)));

        self.refreshScores();

        self.playBut = PlayButton(self, game, (150, 600), (250, 60));
        self.menuBut = MenuButton(self, game, (800, 600), (250, 60));

        self.img = pygame.image.load("res/sprites/UI/panel.png");

        self.surf = pygame.transform.scale(self.img, self.size);


    def update(self):
        self.searchBar.update();
        self.refreshScores();


    def refreshScores(self):
        self.scoreLabels = [];
        count = 0;
        text = self.searchBar.text;

        if(text == ""):
            text = None;

        for score in self.game.getTopScores(text):
            count += 1;
            lbl = Label(str(count) + ": " + score.name + "    :    " + str(score.score), (100, (count+1)*85), 25, self);
            self.scoreLabels.append(lbl);


    def render(self, screen):

        self.surf = pygame.transform.scale(self.img, self.size);
        
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2];

        self.title.render();
        self.searchLabel.render();
        self.searchBar.render(self.surf);

        self.playBut.iButton.render();
        self.menuBut.iButton.render();

        for score in self.scoreLabels:
            score.render(self.surf);

        screen.blit(self.surf, pPos);


    def handleClick(self, pos):
        if(self.playBut.iButton.isInside(self.translatePos(pos))):
            self.playBut.action();
        elif(self.menuBut.iButton.isInside(self.translatePos(pos))):
            self.menuBut.action();

        self.searchBar.handleClick(self.translatePos(pos));



    def handleHover(self, pos):
        if(self.playBut.iButton.isInside(self.translatePos(pos))):
            self.playBut.iButton.hover = True;
        else:
            self.playBut.iButton.hover = False;

        if(self.menuBut.iButton.isInside(self.translatePos(pos))):
            self.menuBut.iButton.hover = True;
        else:
            self.menuBut.iButton.hover = False;


    #Turns raw mouse pos data into mouse data on panel.
    def translatePos(self, pos):
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2];
        newPos = (pos[0]-pPos[0], pos[1]-pPos[1]);

        return newPos;




class MainMenuPanel:
    def __init__(self, game):
        self.size = (width-40, height-40);
        self.game = game;

        self.setupButtons();

        img = pygame.image.load("res/sprites/UI/panel.png"); #TODO add cool background.
        self.surf = pygame.transform.scale(img, self.size);



    def setupButtons(self):
        self.buttons = [];

        playBut = PlayButton(self, self.game, (100, 100));
        leaderButton = LeaderboardButton(self, self.game, (100, 300));

        self.buttons.append(playBut);
        self.buttons.append(leaderButton);


    def render(self, screen):
        
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2];
        screen.blit(self.surf, pPos);

        for button in self.buttons:
            button.iButton.render();


    def handleClick(self, pos):
        for button in self.buttons:
            if(button.iButton.isInside(self.translatePos(pos))):
                button.action();


    def handleHover(self, pos):
        for button in self.buttons:
            if(button.iButton.isInside(self.translatePos(pos))):
                button.iButton.hover = True;
            else:
                button.iButton.hover = False;


    #Turns raw mouse pos data into mouse data on panel.
    def translatePos(self, pos):
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2];
        newPos = (pos[0]-pPos[0], pos[1]-pPos[1]);

        return newPos;

class SetHighscorePanel:
    def __init__(self, game):
        self.size = (width-40, height-40);
        self.game = game;


        self.img = pygame.image.load("res/sprites/UI/panel.png");

        self.surf = pygame.transform.scale(self.img, self.size);


        self.setupButtons();


    def setupButtons(self):

        self.surf = pygame.transform.scale(self.img, self.size);

        self.buttons = [];

        self.title = Label("You set a new highscore!", (width/2, 150), 50, self, True);
        self.desc = Label("Score: " + str(self.game.score) + ", Please type your name for the leaderboards.", (width/2, 200), 20, self, True);

        self.textbox = TextBox.TextBox(pygame.Rect((width/2-200, height/2-60), (400, 60)));

        done = DoneButton(self);

        reset = ResetButton(self, self.game);

        self.buttons.append(done);
        self.buttons.append(reset);


    def finish(self):
        self.game.addNewScore(self.textbox.text);
        self.game.goToMainMenu();


    def render(self, screen):
        
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2];
        screen.blit(self.surf, pPos);

        self.title.render();
        self.desc.render();

        self.textbox.render(self.surf);

        for button in self.buttons:
            button.iButton.render();

    def update(self):
        self.textbox.update();

    def handleClick(self, pos):

        self.textbox.handleClick(self.translatePos(pos));

        for button in self.buttons:
            if(button.iButton.isInside(self.translatePos(pos))):
                button.action();


    def handleHover(self, pos):
        for button in self.buttons:
            if(button.iButton.isInside(self.translatePos(pos))):
                button.iButton.hover = True;
            else:
                button.iButton.hover = False;


    #Turns raw mouse pos data into mouse data on panel.
    def translatePos(self, pos):
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2];
        newPos = (pos[0]-pPos[0], pos[1]-pPos[1]);

        return newPos;


class HUD:
    def __init__(self, game):
        # Create transparent surface the size of the screen.
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA, 32);
        self.surf = self.surf.convert_alpha();

        self.game = game;

    def render(self, screen):
        scoreSurf = mediumFont.render("SCORE: " + str(self.game.score), True, (255, 255, 255));

        screen.blit(scoreSurf, (5, 5));


class Label:
    def __init__(self, text, pos, textSize=15, panel=None, centered=False):
        self.pos = pos;
        self.text = text;
        self.size = textSize;
        self.panel = panel;

        self.centered = centered;

        self.font = pygame.font.Font("res/other_assets/kenvector_future.ttf", self.size);


    def render(self, screen=None):

        if(screen == None):
            screen = self.panel.surf;

        self.image = self.font.render(self.text, True, (0, 0, 0));

        pos = None;

        if(self.centered):
            pos = [self.pos[0]-self.image.get_width()/2, self.pos[1]-self.image.get_height()/2];

        else:
            pos = self.pos;
        
        screen.blit(self.image, pos);

class Button:
    def __init__(self, text, pos, panel=None, dim=(150, 45)):
        self.pos = pos;
        self.text = text;
        self.dim = dim;
        self.disabled = False;
        self.hover = False;
        self.panel = panel;

        self.setupImages();
        self.image = self.images[0];
        buttons.append(self);


    def render(self, screen=None):
        if(screen == None):
            screen = self.panel.surf;

        self.updateImage();
        screen.blit(self.image, self.pos);
        self.renderText(screen);
        

    def renderText(self, screen):
        surf = mediumFont.render(self.text, True, fontColor);
        pos = (self.getMiddlePos()[0]-surf.get_width()/2,
                self.getMiddlePos()[1]-surf.get_height()/2);

        screen.blit(surf, pos);


    def getMiddlePos(self):
        return (self.pos[0]+self.image.get_width()/2, self.pos[1]+self.image.get_height()/2);


    def isInside(self, pos):
        corner = [self.pos[0]+self.dim[0], self.pos[1]+self.dim[1]];

        if(pos[0]>self.pos[0] and pos[1]>self.pos[1]):
            if(pos[0]<corner[0] and pos[1]<corner[1]):
                return True;


    def updateImage(self):
        if(not self.disabled):
            if(self.hover):
                self.image = self.images[1];
            else:
                self.image = self.images[0];
        else:
            self.image = self.images[2];


    #Scales and sets images for button states.
    def setupImages(self):
        self.images = [];
        # [default, hover, disabled]
        images = ["res/sprites/UI/button.png",
                "res/sprites/UI/buttonHover.png",
                "res/sprites/UI/buttonDisabled.png"];

        for image in images:
            img = pygame.image.load(image);
            self.images.append(pygame.transform.scale(img, self.dim));
 




class PlayButton:
    def __init__(self, panel, game, pos, dim=(400, 60)):
        # i stands for inside.
        self.iButton = Button("Play", pos, panel, dim);
        self.game = game;

    def action(self):
        self.game.reset();


class DoneButton:
    def __init__(self, panel):
        # i stands for inside.
        self.iButton = Button("Done", (width/2-250, 500), panel, (500, 65));
        self.panel = panel;

    def action(self):
        self.panel.finish();



class MenuButton:
    def __init__(self, panel, game, pos, dim=(400, 60)):
        # i stands for inside.
        self.iButton = Button("Main Menu", pos, panel, dim);
        self.game = game;

    def action(self):
        self.game.goToMainMenu();


class LeaderboardButton:
    def __init__(self, panel, game, pos, dim=(400, 60)):
        # i stands for inside.
        self.iButton = Button("Leaderboard", pos, panel, dim);
        self.game = game;

    def action(self):
        self.game.showLeaderboards();


class ResetButton:
    def __init__(self, panel, game):
        # i stands for inside.
        self.iButton = Button("Retry", (width/2-250, 600), panel, (500, 65));
        self.game = game;

    def action(self):
        self.game.reset();









