import random 
import pygame 
import asyncio
import sys
# if sys.platform != "emscripten":
#     from database import opprett_bruker, logg_inn, connect_to_db


pygame.init()

HighScore = []

WIDTH = 1200
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0, 255)
SPEED = 10

FPS = 30

timer = 0
score = 0

bg = pygame.image.load("pygameBilder/space3.jpeg")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You know when the")

heart_img = pygame.image.load("pygameBilder/heart.png")
heart_img = pygame.transform.scale(heart_img, (40, 40))

start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
start_ny = pygame.Rect(WIDTH // 2  - 125, HEIGHT // 2 + 150, 250, 100)

opprett_bruker_knapp = pygame.Rect(WIDTH // 2 - 400, HEIGHT // 2 - 200, 200, 100)
opprett_bruker_knapp2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 100)

bruker_navn = pygame.Rect(WIDTH // 2 - 225, HEIGHT // 2 - 300, 200, 100)
bruker_navn2 = pygame.Rect(WIDTH // 2 + 25, HEIGHT // 2 - 300, 200, 100)

logg_inn_knapp = pygame.Rect(WIDTH // 2 + 200, HEIGHT // 2 - 200, 200, 100)
logg_inn_knapp2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 100)

passord = pygame.Rect(WIDTH // 2 - 225, HEIGHT // 2 - 150, 200, 100)
passord2 = pygame.Rect(WIDTH // 2 + 25, HEIGHT // 2 - 150, 200, 100)

navn = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 + 250, 200, 100)
navn2 = pygame.Rect(WIDTH // 2 + 400, HEIGHT // 2 + 250, 200, 100)

etternavn = pygame.Rect(WIDTH // 2 - 600, HEIGHT // 2 + 250, 200, 100)
etternavn2 = pygame.Rect(WIDTH // 2  - 300, HEIGHT // 2 + 250, 200, 100)







    




    

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("pygameBilder/crab.png")
        self.image = pygame.transform.scale(self.image, (59, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.lives = 5

    def update(self):
        key = pygame.key.get_pressed()
        x = ((key[pygame.K_d] - key[pygame.K_a]) * SPEED)
        y = ((key[pygame.K_s] - key[pygame.K_w]) * SPEED)
        self.rect.move_ip(x,y)
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

class Hit_box(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((44,22), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [player.rect.x, player.rect.y]
    
    def update(self):
        hit_box.rect.topleft = (player.rect.x + 11, player.rect.y + 9)

class Astroide(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("pygameBilder/astroide.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 8
        self.direction = pygame.Vector2(player.rect.x - x, player.rect.y - y).normalize()

    def update(self):
        self.rect.move_ip(self.direction * self.speed)  

        if (self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            all_sprites.remove(self)
            if self in astroider:
                astroider.remove(self)
            global score
            score += 1

        if self.rect.colliderect(hit_box.rect):
            all_sprites.remove(self)
            if self in astroider:
                astroider.remove(self)
            player.lives -= 1

class EkstraLiv(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("pygameBilder/Health-potion.png")
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
    
    def update(self):
        if self.rect.colliderect(hit_box.rect):
            all_sprites.remove(self)
            player.lives += 1

class Kaktus(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("pygameBilder/kaktus.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
    
    def update(self):
        if self.rect.colliderect(hit_box.rect):
            all_sprites.remove(self)
            player.lives -= 1
    
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

player = Player(600,400)
hit_box = Hit_box(player.rect.x, player.rect.y)
all_sprites = pygame.sprite.Group()
all_sprites.add(player, hit_box)

astroider = []
clock = pygame.time.Clock()
timer, score = 0,0



      
async def opprett_bruker_side():
    global id 
    email_tekst = ''
    passord_tekst = ''
    navn_tekst = ''
    etternavn_tekst = ''
    skrive_boks = 0
    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if bruker_navn2.collidepoint(mouse_pos):
                    skrive_boks = 1        
                elif passord2.collidepoint(mouse_pos):
                    skrive_boks = 2 
                elif navn2.collidepoint(mouse_pos):
                    skrive_boks = 3        
                elif etternavn2.collidepoint(mouse_pos):
                    skrive_boks = 4 
                elif opprett_bruker_knapp2.collidepoint(mouse_pos):
                    await start_loop()
                else:
                    skrive_boks = 0

            if event.type == pygame.KEYDOWN and skrive_boks == 1:
                if event.key == pygame.K_BACKSPACE: 
                    email_tekst = email_tekst[:-1]
                elif event.key == pygame.K_KP_ENTER:
                    skrive_boks = 0
                else: 
                    email_tekst += event.unicode
            elif event.type == pygame.KEYDOWN and skrive_boks == 2:
                if event.key == pygame.K_BACKSPACE: 
                    passord_tekst = passord_tekst[:-1]
                elif event.key == pygame.K_g:
                    skrive_boks = 0
                else: 
                    passord_tekst += event.unicode
            elif event.type == pygame.KEYDOWN and skrive_boks == 3:
                if event.key == pygame.K_BACKSPACE: 
                    navn_tekst = navn_tekst[:-1]
                elif event.key == pygame.K_g:
                    skrive_boks = 0
                else: 
                    navn_tekst += event.unicode
            elif event.type == pygame.KEYDOWN and skrive_boks == 4:
                if event.key == pygame.K_BACKSPACE: 
                    etternavn_tekst = etternavn_tekst[:-1]
                elif event.key == pygame.K_g:
                    skrive_boks = 0
                else: 
                    etternavn_tekst += event.unicode

        pygame.draw.rect(screen, GREEN, opprett_bruker_knapp2)
        pygame.draw.rect(screen, GREEN, bruker_navn)
        pygame.draw.rect(screen, GREEN, bruker_navn2)
        pygame.draw.rect(screen, GREEN, passord)
        pygame.draw.rect(screen, GREEN, passord2)
        pygame.draw.rect(screen, GREEN, navn)
        pygame.draw.rect(screen, GREEN, navn2)
        pygame.draw.rect(screen, GREEN, etternavn) 
        pygame.draw.rect(screen, GREEN, etternavn2) 

        draw_text("Opprett bruker", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 , HEIGHT // 2 + 150)
        draw_text("Email:", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 - 125, HEIGHT // 2 - 250)
        draw_text("Passord:", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 - 125, HEIGHT // 2 - 100)
        draw_text(email_tekst, pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 + 125, HEIGHT // 2 - 250)
        draw_text(passord_tekst, pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 + 125, HEIGHT // 2 - 100)
        
        draw_text("Navn:", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 + 200, HEIGHT // 2 + 300)
        draw_text("Etternavn:", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 - 500, HEIGHT // 2 + 300)
        draw_text(navn_tekst, pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 + 500, HEIGHT // 2 + 300)
        draw_text(etternavn_tekst, pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 - 200, HEIGHT // 2 + 300)
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0) 

async def logg_inn_side():
    global id 
    email_tekst = ''
    passord_tekst = ''
    skrive_boks = 0
    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if bruker_navn2.collidepoint(mouse_pos):
                    skrive_boks = 1        
                elif passord2.collidepoint(mouse_pos):
                    skrive_boks = 2 
                elif opprett_bruker_knapp2.collidepoint(mouse_pos):
                    await start_loop()
                else:
                    skrive_boks = 0

            if event.type == pygame.KEYDOWN and skrive_boks == 1:
                if event.key == pygame.K_BACKSPACE: 
                    email_tekst = email_tekst[:-1]
                elif event.key == pygame.K_KP_ENTER:
                    skrive_boks = 0
                else: 
                    email_tekst += event.unicode
            elif event.type == pygame.KEYDOWN and skrive_boks == 2:
                if event.key == pygame.K_BACKSPACE: 
                    passord_tekst = passord_tekst[:-1]
                elif event.key == pygame.K_g:
                    skrive_boks = 0
                else: 
                    passord_tekst += event.unicode

        pygame.draw.rect(screen, GREEN, logg_inn_knapp2)
        pygame.draw.rect(screen, GREEN, bruker_navn)
        pygame.draw.rect(screen, GREEN, bruker_navn2)
        pygame.draw.rect(screen, GREEN, passord)
        pygame.draw.rect(screen, GREEN, passord2)

        draw_text("Logg inn", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 , HEIGHT // 2 + 150)
        draw_text("Email:", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 - 125, HEIGHT // 2 - 250)
        draw_text("Passord:", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 - 125, HEIGHT // 2 - 100)
        draw_text(email_tekst, pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 + 125, HEIGHT // 2 - 250)
        draw_text(passord_tekst, pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 + 125, HEIGHT // 2 - 100)
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0) 
async def start_loop():   
            while True:
                screen.fill(BLACK)
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if start_button.collidepoint(mouse_pos):
                            await main() 
                        if opprett_bruker_knapp.collidepoint(mouse_pos): 
                            await opprett_bruker_side()
                        if logg_inn_knapp.collidepoint(mouse_pos):
                            await logg_inn_side()  

                pygame.draw.rect(screen, GREEN, opprett_bruker_knapp)
                pygame.draw.rect(screen, GREEN, logg_inn_knapp)
                pygame.draw.rect(screen, GREEN, start_button)
                draw_text("opprett bruker", pygame.font.Font(None, 35), BLACK, screen, WIDTH // 2 - 300, HEIGHT // 2 - 150)
                draw_text("logg inn", pygame.font.Font(None, 50), BLACK, screen, WIDTH // 2 + 300, HEIGHT // 2 - 150)
                draw_text("START", pygame.font.Font(None, 50), BLACK, screen, WIDTH // 2, HEIGHT // 2)

                pygame.display.flip()
                clock.tick(FPS)
                await asyncio.sleep(0) 
        
async def main():
    global timer, score 
    while True:         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        
        h_vegg = [WIDTH, random.randint(0,HEIGHT)]
        v_vegg = [0, random.randint(0,HEIGHT)]
        tak = [random.randint(0,WIDTH), 0]
        gulv = [random.randint(0,WIDTH), HEIGHT]
        vegger = [h_vegg, v_vegg, tak, gulv]
            
        if len(astroider) < 35:
            vegg_valg = vegger[random.randint(0,3)]
            ny_astroide = Astroide(vegg_valg[0], vegg_valg[1])
            astroider.append(ny_astroide)
            all_sprites.add(ny_astroide)
        for i in range(1):
            timer +=1 
            if timer == 200:
                ekstra_liv = EkstraLiv(random.randint(0, WIDTH), random.randint(0, HEIGHT))
                all_sprites.add(ekstra_liv)
                timer = 0
                kaktus = Kaktus(random.randint(0, WIDTH), random.randint(0, HEIGHT))
                all_sprites.add(kaktus)


            

        screen.blit(bg,(0,0))
        all_sprites.update()
        all_sprites.draw(screen)
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))

        for i in range(player.lives):
            screen.blit(heart_img, (WIDTH - 50 - i * 50, 10))

        if player.lives <= 0:
            draw_text("GAME OVER", pygame.font.Font(None, 100), RED, screen, WIDTH // 2, HEIGHT // 2)
            draw_text(f"Final Score: {score}", pygame.font.Font(None, 50), GREEN, screen, WIDTH // 2, HEIGHT // 2 + 100)
            HighScore.append(score)
            HighScore.sort()
            HighScore.reverse()
            draw_text(f"HighScore: {HighScore[0]}", pygame.font.Font(None, 50), GREEN, screen, WIDTH // 2, 100)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if start_ny.collidepoint(mouse_pos):
                            player.lives = 5
                            score = 0
                            timer = 0
                            astroider.clear()
                            all_sprites.empty()
                            all_sprites.add(player, hit_box)
                            player.rect.topleft = [600, 400]
                            await start_loop()
                await asyncio.sleep(0) 
                        
                pygame.draw.rect(screen, GREEN, start_ny)
                draw_text("SPILL IGJEN", pygame.font.Font(None, 50), BLACK, screen, WIDTH // 2 , HEIGHT // 2 + 200)
                pygame.display.flip()
                clock.tick(FPS)
                

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0) 
        

asyncio.run(start_loop())