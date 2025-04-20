from reji_panel import reji_panel

import pygame
import os
import time
from data_loader import load_replikler, normalize_name
from settings import GameSettings
from ui import character_grid_menu, scene_selection_menu, draw_replik_screen
from debug_tools import draw_debug, draw_help_panel


class Game:
    def __init__(self):
        pygame.init()

        # ---------------- General setup ---------------- #
        self.settings = GameSettings()
        self.screen = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption("Ezber Oyunu - Gelişmiş Sürüm")
        self.clock = pygame.time.Clock()

        # Fontlar
        self.font = pygame.font.SysFont(self.settings.FONT_NAME, self.settings.FONT_SIZE)
        self.font_bold = pygame.font.SysFont(
            self.settings.FONT_NAME, self.settings.FONT_BOLD_SIZE, bold=True
        )

        # ---------------- Veri ---------------- #
        self.replikler = load_replikler(self.settings.REPLIKLER_DOSYA)
        self.portraits_cache: dict[str, pygame.Surface] = {}
        self.load_portraits_for_menu()

        # Arka plan dosyasını yükle – hem eski (FOLDER + NAME) hem yeni (DEFAULT_BACKGROUND_PATH) yapıları destekler
        try:
            self.bg_img = pygame.image.load(
                os.path.join(self.settings.BACKGROUND_FOLDER, self.settings.DEFAULT_BG)
            )
        except AttributeError:
            self.bg_img = pygame.image.load(self.settings.DEFAULT_BACKGROUND_PATH)

        # ---------------- Menü Seçimleri ---------------- #
        self.character = character_grid_menu(
            self.screen,
            self.font,
            self.font_bold,
            self.replikler,
            self.portraits_cache,
            self.bg_img,
        )
        self.scene = scene_selection_menu(
            self.screen, self.font, self.font_bold, self.replikler
        )

        # Seçime göre filtrele ► sadece ilgili replikler
        self.replikler = self.filter_replikler()
        self.load_portraits_for_filtered()

        # ---------------- Oyun Durumu ---------------- #
        self.current_index = 0
        self.letter_index = 0
        self.typing_speed = 30  # karakter/saniye
        self.last_typing_time = time.time()
        self.render_cache: dict[tuple, pygame.Surface] = {}

        # UI & Debug bayrakları
        self.debug = True
        self.show_help = False
        self.back_button_rect: pygame.Rect | None = None

    # -------------------------------------------------- #
    # Yardımcı Fonksiyonlar
    # -------------------------------------------------- #

    def load_portraits_for_menu(self):
        for r in self.replikler:
            for spk in r.get("speakers", []):
                if spk not in self.portraits_cache:
                    norm = normalize_name(spk)
                    fn = f"{norm}.png"
                    path = os.path.join(self.settings.PORTRAIT_FOLDER, fn)
                    try:
                        img = pygame.image.load(path)
                    except FileNotFoundError:
                        img = pygame.image.load(
                            os.path.join(
                                self.settings.PORTRAIT_FOLDER, self.settings.DEFAULT_PORTRAIT
                            )
                        )
                    self.portraits_cache[spk] = pygame.transform.smoothscale(
                        img,
                        (int(self.settings.WIDTH * 0.2), int(self.settings.HEIGHT * 0.35)),
                    )

    def load_portraits_for_filtered(self):
        # Yalnızca filtrelenmiş karakter portrelerini ekle
        for r in self.replikler:
            for spk in r.get("speakers", []):
                if spk not in self.portraits_cache:
                    norm = normalize_name(spk)
                    fn = f"{norm}.png"
                    path = os.path.join(self.settings.PORTRAIT_FOLDER, fn)
                    try:
                        img = pygame.image.load(path)
                    except FileNotFoundError:
                        img = pygame.image.load(
                            os.path.join(
                                self.settings.PORTRAIT_FOLDER, self.settings.DEFAULT_PORTRAIT
                            )
                        )
                    self.portraits_cache[spk] = pygame.transform.smoothscale(
                        img,
                        (int(self.settings.WIDTH * 0.2), int(self.settings.HEIGHT * 0.35)),
                    )

    def filter_replikler(self):
        """Kullanıcının seçtiği perde/bölüm/tablo ve karaktere göre replikleri daralt."""
        p, b, t = self.scene
        filtered = [r for r in self.replikler if r.get("perde") == p and r.get("bolum") == b and r.get("tablo") == t]
        if self.character != "Tümü":
            filtered = [r for r in filtered if self.character in r.get("speakers", [])]
        return filtered

    def reset_to_menu(self):
        """Menüye dönerken tüm sayaçları sıfırla."""
        self.character = character_grid_menu(
            self.screen,
            self.font,
            self.font_bold,
            self.replikler,
            self.portraits_cache,
            self.bg_img,
        )
        self.scene = scene_selection_menu(
            self.screen, self.font, self.font_bold, self.replikler
        )
        self.replikler = self.filter_replikler()
        self.load_portraits_for_filtered()
        self.current_index = 0
        self.letter_index = 0
        self.last_typing_time = time.time()

    # -------------------------------------------------- #
    # Çizim yardımcıları
    # -------------------------------------------------- #

    def draw_back_button(self):
        font = pygame.font.SysFont("Arial", 20)
        txt = font.render("← Geri Dön", True, (255, 255, 255))
        rect = txt.get_rect(topleft=(20, 20))
        pygame.draw.rect(self.screen, (60, 60, 60), rect.inflate(20, 10))
        self.screen.blit(txt, rect)
        return rect.inflate(20, 10)

    # -------------------------------------------------- #
    # Olay Yönetimi
    # -------------------------------------------------- #

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif ev.type == pygame.KEYDOWN:
                # ------ Replik gezinme ------ #
                if ev.key == pygame.K_RIGHT:
                    self.current_index = min(self.current_index + 1, len(self.replikler) - 1)
                    self.letter_index = 0

                elif ev.key == pygame.K_LEFT:
                    self.current_index = max(self.current_index - 1, 0)
                    self.letter_index = 0

                # ------ Reji Paneli ------ #
                elif ev.key == pygame.K_r:
                    reji_panel(self.screen, self.font, self.font_bold)

                # ------ Yardım Paneli ------ #
                elif ev.key == pygame.K_h:
                    self.show_help = not self.show_help

            # ------ Geri Dön Butonu ------ #
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(ev.pos):
                    self.reset_to_menu()

    # -------------------------------------------------- #
    # Ana Çizim Döngüsü
    # -------------------------------------------------- #

    def update_screen(self):
        draw_replik_screen(
            self.screen,
            self.font,
            self.font_bold,
            self.replikler,
            self.portraits_cache,
            self.current_index,
            self.letter_index,
            self.typing_speed,
            background_img=self.bg_img,
            render_cache=self.render_cache,
        )

        if self.debug:
            draw_debug(
                self.screen, self.clock.get_fps(), self.current_index, self.character
            )

        if self.show_help:
            draw_help_panel(self.screen)

        self.back_button_rect = self.draw_back_button()
        pygame.display.flip()

    # -------------------------------------------------- #
    # Oyun Döngüsü
    # -------------------------------------------------- #

    def run(self):
        while True:
            self.handle_events()
            self.update_screen()
            self.clock.tick(self.settings.FPS)
