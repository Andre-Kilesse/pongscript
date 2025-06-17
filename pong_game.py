import pygame

class PongGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.BALL_SPEED = [4, 4]
        self.PADDLE_SPEED = 6
        self.SPEED_INCREMENT = 0.2
        self.COLOR = (255, 255, 255)
        self.BACKGROUND = (0, 0, 0)
        self.FPS = 60
        self.TECLA_CIMA_P1 = pygame.K_w
        self.TECLA_BAIXO_P1 = pygame.K_s
        self.TECLA_CIMA_P2 = pygame.K_UP
        self.TECLA_BAIXO_P2 = pygame.K_DOWN

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.running = True
        self.score1 = 0
        self.score2 = 0
        self.last_winner = 1

    def init_objects(self):
        self.ball = pygame.Rect(self.WIDTH // 2 - 15, self.HEIGHT // 2 - 15, 30, 30)
        self.paddle1 = pygame.Rect(20, self.HEIGHT // 2 - 60, 10, 120)
        self.paddle2 = pygame.Rect(self.WIDTH - 30, self.HEIGHT // 2 - 60, 10, 120)

    def reset_ball(self):
        self.ball.x = self.WIDTH // 2 - 15
        self.ball.y = self.HEIGHT // 2 - 15
        direction = 1 if self.last_winner == 2 else -1
        self.ball_dx = self.BALL_SPEED[0] * direction
        self.ball_dy = self.BALL_SPEED[1]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[self.TECLA_CIMA_P1] and self.paddle1.top > 0:
            self.paddle1.y -= self.PADDLE_SPEED
        if keys[self.TECLA_BAIXO_P1] and self.paddle1.bottom < self.HEIGHT:
            self.paddle1.y += self.PADDLE_SPEED
        if keys[self.TECLA_CIMA_P2] and self.paddle2.top > 0:
            self.paddle2.y -= self.PADDLE_SPEED
        if keys[self.TECLA_BAIXO_P2] and self.paddle2.bottom < self.HEIGHT:
            self.paddle2.y += self.PADDLE_SPEED

    def update_ball(self):
        self.ball.x += int(self.ball_dx)
        self.ball.y += int(self.ball_dy)

        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.ball_dy *= -1

        if self.ball.colliderect(self.paddle1):
            self.ball.x = self.paddle1.right + 5
            self.ball_dx *= -1
            self.ball_dx += self.SPEED_INCREMENT
            self.ball_dy += self.SPEED_INCREMENT if self.ball_dy > 0 else -self.SPEED_INCREMENT
        elif self.ball.colliderect(self.paddle2):
            self.ball.x = self.paddle2.left - self.ball.width - 5
            self.ball_dx *= -1
            self.ball_dx -= self.SPEED_INCREMENT
            self.ball_dy += self.SPEED_INCREMENT if self.ball_dy > 0 else -self.SPEED_INCREMENT

        if self.ball.left <= 0:
            self.score2 += 1
            self.last_winner = 2
            self.reset_ball()
        elif self.ball.right >= self.WIDTH:
            self.score1 += 1
            self.last_winner = 1
            self.reset_ball()

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        pygame.draw.rect(self.screen, self.COLOR, self.paddle1)
        pygame.draw.rect(self.screen, self.COLOR, self.paddle2)
        pygame.draw.ellipse(self.screen, self.COLOR, self.ball)
        pygame.draw.aaline(self.screen, self.COLOR, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT))
        score_text = self.font.render(f"{self.score1}     {self.score2}", True, self.COLOR)
        self.screen.blit(score_text, (self.WIDTH // 2 - 30, 20))
        pygame.display.flip()

    def run(self):
        self.init_objects()
        self.reset_ball()
        while self.running:
            self.handle_events()
            self.handle_input()
            self.update_ball()
            self.draw()
            self.clock.tick(self.FPS)
        pygame.quit()