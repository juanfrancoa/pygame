import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1280, 720
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego con fondo y obstáculos")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (80, 150, 255)
GRIS = (180, 180, 180)
VERDE = (100, 255, 150)

# Fuente
fuente_titulo = pygame.font.Font(None, 100)
fuente_opcion = pygame.font.Font(None, 70)
fuente_peque = pygame.font.Font(None, 40)

# Función para dibujar texto centrado
def dibujar_texto(texto, fuente, color, superficie, x, y):
    texto_obj = fuente.render(texto, True, color)
    texto_rect = texto_obj.get_rect(center=(x, y))
    superficie.blit(texto_obj, texto_rect)
    return texto_rect


# ===================================================
# Clase del Juego
# ===================================================
class Juego:
    def __init__(self):
        self.jugador_img = pygame.image.load("assets/knight.png").convert_alpha()
        self.jugador_img = pygame.transform.scale(self.jugador_img, (70, 70))
        self.jugador = self.jugador_img.get_rect(center=(ANCHO // 2, ALTO - 100))
        self.velocidad = 7
        self.pausado = False
        

        self.fondo_img = pygame.image.load("assets/pattern.webp").convert()
        self.fondo_img = pygame.transform.scale(self.fondo_img, (ANCHO, ALTO))
        self.y_fondo = 0

        # Obstáculos
        self.obstaculo_img = pygame.image.load("assets/stone.webp").convert_alpha()
        self.obstaculo_img = pygame.transform.scale(self.obstaculo_img, (80, 80))
        self.obstaculos = []
        self.tiempo_nuevo_obstaculo = pygame.time.get_ticks()

    def crear_obstaculo(self):
        x = random.randint(50, ANCHO - 100)
        rect = self.obstaculo_img.get_rect(topleft=(x, -100))
        self.obstaculos.append(rect)

    def mover_fondo(self):
        self.y_fondo += 5
        if self.y_fondo >= ALTO:
            self.y_fondo = 0

        ventana.blit(self.fondo_img, (0, self.y_fondo))
        ventana.blit(self.fondo_img, (0, self.y_fondo - ALTO))

    def ejecutar(self):
        clock = pygame.time.Clock()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self.pausado = True
                    menu_principal(self)

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and self.jugador.left > 0:
                self.jugador.x -= self.velocidad
            if teclas[pygame.K_RIGHT] and self.jugador.right < ANCHO:
                self.jugador.x += self.velocidad

            # Crear obstáculos cada cierto tiempo
            if pygame.time.get_ticks() - self.tiempo_nuevo_obstaculo > 600:
                self.crear_obstaculo()
                self.tiempo_nuevo_obstaculo = pygame.time.get_ticks()

            # Mover fondo
            self.mover_fondo()

            # Dibujar jugador
            ventana.blit(self.jugador_img, self.jugador)

            # Mover y dibujar obstáculos
            for obstaculo in self.obstaculos[:]:
                obstaculo.y += 10
                ventana.blit(self.obstaculo_img, obstaculo)
                if obstaculo.top > ALTO:
                    self.obstaculos.remove(obstaculo)


                # Ajuste de hitboxes
                jugador_hitbox = self.jugador.inflate(-20, -20)  #  reduce ancho/alto
                obstaculo_hitbox = obstaculo.inflate(-20, -20)  #  reduce margen de colisión

                # Detección de colisión precisa
                if jugador_hitbox.colliderect(obstaculo_hitbox):
                    dibujar_texto("¡PERDISTE!", fuente_titulo, (255, 50, 50), ventana, ANCHO // 2, ALTO // 2)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    menu_principal()


            dibujar_texto("(ESC pausar juego)", fuente_peque, BLANCO, ventana, ANCHO // 2, 50)

            pygame.display.flip()
            clock.tick(60)


# ===================================================
# Menú Principal
# ===================================================
def menu_principal(juego=None):
    while True:
        ventana.fill(NEGRO)
        mx, my = pygame.mouse.get_pos()

        dibujar_texto("MENÚ PRINCIPAL", fuente_titulo, BLANCO, ventana, ANCHO // 2, 180)
        y_base = 350
        botones = []

        if juego and juego.pausado:
            boton_reanudar = dibujar_texto("REANUDAR", fuente_opcion,
                                           AZUL if y_base < my < y_base + 60 else BLANCO,
                                           ventana, ANCHO // 2, y_base)
            botones.append(("reanudar", boton_reanudar))
            y_base += 80

        boton_jugar = dibujar_texto("NUEVO JUEGO", fuente_opcion,
                                    AZUL if y_base < my < y_base + 60 else BLANCO,
                                    ventana, ANCHO // 2, y_base)
        botones.append(("nuevo", boton_jugar))
        y_base += 80

        boton_salir = dibujar_texto("SALIR", fuente_opcion,
                                    AZUL if y_base < my < y_base + 60 else BLANCO,
                                    ventana, ANCHO // 2, y_base)
        botones.append(("salir", boton_salir))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for accion, boton in botones:
                    if boton.collidepoint((mx, my)):
                        if accion == "nuevo":
                            nuevo_juego = Juego()
                            nuevo_juego.ejecutar()
                        elif accion == "reanudar" and juego:
                            juego.pausado = False
                            juego.ejecutar()
                        elif accion == "salir":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()


# ===================================================
# Iniciar programa
# ===================================================
menu_principal()