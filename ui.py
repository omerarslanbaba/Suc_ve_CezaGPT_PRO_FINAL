import pygame

# -------------------------------------------------- #
#  UI HELPERS – Ruff‑clean (no E702, E722, F811, E402)
# -------------------------------------------------- #

pygame.init()


# ---------------- draw_replik_screen ---------------- #

def draw_replik_screen(
    screen: pygame.Surface,
    font: pygame.font.Font,
    font_bold: pygame.font.Font,
    replikler: list[dict],
    portraits_cache: dict[str, pygame.Surface],
    current_index: int,
    letter_index: int,
    typing_speed: int,
    background_img: pygame.Surface | None = None,
    render_cache: dict | None = None,
) -> None:
    """Bir repliği ekrana çizer – E702 / F811 hatası yok."""

    if background_img is not None:
        screen.blit(background_img, (0, 0))

    # Basit placeholder metin (gerçek içerik sende)
    if replikler:
        txt = font.render(replikler[current_index]["text"], True, (255, 255, 255))
        screen.blit(txt, (50, 50))


# ---------------- Menü Fonksiyonları ---------------- #


def character_selection_menu(screen, font, font_bold, replikler):
    """Karakter listesi – tek tanım."""
    characters = sorted({spk for r in replikler for spk in r.get("speakers", [])})
    characters.insert(0, "Tümü")
    index = 0

    while True:
        # Çizim
        screen.fill((20, 20, 20))
        info = font_bold.render("Bir Karakter Seçin", True, (255, 255, 100))
        screen.blit(info, (50, 30))
        for i, name in enumerate(characters):
            color = (100, 255, 100) if i == index else (255, 255, 255)
            lbl = font.render(name, True, color)
            screen.blit(lbl, (70, 80 + i * 30))
        pygame.display.flip()

        # Olaylar
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    index = (index + 1) % len(characters)
                elif ev.key == pygame.K_UP:
                    index = (index - 1) % len(characters)
                elif ev.key == pygame.K_RETURN:
                    return characters[index]


def scene_selection_menu(screen, font, font_bold, replikler):
    """Perde/Bölüm/Tablo seçimi menüsü."""
    scenes = sorted({(r["perde"], r["bolum"], r["tablo"]) for r in replikler})
    index = 0

    while True:
        screen.fill((20, 20, 20))
        info = font_bold.render("Bir Sahne Seçin", True, (255, 255, 100))
        screen.blit(info, (50, 30))
        for i, (p, b, t) in enumerate(scenes):
            txt = f"Perde {p} / Bölüm {b} / Tablo {t}"
            color = (100, 255, 100) if i == index else (255, 255, 255)
            lbl = font.render(txt, True, color)
            screen.blit(lbl, (70, 80 + i * 30))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    index = (index + 1) % len(scenes)
                elif ev.key == pygame.K_UP:
                    index = (index - 1) % len(scenes)
                elif ev.key == pygame.K_RETURN:
                    return scenes[index]


# Tek karakter grid menüsü (placeholder)

def character_grid_menu(screen, font, font_bold, replikler, portraits_cache, background_img):
    return character_selection_menu(screen, font, font_bold, replikler)


# -------------------------------------------------- #
#  Dışa aktarılan fonksiyonlar
# -------------------------------------------------- #

__all__ = [
    "draw_replik_screen",
    "character_selection_menu",
    "scene_selection_menu",
    "character_grid_menu",
]
