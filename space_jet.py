import pygame as p
from Setting import Setting
from bullet import Bullet
from time import sleep
import pygame_gui
import random

sett = Setting()

 





class Explosion(p.sprite.Sprite):
	def __init__(self, x, y):
		p.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = p.image.load(f"data/exp{num}.png")
			img = p.transform.scale(img, (200, 200))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 10
		self.counter += 1
                
		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()








class Stone :
    def __init__(self):
        # Load images of the stone and the pin from a folder named "data"
        self.image = p.image.load('data\\ghim.png')
        self.image2 = p.image.load('data\\stone.png')
        # Set the size of the stone to be 1/12 of the actual size of the image
        width = random.randint(50,self.image2.get_width() // 8)
        height = random.randint(50,self.image2.get_height() // 8)
        self.size2 = (width,height )
        self.image2 = p.transform.scale(self.image2, self.size2)
        self.rect2 = self.image2.get_rect()
        # Set the position of the stone randomly between x=10 and x=sett.width-400, and y=700 and y=780
        self.rect2.x = random.randint(0,500)
        self.rect2.y = random.randint(700,780)
        # Set the size of the pin to be the actual size of the image
        self.size = (random.randint(500,self.image.get_width() // 1),random.randint(500,self.image.get_height() // 1))
        self.image = p.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        # Set the position of the pin randomly between x=50 and x=sett.width-200, and y=600 and y=700
        self.rect.x = random.randint(0, 500)
        self.rect.y = random.randint(600,700)

    def move(self):
        self.hitbox = p.Rect(self.rect2.x, self.rect2.y, self.rect2.width, self.rect2.height)
        # Move the pin upwards by 8 pixels per frame
        self.rect.y -= 8
        self.rect.x -= 3
        # Move the stone upwards by 3 pixels per frame
        self.rect2.y -= 3

    def draw(self, screen):
        # Draw the pin and the stone on the screen
        screen.blit(self.image2, self.rect2)
        screen.blit(self.image, self.rect)
        



class EnemySpaceship:
    def __init__(self):
        # Load the image of the enemy spaceship from a folder named "data"
        self.image = p.image.load('data\\img1.png')
        # Set the size of the spaceship to be 1/12 of the actual size of the image
        self.size = (self.image.get_width() // 4, self.image.get_height() // 4)
        self.image = p.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        # Set the position of the spaceship randomly between x=50 and x=sett.width-200, and y=600 and y=700
        self.rect.x = random.randint(50, sett.width - 200)
        self.rect.y = random.randint(700,770)
        # Set the speed of the spaceship to be a random number between 3 and 7
        self.speed = random.randint(3, 7)
        # Set the hitbox of the spaceship to be a rectangle with the same position and size as the spaceship
        self.hitbox = p.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)


    def move(self):
        self.rect.y -= self.speed
        self.hitbox = p.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)





class SpaceJet:
    def __init__(self):
        # Define the init method which initializes the game objects
        p.init() # Initialize Pygame library
       # Set the game screen with the given dimensions
        self.screen = p.display.set_mode((0,0),p.FULLSCREEN)
        self.restartScreen = p.display.set_mode((0,0),100,100)
  
        # Set the game caption
        p.display.set_caption("space Jet")

        # Initialize bullets list, bullet image, and bullet size
        self.bullets = []
        self.bullet_img = p.image.load('data\\rec.png').convert_alpha()
        self.bullt_size = (self.bullet_img.get_width() // 24, self.bullet_img.get_height() // 26)
        self.bullet_img  = p.transform.scale(self.bullet_img , self.bullt_size)
        self.bullet_img = p.transform.flip(self.bullet_img, True, True)

        
        # Initialize stones and enemy_spaceships lists
        self.stones = []
        self.enemy_spaceships = []

        # Set the game clock
        self.clock = p.time.Clock()

        # Set the bullet limit and the bullets shot
        self.bullet_limit = 5
        self.bullets_shot = 0
        self.highScore = 0
        self.score = 0
        self.ship_health = 50
        self.last_swap_time = 0
        self.swap_interval = 5000 # milliseconds
        self.scor_scale = 10
        self.scroll_speed = 20.0

    
    def save_highscore(self):
        filename = "highscore.txt"
        # Try to read the current highscore from the file
        try:
            with open(filename, "r") as file:
                self.highScore = int(file.read())
        except FileNotFoundError:
            self.highScore = 0
        
        # If the current score is higher than the highscore, save the new highscore to the file
        if self.score > self.highScore:
            with open(filename, "w") as file:
                file.write(str(self.score))


    def play_music(self):
        p.mixer.music.load("Music\\686555__gregorquendel__symphonic-arpeggio-strings-woodwinds-ii-variation-ii.wav")
        p.mixer.music.play(-1)


    def draw_ship_health(self):
        # Define the size and position of the health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 20
        health_bar_y = 20

        # Calculate the width of the red rectangle based on the current health of the ship
        health_percentage = self.ship_health / 100
        red_rect_width = health_bar_width * health_percentage

        # Draw the health bar background and red rectangle
        health_bar_bg_rect = p.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        health_bar_red_rect = p.Rect(health_bar_x, health_bar_y, red_rect_width, health_bar_height)
        p.draw.rect(self.screen, (255, 255, 255), health_bar_bg_rect)
        p.draw.rect(self.screen, (219, 7, 7), health_bar_red_rect)


    # Define the run_game method which starts the game loop
    def run_game(self):
        # Load the game backgrounds and spaceship images
        background1 = p.image.load("data\\pngegg.png").convert()
        background2 = p.image.load("data\\pngegg.png").convert()
        space_ship = p.image.load("data\\ship.png")
        start_img = p.image.load("data\\back.png").convert()

        # Set the new size of the game background and spaceship
        new_size = (sett.width+600,sett.height+120)
        
        space_size = (space_ship.get_width() // 3, space_ship.get_height() // 3)
        # bomb_size = (bomb.get_width() // 2, bomb.get_height() // 2)
        

        # Scale the game background and spaceship images
        background1 = p.transform.scale(background1, new_size)
        start_img = p.transform.scale(start_img, new_size)  
        background2 = p.transform.scale(background2, new_size)
        space_ship = p.transform.scale(space_ship, space_size)
        # bomb = p.transform.scale(bomb, bomb_size)
        space_ship = p.transform.flip(space_ship, True, True)
        space_ship_rect = space_ship.get_rect()
        # Set the starting position and velocity of the game backgrounds
        background1_y = 0
        space_ship_rect.x = 350
        space_ship_rect.y = 100
        background2_y = -background2.get_rect().height

        # Set the scrolling speed of the backgrounds

        # Set the frequency of stones and enemy_spaceships appearance
        stone_frequency = 10000
        last_stone_time = p.time.get_ticks() - stone_frequency
        enemy_spaceship_frequency = 3000
        last_enemy_spaceship_time = p.time.get_ticks() - enemy_spaceship_frequency
        # Set the running flag to True

        running = False
        manage = pygame_gui.UIManager((sett.width,sett.height))
        manager = pygame_gui.UIManager((sett.width,sett.height))
        
        start_button = pygame_gui.elements.UIButton(
            relative_rect=p.Rect((sett.width - 450, 240), (200, 50)),
            text='Start Game',
            manager=manager
        )
        option_button = pygame_gui.elements.UIButton(
            relative_rect=p.Rect((sett.width - 450, 300), (200, 50)),
            text='Options',
            manager=manager
        )

        quit_button = pygame_gui.elements.UIButton(
            relative_rect=p.Rect((sett.width - 450, 360), (200, 50)),
            text='Quit',
            manager=manager
        )
        restart_button = pygame_gui.elements.UIButton(
                    relative_rect=p.Rect((sett.width - 450, 340), (200, 50)),
                    text='Restart',
                    manager=manage
                )

                # Create quit button
        quit_butto = pygame_gui.elements.UIButton(
                    relative_rect=p.Rect((sett.width - 450, 400), (200, 50)),
                    text='Quit',
                    manager=manage
                )
        

        clock = p.time.Clock()
       
        running_app = True
        p.mixer.music.load("Music\\universe-deep-space-sounds-2751.mp3")
        p.mixer.music.play()
        while running_app:
            
            time_delta = clock.tick(60)
            
 
            for event in p.event.get():
                if event.type == p.QUIT:
                    running_app = False

                manager.process_events(event)

                if event.type == p.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == start_button:
                            running_app = False
                            running = True

                        elif event.ui_element == quit_button:
                            running_app = False
                        elif event.ui_element == option_button:
                            print('Opening options...')

            manager.update(time_delta)

            self.screen.blit(start_img,(0,0))

            manager.draw_ui(self.screen)

            p.display.flip()
            # Start the game loop

        
        # play the background muisc
        p.mixer.music.pause()
        p.mixer.music.load("Music\\686555__gregorquendel__symphonic-arpeggio-strings-woodwinds-ii-variation-ii.wav")
        p.mixer.music.play(-1)

        self.bullet_channel = p.mixer.Channel(1)
        explosion_group = p.sprite.Group()


        while running:
            # Set the game clock speed to 60 frames per second
            self.clock.tick(60)

            # Check if player has lost
            if self.ship_health <= 0:
                # Display new screen with restart and quit buttons
                if self.score > self.highScore:
                    self.highScore = self.score
                self.save_highscore()
                self.screen.blit(start_img,(0,0))
               # Set the width and height of the board
                board_width = 300
                board_height = 200

                # Create the board surface
                board = p.Surface((board_width, board_height))

                # Set the font and text
                font = p.font.SysFont(None, 40)
                text1 = font.render("You lost!", True, (255, 255, 255))
                text2 = font.render(f"Your score: {self.score}", True, (255, 255, 255))
                text3 = font.render(f"Highest score: {self.highScore}", True, (255, 255, 255))

                # Clear the board with a background color
                board.fill((33, 33, 33))

                # Blit the text onto the board
                board.blit(text1, (100, 30))
                board.blit(text2, (70, 70))
                board.blit(text3, (30, 110))

                # Print the board on the screen
                
                self.screen.blit(board, (520, 90))
                                
                # p.display.flip()

                # Wait for player to click a button
                Run = True
                while Run:
                    time_delta = clock.tick(60)
                    for event in p.event.get():
                        if event.type == p.QUIT:
                            running = False
                            break  
                        manage.process_events(event)
                        if event.type == p.USEREVENT: 
                            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:            
                                if event.ui_element == restart_button:
                                        self.__init__()
                                        Run = False
                                elif event.ui_element == quit_butto:
                                    running = False
                                    break
                    manage.update(time_delta)
                    manage.draw_ui(self.screen)
                    p.display.flip()
                        
                    if not running:
                        break

            else:
                
                # Continue playing the game
                manage.update(p.time.get_ticks() / 1000.0)
                explosion_group.draw(self.screen)
                explosion_group.update() 
                for event in p.event.get():
                    if event.type == p.QUIT:
                        running = False
                    elif event.type == p.KEYDOWN:
                        if event.key == p.K_q:
                            running = False
                        elif event.key ==  p.K_SPACE:
                            new_bullet = Bullet(space_ship_rect.x + space_size[0] // 2, space_ship_rect.y, self.bullet_img) 
                            self.bullets.append(new_bullet)
                            bullet_sound = p.mixer.Sound("Music\\boom_c_06-102838.mp3")
                            self.bullet_channel.play(bullet_sound)

                # Check for keyboard input
                
                keys = p.key.get_pressed()
                if keys[p.K_UP]:
                    background1_y -= self.scroll_speed
                    background2_y -= self.scroll_speed
                if keys[p.K_DOWN]:
                    background1_y += self.scroll_speed
                    background2_y += self.scroll_speed
                if keys[p.K_RIGHT] and space_ship_rect.x + space_size[0] < self.screen.get_rect().right:
                    space_ship_rect.x += 10
                if keys[p.K_LEFT] and space_ship_rect.x > 0:
                    space_ship_rect.x -= 10

                if background1_y > sett.height:
                    background1_y = -background1.get_rect().height
                if background1_y < -background1.get_rect().height:
                    background1_y = sett.height

                # Check if the second background image has moved off the screen and reset its position if so
                if background2_y > sett.height:
                    background2_y = -background2.get_rect().height
                if background2_y < -background2.get_rect().height:
                    background2_y = sett.height

                    
                

                # Draw the background images and the player's spaceship onto the screen
                
                current_time = p.time.get_ticks()
                if current_time - self.last_swap_time >= self.swap_interval:
                    # Swap the images
                    background1,background2 = background2,background1
                    self.last_swap_time = current_time

                self.screen.blit(background1, (0, -background1_y))
                self.screen.blit(background1, (0, -background2_y))
                font = p.font.SysFont(None, 25)
                # rectb = p.Rect(220, 200, 200, 50)
                text = font.render(f"Score: {self.score}", True, (200,200,200))
                # self.screen.blit(rectb, (10, 10))
                self.screen.blit(text, (20, 50))
                explosion_group.draw(self.screen)
                explosion_group.update()
                self.draw_ship_health()
                

                # print(space_ship_rect)

                # Move and draw the player's bullets and check if they have hit an enemy spaceship
                for bullet in self.bullets:
                    bullet.update()
                    if bullet.rect.y > sett.width:
                        self.bullets.remove(bullet)
                        self.bullets_shot -= 1
                    else:
                        bullet.draw(self.screen)
                    for enemy in self.enemy_spaceships:
                        if bullet.hitbox.colliderect(enemy.hitbox):
                            # self.screen.blit(bomb,(bullet.rect.x-100,bullet.rect.y))
                            explosio = Explosion(enemy.rect.x,enemy.rect.y)
                            explosion_group.add(explosio)
                            self.score += self.scor_scale
                            self.bullets.remove(bullet)
                            self.enemy_spaceships.remove(enemy)
                            self.bullets_shot -= 1
                            self.scroll_speed +=2
                            self.bullet_limit +=5
                            self.stone.rect.y -=5
                            self.stone.rect2.y -=5
                            stone_frequency -=20

                        

                    for ston in self.stones:
                        if bullet.hitbox.colliderect(ston.hitbox):
                            explosio = Explosion(ston.rect.x+150,ston.rect.x)
                            explosion_group.add(explosio)
                            self.stones.remove(ston)
                            
                            
                        

                for enemy_spaceship in self.enemy_spaceships:
                    if enemy_spaceship.hitbox.colliderect(space_ship_rect):
                        # self.screen.blit(bomb,(space_ship_rect.x-150,space_ship_rect.y))
                        explosio = Explosion(space_ship_rect.x,space_ship_rect.y)
                        explosion_group.add(explosio)
                        self.ship_health -=10
                        self.enemy_spaceships.remove(enemy_spaceship)

                    

                if self.ship_health >= 0:
                    self.screen.blit(space_ship, (space_ship_rect.x, space_ship_rect.y))

                

                for ston in self.stones:
                    if ston.hitbox.colliderect(space_ship_rect):
                        # self.screen.blit(bomb,(space_ship_rect.x-150,space_ship_rect.y))
                        explosio = Explosion(space_ship_rect.x,space_ship_rect.y)
                        explosion_group.add(explosio)
                        self.ship_health -=5
                        self.stones.remove(ston)
                    

                # Add new stones to the game if enough time has passed
                current_time = p.time.get_ticks()
                if current_time - last_stone_time > stone_frequency:
                    self.stone = Stone() 
                    self.stones.append(self.stone)
                    last_stone_time = current_time
                    
                # Add new enemy spaceships to the game if enough time has passed
                current_time = p.time.get_ticks()
                if current_time - last_enemy_spaceship_time > enemy_spaceship_frequency :
                    self.enemy_spaceship = EnemySpaceship()
                
                    self.enemy_spaceships.append(self.enemy_spaceship)
                    last_enemy_spaceship_time = current_time

                for enemy_spaceship in self.enemy_spaceships:
                    enemy_spaceship.draw(self.screen)

                # Move and remove stones that have moved off the screen, and draw remaining stones
                for stone in self.stones:
                    stone.move()
                    if stone.rect.y > sett.height:
                        self.stones.remove(stone)
                    else:
                        stone.draw(self.screen)

                # Move and remove enemy spaceships that have moved off the screen, and draw remaining enemy spaceships
                for enemy_spaceship in self.enemy_spaceships:
                    enemy_spaceship.move()
                    if enemy_spaceship.rect.top > sett.height:
                        self.enemy_spaceships.remove(enemy_spaceship)

            
        


            p.display.flip()

        # Quit Pygame
    p.quit()


# Define the main function that initializes and runs the game
def main():
    SpaceJet().run_game()

# Call the main function if this file is run as the main program
if __name__ == "__main__":
    main() 
