"""
This is the GUI file in charge of GUIs components.
"""

import pygame;
import sys;

sys.path.append("res"); #Change path to the modules folder.
from modules import TextBox;

#Constants.
width = 0;
height = 0;
FPS = 0;

#Initialise the font.
pygame.font.init();

#Sets used fonts.
smallFont = pygame.font.Font("res/other_assets/kenvector_future.ttf", 10)
mediumFont = pygame.font.Font("res/other_assets/kenvector_future.ttf", 30);
fontColor = (0, 0, 0);

# List of buttons in-game so I can check for mouse inputs for all.
buttons = [];

#Init function used for setting of constant values.
def init(w, h, fps):
    global FPS,width,height;
    width = w;
    height = h;
    FPS = fps;


#Class that stores panel for highscores.
class HighscoresPanel:
    def __init__(self, game):
        self.size = (width-40, height-40); #The size of the panel

        self.game = game; #Instance of game object.
        self.title = Label("Leaderboard", (100, 50), 50, self); #Title Label.
        
        self.searchLabel = Label("Search:", (width-450, 65), 30, self, True);
        self.searchBar = TextBox.TextBox(pygame.Rect((width-450, 100), (300, 60))); #Text box for earching.

        self.refreshScores(); #Refreshs all the scores.

        self.playBut = PlayButton(self, game, (150, 600), (250, 60)); #Play button.
        self.menuBut = MenuButton(self, game, (800, 600), (250, 60)); #Menu button.

        self.img = pygame.image.load("res/sprites/UI/panel.png"); #Background image of panel.

        self.surf = pygame.transform.scale(self.img, self.size); #The scaled image of the panel.


    #Called to update Highscore.
    def update(self):
        self.searchBar.update();
        self.refreshScores(); #Refreshes scores every game tick.


    #Refreshes the scores shown on the leaderboard.
    def refreshScores(self):
        self.scoreLabels = []; #Stores the labels of the scores.
        count = 0; #Counts through loop.
        text = self.searchBar.text; #The text in the search bar.

        if(text == ""): #When the text in the textbox is empty.
            text = None;

        for score in self.game.getTopScores(text): #For every score in top scores.
            count += 1;
            lbl = Label(str(count) + ": " + score.name + "    :    " + str(score.score), (100, (count+1)*85), 25, self); #Set label.
            self.scoreLabels.append(lbl); #Add label to score labels.


    #Called every tick to render image.
    def render(self, screen):

        self.surf = pygame.transform.scale(self.img, self.size); #Scale surface object.
        
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2]; #Stands for panel position (top left).

        #Render all objects.
        self.title.render();
        self.searchLabel.render();
        self.searchBar.render(self.surf);

        self.playBut.iButton.render();
        self.menuBut.iButton.render();

        for score in self.scoreLabels:
            score.render(self.surf);

        screen.blit(self.surf, pPos); #Add to screen.


    #Handle click of objects.
    def handleClick(self, pos):
        #For the buttons.
        if(self.playBut.iButton.isInside(self.translatePos(pos))):
            self.playBut.action();
        elif(self.menuBut.iButton.isInside(self.translatePos(pos))):
            self.menuBut.action();

        self.searchBar.handleClick(self.translatePos(pos)); #Handle click for text box.


    #Handle hover of objects.
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


#The panel of the main menu.
class MainMenuPanel:
    def __init__(self, game):
        self.size = (width-40, height-40);
        self.game = game;

        self.setupButtons();

        #Create empty Surface.
        self.surf = pygame.Surface(self.size, pygame.SRCALPHA, 32);
        self.surf = self.surf.convert_alpha();


    #Setup all the buttons.
    def setupButtons(self):
        self.buttons = [];

        playBut = PlayButton(self, self.game, (700, 300));
        leaderButton = LeaderboardButton(self, self.game, (700, 500));

        self.buttons.append(playBut);
        self.buttons.append(leaderButton);


    #Render all the components.
    def render(self, screen):
        
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2]; #Panel position.
        screen.blit(self.surf, pPos);

        for button in self.buttons:
            button.iButton.render();


    #Handle clicking of the components.
    def handleClick(self, pos):
        for button in self.buttons:
            if(button.iButton.isInside(self.translatePos(pos))):
                button.action(); #Calls the action of the button.

    #Handle hover of the ccomponents.
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


