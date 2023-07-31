import pygame
import button


pygame.init()
# Dimensiones de la pantalla
ANCHO = 1000
ALTO = 800

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Main Menu")

# Fuente de la letra
font = pygame.font.SysFont("arialblack",40)

# Colores del texto
text_col = (255,255,255)

# cargar imagenes del menu
humano_img = pygame.image.load("menu_items/humano.png").convert_alpha()
pulpo_img = pygame.image.load("menu_items/pulpo.png").convert_alpha()
mono_img = pygame.image.load("menu_items/mono.png").convert_alpha()
PG_img = pygame.image.load("menu_items/pie_grande.png").convert_alpha()


# Crear objetos botón
humano_bt = button.Button(-100, 300, humano_img, 1)
pulpo_bt = button.Button(200, 300, pulpo_img, .5)
mono_bt = button.Button(450, 300, mono_img, 1)
PG_bt = button.Button(700, 300, PG_img, .5)






def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


# Game loop
menu = True
run = True
# Banderas
humano = False
pulpo = False
mono = False
PG = False
# ciclo principal
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if menu:
        screen.fill((52, 78, 91))
        draw_text("Choose your character", font, text_col, 225, 20)
        draw_text("Human",font, text_col, 30, 250)
        draw_text("Octopus", font, text_col, 240, 250)
        draw_text("Monkey", font, text_col, 500, 250)
        draw_text("Sasquatch", font, text_col, 730, 250)
        if humano_bt.draw(screen):
            humano = True
            run = False
        if pulpo_bt.draw(screen):
            pulpo = True
            run = False
        if mono_bt.draw(screen):
            mono = True
            run = False
        if PG_bt.draw(screen):
            PG = True
            run = False



    # event handler

    pygame.display.update()