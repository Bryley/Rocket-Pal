"""
This is the GUI file in charge of GUIs
"""

import pygame;

width = 0;
height = 0;
FPS = 0;

pygame.font.init();
mediumFont = pygame.font.Font("res/other_assets/SimplyPix.ttf", 20);

def init(w, h, fps):

    global FPS,width,height;
    width = w;
    height = h;
    FPS = fps;


class HUD:
    def __init__(self, game):
        # Create transparent surface the size of the screen.
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA, 32);
        self.surf = self.surf.convert_alpha();

        self.game = game;

    def render(self, screen):
        scoreSurf = mediumFont.render("SCORE: " + str(self.game.score), True, (255, 255, 255));

        screen.blit(scoreSurf, (5, 5));

"""
NTS:
    - Added stars.
    - Added basic score system.
    - No bugs (yet)
    - Should commit changes :)
"""