#Add new highscore panel.
class SetHighscorePanel:
    def __init__(self, game):
        self.size = (width-40, height-40);
        self.game = game;


        self.img = pygame.image.load("res/sprites/UI/panel.png");

        self.surf = pygame.transform.scale(self.img, self.size);


        self.setupButtons();


    #Setup of buttons.
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


    #Called when "Done" button is clicked.
    def finish(self):
        self.game.addNewScore(self.textbox.text);
        self.game.goToMainMenu();


    #Renders components.
    def render(self, screen):
        
        pPos = [(width-self.size[0])/2, (height-self.size[1])/2]; #Panel position.
        screen.blit(self.surf, pPos);

        self.title.render();
        self.desc.render();

        self.textbox.render(self.surf); #Render textbox.

        for button in self.buttons:
            button.iButton.render();


    #Called every game tick.
    def update(self):
        self.textbox.update();


    #Handle click of components.
    def handleClick(self, pos):

        self.textbox.handleClick(self.translatePos(pos));

        for button in self.buttons:
            if(button.iButton.isInside(self.translatePos(pos))):
                button.action();


    #Handles hover of components.
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


#The HUD object, stands for Heads Up Display. Designed to show score.
class HUD:
    def __init__(self, game):
        # Create transparent surface the size of the screen.
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA, 32);
        self.surf = self.surf.convert_alpha();

        self.game = game;


    #Renders score.
    def render(self, screen):
        scoreSurf = mediumFont.render("SCORE: " + str(self.game.score), True, (255, 255, 255));

        screen.blit(scoreSurf, (5, 5));


#Label GUI component class.
class Label:
    def __init__(self, text, pos, textSize=15, panel=None, centered=False):
        self.pos = pos;
        self.text = text;
        self.size = textSize;
        self.panel = panel;

        self.centered = centered; #Text is centered on pos.

        self.font = pygame.font.Font("res/other_assets/kenvector_future.ttf", self.size); #Font object.


    #Renders the text.
    def render(self, screen=None):

        if(screen == None):
            screen = self.panel.surf;

        self.image = self.font.render(self.text, True, (0, 0, 0));

        pos = None;

        if(self.centered): #If text is centered.
            pos = [self.pos[0]-self.image.get_width()/2, self.pos[1]-self.image.get_height()/2];

        else:
            pos = self.pos;
        
        screen.blit(self.image, pos);


#Button GUI component class.
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


    #Called every tick for rendering object.
    def render(self, screen=None):
        if(screen == None):
            screen = self.panel.surf;

        self.updateImage();
        screen.blit(self.image, self.pos);
        self.renderText(screen);
        

    #Renders Text on button.
    def renderText(self, screen):
        surf = mediumFont.render(self.text, True, fontColor);
        pos = (self.getMiddlePos()[0]-surf.get_width()/2,
                self.getMiddlePos()[1]-surf.get_height()/2);

        screen.blit(surf, pos);

    #Returns the middle position of the button. 
    def getMiddlePos(self):
        return (self.pos[0]+self.image.get_width()/2, self.pos[1]+self.image.get_height()/2);

    #Checks if the position given is inside the button.
    def isInside(self, pos):
        corner = [self.pos[0]+self.dim[0], self.pos[1]+self.dim[1]];

        if(pos[0]>self.pos[0] and pos[1]>self.pos[1]):
            if(pos[0]<corner[0] and pos[1]<corner[1]):
                return True;

    #Updates the image.
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
 



#Class for the play button.
class PlayButton:
    def __init__(self, panel, game, pos, dim=(400, 60)): #dim = Dimensions.
        # i stands for inside.
        self.iButton = Button("Play", pos, panel, dim);
        self.game = game; #Game instance.
    
    #Function called when button is clicked.
    def action(self):
        self.game.reset();

#Done button, found when setting a new highscrore
class DoneButton:
    def __init__(self, panel):
        # i stands for inside.
        self.iButton = Button("Done", (width/2-250, 500), panel, (500, 65));
        self.panel = panel;

    #Function called when button is clicked.
    def action(self):
        self.panel.finish();


#Menu button class, sends user to the main menu.
class MenuButton:
    def __init__(self, panel, game, pos, dim=(400, 60)):
        # i stands for inside.
        self.iButton = Button("Main Menu", pos, panel, dim);
        self.game = game;

    #Function called when button is clicked.
    def action(self):
        self.game.goToMainMenu();

#Leaderboard button class sends player to leaderboard.
class LeaderboardButton:
    def __init__(self, panel, game, pos, dim=(400, 60)):
        # i stands for inside.
        self.iButton = Button("Leaderboard", pos, panel, dim);
        self.game = game;

    #Function called when button is clicked.
    def action(self):
        self.game.showLeaderboards();


#Reset button class, resets the game when pressed.
class ResetButton:
    def __init__(self, panel, game):
        # i stands for inside.
        self.iButton = Button("Retry", (width/2-250, 600), panel, (500, 65));
        self.game = game;

    #Function called when button is clicked.
    def action(self):
        self.game.reset();









