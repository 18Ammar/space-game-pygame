import pygame as p
from Setting import Setting

sett = Setting()

class Bullet(p.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -10
        self.hitbox = p.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update(self):
        self.rect.y -= self.speed
        self.hitbox = p.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
