"""
Textbox.py
Used for handling textboxes in the software.
"""

import pygame;

#Constants
black = (0, 0, 0);
borderGrey = (100, 100, 100);
white = (255, 255, 255);
border = 3;
FPS = 0;
width = 0;
height = 0;

textBoxes = [];
activeBox = None;

def init(w, h, fps):
    global FPS,width,height;
    width = w;
    height = h;
    FPS = fps;



# NOTE: This class was copied and pasted from a previous program I have written called Alarm Buddy.
#Class for the TextBox.
class TextBox:

    def __init__(self, rect, limit=10):
        self.rect = rect;
        #Limit is the maximum number of characters that the text box allows.
        self.limit = limit;
        
        self.surf = pygame.Surface((rect.width, rect.height));
        #Text is the acual text that the user has written.
        self.text = "";
        #The textInside variable is the text aswell as the '_' sign to show that the box is active.
        self.textInside = "";
        #Used for the blinking animation.
        self.timer = 0;
        self.font = pygame.font.Font("res/other_assets/kenvector_future.ttf", int(rect.height/2));
        #True if the left shift key is held down.
        self.capital = False;

        #Add the textbox to the global list.
        textBoxes.append(self);


    #Update the Text box and make the animation.
    def update(self):
        #If this Box is active.
        if(self == activeBox):

            #If the timer is greater than half the FPS. (Triggers 2 times per second).
            if(self.timer >= FPS/2):
                #If the underscore is already at the end of the textInside.
                if(self.textInside.endswith("_")):
                    self.textInside = self.textInside[:-1];

                #If the underscore is not at the end.
                else:
                   self.textInside += "_";

                #Reset the timer variable.
                self.timer = 0;

            #Add one to the timer.
            self.timer += 1;

        #If the box is not active.
        else:
            #Set the text inside to the text the user has written.
            self.textInside = self.text;

    #Render the box.
    def render(self, screen):
        pygame.draw.rect(self.surf, borderGrey, pygame.Rect(0, 0, self.rect.width, self.rect.height));
        pygame.draw.rect(self.surf, black,
                         pygame.Rect(border, border,
                                     self.rect.width-border*2, self.rect.height-border*2));

        self.drawText();
        screen.blit(self.surf, self.rect);

    #Draws the text to the screen.
    def drawText(self):
        fontArea = self.font.render(self.textInside, True, white);

        fontRec = fontArea.get_rect();

        fontRec.y = self.surf.get_height()/2;
        fontRec.x = 7;

        self.surf.blit(fontArea, fontRec);

    #Function gets key pressed and registers it with the TextBox.
    def keyPressAdd(self, key):
        global activeBox;

        #If this box is the active one.
        if(self == activeBox):

            #If the backspace key was pressed.
            if(key == pygame.K_BACKSPACE):
                #Delete the last letter.
                self.text = self.text[:-1];

            #If the Escape key was pressed.
            elif(key == pygame.K_ESCAPE):
                #Make the box unactive.
                activeBox = None;

            #If the text has reached the limit.
            if(len(self.text) >= self.limit):
                #Get out of the function.
                return;

            #If the Shift key was pressed.
            if(key == pygame.K_LSHIFT):
                #Make capital turned on.
                self.capital = True;

            #If the spacebar key was pressed.
            elif(key == pygame.K_SPACE):
                self.text += " ";

            #If the key pressed was between A to Z or 0 to 9.
            elif((key >= pygame.K_a and key <= pygame.K_z) or (key >= pygame.K_0 and key <= pygame.K_9)):
                #Convert the key code to a string.
                letter = chr(key);

                #If the shift key is down.
                if(self.capital):
                    #Convert to uppercase.
                    letter = letter.upper();

                #Add the letter to text.
                self.text += letter;

            #Change the textInside to the text.
            self.textInside = self.text;


    #Gets triggered when a key was released.
    def keyRelease(self, key):
        #If the key was shift.
        if(key == pygame.K_LSHIFT):
            #Turn capitals off.
            self.capital = False;

    #Handles the click of the textbox.
    def handleClick(self, pos):
        global activeBox;
        if(self.rect.collidepoint(pos)):
            activeBox = self;
            self.textInside += "_";

    #Sets the text inside the textbox.
    def setText(self, text):
        self.text = str(text);
        self.textInside = str(text);

    #Sets the position of the component.
    def setPos(self, x, y, centerX, centerY):
        self.rect.x = x;
        self.rect.y = y;
        
        if(centerX):
            self.rect.x = x-self.surf.get_width()/2;
        if(centerY):
            self.rect.y = y-self.surf.get_height()/2;


#Handles the key press for all textboxes.
def handlePressDown(key):
    for i in textBoxes:
        i.keyPressAdd(key);

#Handles the key up for all textboxes.
def handlePressUp(key):
    for i in textBoxes:
        i.keyRelease(key);
            









