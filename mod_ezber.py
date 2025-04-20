
import pygame
from data_loader import load_replikler
from settings import GameSettings
from ui import character_grid_menu, scene_selection_menu, draw_replik_screen

class EzberModu:
    def __init__(self, screen, font, font_bold):
        self.screen = screen
        self.font = font
        self.font_bold = font_bold
        self.settings = GameSettings()
        self.replikler = load_replikler(self.settings.REPLIKLER_DOSYA)
        self.bg_img = pygame.image.load(self.settings.DEFAULT_BACKGROUND_PATH)
        self.clock = pygame.time.Clock()
        self.render_cache = {}

    def filter_by_character_and_scene(self, character, scene):
        p, b, t = scene
        return [
            r for r in self.replikler
            if r.get("perde") == p and r.get("bolum") == b and r.get("tablo") == t and
            character in r.get("speakers", [])
        ]

    def run(self):
        karakter = character_grid_menu(self.screen, self.font, self.font_bold, self.replikler, {}, self.bg_img)
        scene = scene_selection_menu(self.screen, self.font, self.font_bold, self.replikler)
        filt = self.filter_by_character_and_scene(karakter, scene)

        current_index = 0
        letter_index = 0
        last_typing_time = pygame.time.get_ticks()
        typing_speed = 30

        portraits = {}
        for r in filt:
            for spk in r.get("speakers", []):
                if spk not in portraits:
                    path = f"{self.settings.PORTRAIT_FOLDER}/{spk.lower().replace(' ', '')}.png"
                    try:
                        portraits[spk] = pygame.image.load(path)
                    except:
                        portraits[spk] = pygame.image.load(self.settings.DEFAULT_PORTRAIT_PATH)

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RIGHT:
                        current_index = min(current_index + 1, len(filt) - 1)
                        letter_index = 0
                    elif ev.key == pygame.K_LEFT:
                        current_index = max(current_index - 1, 0)
                        letter_index = 0
                    elif ev.key == pygame.K_ESCAPE:
                        return

            now = pygame.time.get_ticks()
            if now - last_typing_time > 1000 // typing_speed:
                if current_index < len(filt):
                    letter_index = min(letter_index + 1, len(filt[current_index]["full"]))
                    last_typing_time = now

            draw_replik_screen(
                self.screen, self.font, self.font_bold, filt,
                portraits, current_index, letter_index, typing_speed,
                background_img=self.bg_img, render_cache=self.render_cache
            )
            pygame.display.flip()
            self.clock.tick(self.settings.FPS)
