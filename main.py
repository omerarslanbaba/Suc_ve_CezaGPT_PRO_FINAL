
import pygame
from settings import GameSettings
from main_menu import main_menu
from mod_okuma import OkumaModu
from mod_ezber import EzberModu
from mod_test import TestModu

def main():
    pygame.init()
    settings = GameSettings()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Ezber Oyunu - MODLU")
    font = pygame.font.SysFont(settings.FONT_NAME, settings.FONT_SIZE)
    font_bold = pygame.font.SysFont(settings.FONT_NAME, settings.FONT_BOLD_SIZE, bold=True)

    secilen_mod = main_menu(screen, font, font_bold)

    if secilen_mod == 0:
        OkumaModu(screen, font, font_bold).run()
    elif secilen_mod == 1:
        EzberModu(screen, font, font_bold).run()
    elif secilen_mod == 2:
        TestModu(screen, font, font_bold).run()

if __name__ == "__main__":
    main()
