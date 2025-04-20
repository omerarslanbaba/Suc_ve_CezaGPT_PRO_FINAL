import pygame
import os


class GameSettings:
    """Merkezi ayarlar sınıfı – DEFAULT_PORTRAIT_PATH eklendi."""

    def __init__(self):
        pygame.init()

        # ----- Arka Plan ----- #
        self.BACKGROUND_FOLDER = os.path.join("assets", "backgrounds")
        self.DEFAULT_BG        = "default.jpg"
        self.DEFAULT_BACKGROUND_PATH = os.path.join(self.BACKGROUND_FOLDER, self.DEFAULT_BG)

        # Pencere boyutunu arka plan görselinden al
        try:
            img = pygame.image.load(self.DEFAULT_BACKGROUND_PATH)
            self.WIDTH, self.HEIGHT = img.get_width(), img.get_height()
            print(f"[INFO] Arka plan çözünürlüğü: {self.WIDTH}x{self.HEIGHT}")
        except Exception as e:
            print("[HATA] Arka plan yüklenemedi:", e)
            self.WIDTH, self.HEIGHT = 1000, 600
            print("[UYARI] Varsayılan çözünürlük uygulanıyor: 1000x600")

        # ----- Genel ----- #
        self.FPS = 60
        self.FONT_NAME = "Arial"
        self.FONT_SIZE = max(int(self.HEIGHT * 0.04), 12)
        self.FONT_BOLD_SIZE = max(int(self.HEIGHT * 0.046), 14)

        # ----- Veri ve Varlık Klasörleri ----- #
        self.REPLIKLER_DOSYA = "ezber_replikleri_temizlenmis.json"

        self.PORTRAIT_FOLDER = os.path.join("assets", "portraits")
        self.DEFAULT_PORTRAIT = "default.png"
        self.DEFAULT_PORTRAIT_PATH = os.path.join(self.PORTRAIT_FOLDER, self.DEFAULT_PORTRAIT)

        # ----- Renk Paleti ----- #
        self.BLACK  = (20, 20, 20)
        self.WHITE  = (255, 255, 255)
        self.YELLOW = (255, 255, 100)
        self.GRAY   = (150, 150, 150)
        self.GREEN  = (100, 255, 100)
