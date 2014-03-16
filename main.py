import pygame
import sys
import random

from game_objects.paddle_sprites import paddle_sprite
from game_objects.ball_sprites import ball_sprite
from pygame.locals import *

ball = ball_sprite
paddle = paddle_sprite

class main_code:
    
    def pygame_setup(self):
        #initiate the pygame module and it's font module
        pygame.init()
        pygame.font.init()
        #set the display size and title
        self.size = self.width, self.height = 800, 450
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")
        self.top_b, self.bottom_b, self.left_b, self.right_b = 20, self.height - 20, 20, self.width - 20
        #set the clock which will be used to regulate the refresh rate
        self.clock = pygame.time.Clock()
        #set font defaults
        self.font = pygame.font.Font(None, 25)
        #set game objects
        self.game_settings()
        #start the game
        self.main()
        
    def game_settings(self):
        #should splash screen be shown
        self.display_splash = True
        #blit and draw lists for display
        self.draw_items = []
        self.blit_items = []
        
    def game_object_setup(self):
        #scores
        self.player_one_score = 0
        self.player_two_score = 0
        
        #paddles
        self.paddle_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.player_one = paddle((20, 100), (255, 255, 255), 1)
        self.player_one.rect.x = 20
        self.player_one.rect.y = 20
        self.paddle_group.add(self.player_one)
        self.player_group.add(self.player_one)
        
        self.player_two = paddle((20, 100), (255, 255, 255), 1)
        self.ai_group = pygame.sprite.Group()
        self.player_two.rect.x = self.width - self.player_two.rect.width - 20
        self.player_two.rect.y = 20
        self.paddle_group.add(self.player_two)
        self.ai_group.add(self.player_two)
        self.draw_items.append(self.paddle_group)
        
        #balls
        self.ball_group = pygame.sprite.Group()
        self.ball_one = ball((10, 10), (self.width / 2, self.height / 2), (255, 0, 0), 1)
        self.ball_group.add(self.ball_one)
        self.draw_items.append(self.ball_group)
        
    def create_text(self, text, position):
        #get the dimensions of the text, create a surface of that size and blit the text to it
        font_ob = self.font.render(str(text), 1, (255, 0, 0))
        font_ob_size = font_ob.get_rect().width, font_ob.get_rect().height
        font_sur = pygame.Surface(font_ob_size)
        font_sur.blit(font_ob, (0, 0))
        return (font_sur, position)
        
    def splash_screen(self):
        #screen to be displayed when game is started
        start_text = self.create_text("Press P to start", (self.width / 2, self.height / 2))
        self.blit_items.append(start_text)
        if self.key[K_p]:
            self.display_splash = False
            self.empty_blit_list()

    def empty_blit_list(self):
        self.blit_items = []
        
    def empty_draw_list(self):
        self.draw_items = []
        
    def main(self):
        self.game_object_setup()
        while 1:
            player_score = "P1 Score: {}".format(str(self.player_one_score))
            ai_score = "P2 Score: {}".format(str(self.player_two_score))
            p1_blit = self.create_text(str(player_score), (100, 0))
            p2_blit = self.create_text(str(ai_score), (self.right_b - 200, 0))
            self.blit_items.append(p1_blit)
            self.blit_items.append(p2_blit)
            if self.player_one_score > 10 or self.player_two_score > 10:
                self.end_game()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            #monitor keyboard input
            self.key = pygame.key.get_pressed()
            
            #should the splash screen be displayed?
            if self.display_splash == True:
                self.splash_screen()
            else:
                #move ball
                self.ball_movement()
                #check ball position
                self.ball_position()
                #take action on key events
                if any(self.key) > 0 and self.key[K_p] == 0: # go if key pressed != p (splash screen clash)
                    self.paddle_movement(self.player_one, self.key)
                self.ai_paddle(self.player_two)
                
            self.screen_blit(self.draw_items, self.blit_items)
    
    def ball_movement(self):
        #Can this be condensed?
        for ball in self.ball_group:
            if ball.x_direction == "right":
                ball.rect.x += ball.x_speed
            if ball.x_direction == "left":
                ball.rect.x -= ball.x_speed
            if ball.y_direction == "up" and ball.rect.y > self.top_b:
                ball.rect.y -= ball.y_speed
            elif ball.y_direction == "up" and ball.rect.y <= self.top_b:
                ball.y_direction = "down"
            if ball.y_direction == "down" and ball.rect.y < self.bottom_b - ball.rect.height:
                ball.rect.y += ball.y_speed
            elif ball.y_direction == "down" and ball.rect.y >= self.bottom_b - ball.rect.height:
                ball.y_direction = "up"
            
            player_collision = pygame.sprite.spritecollide(ball, self.paddle_group, False)
            for collision in player_collision:
                ball.x_speed += 1
                top_quarter = range(collision.rect.y, collision.rect.y + 25)
                middle = range(collision.rect.y + 25, collision.rect.y + 75)
                bottom_quarter = range(collision.rect.y + 75, collision.rect.y + collision.rect.height)
                if ball.rect.y in top_quarter:
                    ball.y_direction = "up"
                    if ball.x_direction == "right":
                        ball.x_direction = "left"
                    elif ball.x_direction == "left":
                        ball.x_direction = "right"
                        if ball.x_speed < 9:
                            ball.x_speed = ball.y_speed + 1
                elif ball.rect.y in middle:
                    if ball.x_direction == "right":
                        ball.x_direction = "left"
                    elif ball.x_direction == "left":
                        ball.x_direction = "right"
                    speeds = max(ball.x_speed, ball.y_speed)
                    if ball.x_speed < 9:
                        ball.x_speed, ball.y_speed = speeds, speeds
                elif ball.rect.y in bottom_quarter:
                    ball.y_direction = "down"
                    if ball.x_direction == "right":
                        ball.x_direction = "left"
                    elif ball.x_direction == "left":
                        ball.x_direction = "right"
                    if ball.x_speed < 9:
                        ball.x_speed = ball.y_speed + 1
                break
            
    def ball_position(self):
        for ball in self.ball_group:
            # reset ball position and set a random x and y direction
            if ball.rect.x > self.width or ball.rect.x < self.left_b:
                # alter score depending on which side it went out on
                if ball.rect.x > self.right_b:
                    self.player_one_score += 1
                if ball.rect.x < self.left_b:
                    self.player_two_score += 1
                    
                ball.x_speed, ball.y_speed = 5, 5
                ball.rect.x, ball.rect.y = self.width / 2, random.randint(0, self.height)
                ball.x_direction = random.choice(["left", "right"])
                ball.y_direction = random.choice(["up", "down"])
        
    def paddle_movement(self, player, key):
        if key[K_UP] and player.rect.y > self.top_b:
            player.rect.y -= player.speed
        if key[K_DOWN] and player.rect.y < self.bottom_b - player.rect.height:
            player.rect.y += player.speed
            
    def ai_paddle(self, player):
        for each in self.ball_group:
            x_difference = player.rect.x - each.rect.x
            half_width = self.right_b
            choices = [0, 1, 1, 1]
            choice = random.choice(choices)
            
            if choice == 1:
                if each.rect.y > player.rect.y and x_difference < half_width:
                    if player.rect.y < self.bottom_b - player.rect.height:
                        player.rect.y += player.speed
                elif each.rect.y < player.rect.y and x_difference < half_width:
                    if player.rect.y > self.top_b:
                        player.rect.y -= player.speed   
                else:
                    pass
            
    def end_game(self):
        pygame.quit()
        sys.exit()
        
    def screen_blit(self, draw_items = None, blit_items = None):
        self.display.fill((0, 0, 0))
        
        if draw_items is not None:
            for draw_object in draw_items:
                draw_object.draw(self.display)
                
        if blit_items is not None:
            for blit_object in blit_items:
                self.display.blit(blit_object[0], (blit_object[1][0], blit_object[1][1]))
        self.blit_items = []
        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    main_code().pygame_setup()