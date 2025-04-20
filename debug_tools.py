
import pygame

def draw_debug(screen, fps, index, character):
    font = pygame.font.SysFont("Arial", 18)
    lines = [
        f"[FPS] {fps:.2f}",
        f"[Index] {index}",
        f"[Karakter] {character}"
    ]
    for i, line in enumerate(lines):
        surf = font.render(line, True, (100, 255, 100))
        screen.blit(surf, (10, 10 + i * 20))

def draw_help_panel(screen):
    font = pygame.font.SysFont("Arial", 20)
    WIDTH, HEIGHT = screen.get_size()
    bg_rect = pygame.Rect(WIDTH * 0.05, HEIGHT * 0.05, WIDTH * 0.9, HEIGHT * 0.9)
    pygame.draw.rect(screen, (30, 30, 30), bg_rect)
    pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)

    title = font.render("Tuş Yardımı", True, (255, 255, 0))
    screen.blit(title, (bg_rect.x + 20, bg_rect.y + 20))

    keys = [
        ("➡ Sağ Ok", "Sonraki replik"),
        ("⬅ Sol Ok", "Önceki replik"),
        ("R", "Repliği baştan oynat"),
        ("Enter", "Menüde seçim yap"),
        ("Yukarı / Aşağı", "Menüde gezin"),
        ("H", "Yardımı göster/gizle"),
        ("ESC", "Oyunu kapat")
    ]

    for i, (key, desc) in enumerate(keys):
        k_surf = font.render(f"{key:<10}", True, (255, 255, 255))
        d_surf = font.render(desc, True, (180, 180, 180))
        screen.blit(k_surf, (bg_rect.x + 40, bg_rect.y + 70 + i * 40))
        screen.blit(d_surf, (bg_rect.x + 200, bg_rect.y + 70 + i * 40))
