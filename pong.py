import pygame
import random

# Constantes para el ancho y alto de la ventana
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Valores RGB para los colores utilizados en el juego
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Velocidad máxima de la pelota
MAX_SPEED = 0.8
def reset_ball(ball_rect):
    """Reinicia la posición y velocidad de la pelota."""
    ball_rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball_accel_x = random.randint(2, 4) * 0.1
    ball_accel_y = random.randint(2, 4) * 0.1
    if random.randint(1, 2) == 1:
        ball_accel_x *= -1
    if random.randint(1, 2) == 1:
        ball_accel_y *= -1
    return ball_accel_x, ball_accel_y
def main():
    # CONFIGURACIÓN DEL JUEGO
    # Definir los rectángulos de las paletas de los jugadores
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 7, 100)

    # Variables para rastrear el movimiento de las paletas
    paddle_1_move = 0
    paddle_2_move = 0

    # Definir el rectángulo de la pelota
    ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)

    # Determinar la velocidad de la pelota (0.1 es solo para escalar la velocidad hacia abajo)
    ball_accel_x = random.randint(2, 4) * 0.1
    ball_accel_y = random.randint(2, 4) * 0.1

    # Randomizar la dirección de la pelota
    if random.randint(1, 2) == 1:
        ball_accel_x *= -1
    if random.randint(1, 2) == 1:
        ball_accel_y *= -1

    # Crear el objeto reloj para llevar el control del tiempo
    clock = pygame.time.Clock()

    # Variable para verificar si el juego ha comenzado
    started = False

    # Inicializar la biblioteca PyGame
    pygame.init()

    # Crear la ventana del juego
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Establecer el título de la ventana
    pygame.display.set_caption("Pong")

    # Cargar la fuente Consolas
    font = pygame.font.SysFont('Consolas', 30)
    win_font = pygame.font.SysFont('Consolas', 50)

    # Variables para llevar el puntaje
    left_score = 0
    right_score = 0
    winning_score = 3

    while True:
        # Establecer el color de fondo a negro
        screen.fill(COLOR_BLACK)

        # Mostrar el mensaje de inicio si el juego no ha comenzado
        if not started:
            text = font.render('Press Space to Start', True, COLOR_WHITE)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)
            pygame.display.flip()
            clock.tick(60)

            # Manejar los eventos de Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True
            continue

        # Manejar los eventos de Pygame durante el juego
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle_1_move = 0.0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle_2_move = 0.0

            if event.type == pygame.QUIT:
                return

        # Reiniciar la pelota y actualizar el puntaje si la pelota sale de los límites
        if ball_rect.left <= 0:
            right_score += 1
            started = False
            ball_accel_x, ball_accel_y = reset_ball(ball_rect)  # Llamada a reset_ball cuando el jugador derecho anota

        if ball_rect.right >= SCREEN_WIDTH:
            left_score += 1
            started = False
            ball_accel_x, ball_accel_y = reset_ball(ball_rect)  # Llamada a reset_ball cuando el jugador izquierdo anota

        # Mostrar el ganador y reiniciar el juego si alguien gana
        if left_score == winning_score or right_score == winning_score:
            winner = "Player 1" if left_score == winning_score else "Player 2"
            text = win_font.render(f'{winner} Wins!', True, COLOR_WHITE)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        # Hacer rebotar la pelota si toca el borde superior o inferior de la pantalla
        if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
            ball_accel_y *= -1

        # Manejar las colisiones de la pelota con las paletas
        if paddle_1_rect.colliderect(ball_rect) and ball_rect.left <= paddle_1_rect.right:
            ball_accel_x *= -1
            ball_rect.left += 5
            # Aumentar la velocidad de la pelota
            ball_accel_x = min(ball_accel_x * 1.1, MAX_SPEED)
            ball_accel_y = min(ball_accel_y * 1.1, MAX_SPEED)

        if paddle_2_rect.colliderect(ball_rect) and ball_rect.right >= paddle_2_rect.left:
            ball_accel_x *= -1
            ball_rect.left -= 5
            # Aumentar la velocidad de la pelota
            ball_accel_x = min(ball_accel_x * 1.1, MAX_SPEED)
            ball_accel_y = min(ball_accel_y * 1.1, MAX_SPEED)

        # Calcular el tiempo transcurrido entre frames
        delta_time = clock.tick(60)

        # Mover la pelota si el juego ha comenzado
        if started:
            ball_rect.left += ball_accel_x * delta_time
            ball_rect.top += ball_accel_y * delta_time

        # Mover las paletas
        paddle_1_rect.y += paddle_1_move * delta_time
        paddle_2_rect.y += paddle_2_move * delta_time

        #Evitar que se salgan de la pantalla
        if paddle_1_rect.top < 0:
            paddle_1_rect.top = 0
        if paddle_1_rect.bottom > SCREEN_HEIGHT:
            paddle_1_rect.bottom = SCREEN_HEIGHT

        if paddle_2_rect.top < 0:
            paddle_2_rect.top = 0
        if paddle_2_rect.bottom > SCREEN_HEIGHT:
            paddle_2_rect.bottom = SCREEN_HEIGHT

        # Dibujar las paletas y la pelota en la pantalla
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)

        # Dibujar el marcador en la pantalla
        score_text = font.render(f'{left_score} - {right_score}', True, COLOR_WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        # Actualizar la pantalla
        pygame.display.update()


if __name__ == '__main__':
    main()
