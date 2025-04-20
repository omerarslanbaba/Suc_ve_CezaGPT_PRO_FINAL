
import pygame

def main_menu(screen, font, font_bold):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    selected = 0
    options = [
        {"name": "Okuma Modu", "desc": "Sahne seçerek tüm karakterlerin repliklerini görüntüle"},
        {"name": "Ezber Modu", "desc": "Karakter seçerek sadece onun repliklerini takip et"},
        {"name": "Ezber Testi", "desc": "Repliği sen yaz, sistem kontrol etsin"}
    ]

    while True:
        screen.fill((15, 15, 15))
        title = font_bold.render("🎭 OYUN MODU SEÇİMİ", True, (100, 255, 100))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        for i, opt in enumerate(options):
            y = 150 + i * 120
            is_selected = (i == selected)
            color = (80, 80, 80) if is_selected else (40, 40, 40)
            pygame.draw.rect(screen, color, (WIDTH//4, y, WIDTH//2, 100), border_radius=10)

            name_surf = font_bold.render(opt["name"], True, (255, 255, 0) if is_selected else (255, 255, 255))
            desc_surf = font.render(opt["desc"], True, (200, 200, 200))
            screen.blit(name_surf, (WIDTH//4 + 20, y + 15))
            screen.blit(desc_surf, (WIDTH//4 + 20, y + 50))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif ev.key == pygame.K_UP:
                    selected = (selected - 1 + len(options)) % len(options)
                elif ev.key == pygame.K_RETURN:
                    return selected  # 0: okuma, 1: ezber, 2: test

        clock.tick(30)
