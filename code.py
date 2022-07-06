import pygame,sys,time
from settings import *
from sprites import BG, Ground, Kret, Pipe

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Kreci Drill')
        pygame.display.set_icon(pygame.image.load('graphics/kret0.png').convert_alpha())
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        bg_height = pygame.image.load('graphics/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height
        BG(self.all_sprites,self.scale_factor)
        Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
        self.kret = Kret(self.all_sprites,self.scale_factor / 1.6)

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        self.font = pygame.font.Font('font/pixel.ttf',50)

    def collisions(self):
        if pygame.sprite.spritecollide(self.kret,self.collision_sprites,False,pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def display_score(self):
        self.score = pygame.time.get_ticks() // 1000
        score_surf = self.font.render(str(self.score),False,'white')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH/2,WINDOW_HEIGHT/10))
        self.display_surface.blit(score_surf,score_rect)

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.kret.jump()

                if event.type == self.obstacle_timer:
                    Pipe([self.all_sprites,self.collision_sprites],self.scale_factor)

            self.all_sprites.update(dt)
            self.collisions()
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()