
import pygame
from data_loader import load_replikler
from settings import GameSettings
from ui import character_grid_menu, scene_selection_menu

class TestModu:
    def __init__(self, screen, font, font_bold):
        self.screen = screen
        self.font = font
        self.font_bold = font_bold
        self.settings = GameSettings()
        self.replikler = load_replikler(self.settings.REPLIKLER_DOSYA)
        self.bg_img = pygame.image.load(self.settings.DEFAULT_BACKGROUND_PATH)
        self.clock = pygame.time.Clock()

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

        index = 0
        user_input = ""
        correct_color = (100, 255, 100)
        wrong_color = (255, 80, 80)
        result = None  # None: yazıyor, True: doğru, False: yanlış

        while index < len(filt):
            self.screen.fill((10, 10, 10))
            r = filt[index]
            full = r["full"]
            prompt = self.font_bold.render("Repliği yazın ve Enter'a basın:", True, (255, 255, 0))
            self.screen.blit(prompt, (50, 50))

            pygame.draw.rect(self.screen, (30, 30, 30), (50, 100, 900, 40))
            color = (255, 255, 255) if result is None else (correct_color if result else wrong_color)
            txt = self.font.render(user_input, True, color)
            self.screen.blit(txt, (60, 105))

            if result is not None:
                solution = self.font.render("Doğru Replik: " + full, True, (200, 200, 200))
                self.screen.blit(solution, (50, 180))

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return
                elif ev.type == pygame.KEYDOWN:
                    if result is not None and ev.key == pygame.K_RETURN:
                        user_input = ""
                        result = None
                        index += 1
                        continue
                    if result is not None:
                        continue
                    if ev.key == pygame.K_RETURN:
                        result = user_input.strip().lower() == full.strip().lower()
                    elif ev.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif ev.key == pygame.K_ESCAPE:
                        return
                    else:
                        user_input += ev.unicode

            self.clock.tick(self.settings.FPS)
