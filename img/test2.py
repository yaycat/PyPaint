import pygame
from pygame.constants import *
import pyglet
import time

sound = pyglet.media.load('button.mp3', streaming=False)

class Button:
    def __init__(self, surface, position, size, color, text='', font=None, text_color=(0, 0, 0), icon=None):
        self.surface = surface
        self.position = position
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.position, self.size)
        self.icon = pygame.image.load(icon).convert_alpha() if icon else None
        self.text = text
        self.font = pygame.font.Font(font, 30) if font else pygame.font.SysFont(None, 30)
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)
            self.surface.blit(self.icon, icon_rect)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Paint(object):
    def __init__(self, width, height):
        self.window = pygame.display.set_mode((width, height))
        self.new_image = pygame.Surface((width, height))
        self.new_image.fill((255, 255, 255))

        self.running = False
        self.last_mpos = None
        self.click = False
        self.colordraw = (0, 0, 0)
        self.penwidth = 10

        self.pencolore = [(255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0), (255, 255, 0)]  # white, red, blue, green, black, yellow
        self.color_icons = ["white.png", "rede.png", "blue.png", "green.png", "black.png", "yellow.png"]
        self.color_buttons = [Button(self.window, (50 * (i+1), 20), (40, 40), self.pencolore[i], icon=icon) for i, icon in enumerate(self.color_icons)]

        self.thickness_buttons = [Button(self.window, (50 * (i+1), 80), (40, 40), (200, 200, 200), text=str(i+1)) for i in range(6)]

        self.fill_button = Button(self.window, (50 * 7, 20), (40, 40), (200, 200, 200), icon='t_fil.png')

        self.save_button = Button(self.window, (50 * 8, 20), (40, 40), (200, 200, 200), icon='t_air.png')

        pygame.display.set_caption("Paint")

    def events(self):
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                self.running = False
                break

            for i, button in enumerate(self.color_buttons):
                if e.type == MOUSEBUTTONDOWN and button.is_clicked(pygame.mouse.get_pos()):
                    self.colordraw = self.pencolore[i]
                    sound.play()

            for i, button in enumerate(self.thickness_buttons):
                if e.type == MOUSEBUTTONDOWN and button.is_clicked(pygame.mouse.get_pos()):
                    self.penwidth = i + 1
                    sound.play()

            if e.type == MOUSEBUTTONDOWN:
                self.click = True

            if e.type == MOUSEBUTTONUP:
                self.click = False
                self.last_mpos = None

            if e.type == KEYDOWN and e.key == K_f:
                self.fill_window(self.colordraw)
                sound.play()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_LCTRL:
                pygame.image.save(self.new_image,
                                  time.strftime("%y%m%d_%H%M%S.png"))

    def update(self):
        mx, my = pygame.mouse.get_pos()
        if not self.last_mpos is None and self.click:
            mx0, my0 = self.last_mpos
            pygame.draw.line(self.new_image, self.colordraw, (mx0, my0), (mx, my), self.penwidth)
        self.last_mpos = (mx, my)

    def render(self):
        self.window.blit(self.new_image, (0, 0))
        for button in self.color_buttons:
            button.draw()
        for button in self.thickness_buttons:
            button.draw()
        self.fill_button.draw()
        self.save_button.draw()

    def fill_window(self, color):
        self.new_image.fill(color)

    def mainloop(self):
        self.running = True
        while self.running:
            self.events()
            self.render()
            self.update()
            pygame.display.flip()

def main():
    pygame.init()
    mainclass = Paint(1280, 720)
    mainclass.mainloop()
    pygame.quit()

if __name__ == '__main__':
    main()
