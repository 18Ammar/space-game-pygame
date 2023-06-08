import pygame
class Setting:
    def __init__(self):
        pygame.init()
        self.width =  1024
        self.height = 730
        self.bgColor = (255,0,220)
        self.white = (25,25,25)
        self.font = pygame.font.SysFont("arialblack", 40)
        self.TEXT_COL = (255, 255, 255)
        self.bult_width = 20
        self.bult_height = 20
        self.bult_img = pygame.image.load("data\\rec.png")
        self.bult_size = (self.bult_img.get_width() // 12, self.bult_img.get_height() //12)
        self.bult_img = pygame.transform.scale(self.bult_img, self.bult_size)
        self.bult_speed = 100
        self.stone_frequency = 6000 
        self.enemy_spaceship_frequency = 3000  
    
