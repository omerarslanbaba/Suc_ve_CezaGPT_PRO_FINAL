
import pygame
from data_loader import normalize_name

def character_selection_menu(screen, font, font_bold, replikler, portraits, background_img=None):
    seen = {}
    for r in replikler:
        for k in r.get("speakers", []):
            norm = normalize_name(k)
            if norm not in seen:
                seen[norm] = k
    characters = list(seen.values()) + ["Tümü"]
    characters.sort()
    index = 0
    WIDTH, HEIGHT = screen.get_size()

    while True:
        if background_img:
            screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 20))

        title = font_bold.render("Bir karakter seçin (Enter ile):", True, (100, 255, 100))
        screen.blit(title, (WIDTH * 0.05, HEIGHT * 0.05))

        for i, name in enumerate(characters):
            color = (255, 255, 100) if i == index else (255, 255, 255)
            surf = font.render(name, True, color)
            screen.blit(surf, (WIDTH * 0.08, HEIGHT * 0.15 + i * int(HEIGHT * 0.045)))

        # Portre göster
        char = characters[index]
        if char in portraits:
            port_img = pygame.transform.smoothscale(portraits[char], (int(WIDTH * 0.2), int(HEIGHT * 0.35)))
            screen.blit(port_img, (WIDTH * 0.75, HEIGHT * 0.15))

        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    index = (index + 1) % len(characters)
                elif ev.key == pygame.K_UP:
                    index = (index - 1) % len(characters)
                elif ev.key == pygame.K_RETURN:
                    return characters[index]

def scene_selection_menu(screen, font, font_bold, replikler):
    scenes = sorted({(r.get("perde", "?"), r.get("bolum", "?"), r.get("tablo", "?")) for r in replikler})
    index = 0
    WIDTH, HEIGHT = screen.get_size()

    while True:
        screen.fill((20, 20, 20))
        title = font_bold.render("Sahne Seçimi - Perde | Bölüm | Tablo", True, (100, 255, 100))
        screen.blit(title, (WIDTH * 0.05, HEIGHT * 0.05))
        for i, (p, b, t) in enumerate(scenes):
            label = f"{p} / {b} / {t}"
            color = (255, 255, 100) if i == index else (255, 255, 255)
            surf = font.render(label, True, color)
            screen.blit(surf, (WIDTH * 0.08, HEIGHT * 0.15 + i * int(HEIGHT * 0.045)))
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    index = (index + 1) % len(scenes)
                elif ev.key == pygame.K_UP:
                    index = (index - 1) % len(scenes)
                elif ev.key == pygame.K_RETURN:
                    return scenes[index]

def draw_replik_screen(screen, font, font_bold, replikler, portraits, current_index, letter_index, typing_speed, background_img=None, render_cache=None):
    import time
    BLACK = (20, 20, 20)
    GRAY = (150, 150, 150)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 100)
    WIDTH, HEIGHT = screen.get_size()

    if background_img:
        screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
    else:
        screen.fill(BLACK)

    def cached_render(text, font_obj, color):
        key = (text, font_obj.get_height(), color)
        if key not in render_cache:
            render_cache[key] = font_obj.render(text, True, color)
        return render_cache[key]

    for i in range(2, 0, -1):
        idx = current_index - i
        if 0 <= idx < len(replikler):
            r = replikler[idx]
            speaker = ", ".join(r.get("speakers", []))
            full = r.get("full", "")
            sp_surf = cached_render(speaker.upper(), font_bold, GRAY)
            txt_surf = cached_render(full, font, GRAY)
            screen.blit(sp_surf, (WIDTH * 0.06, HEIGHT * (0.05 + i * 0.2)))
            screen.blit(txt_surf, (WIDTH * 0.06, HEIGHT * (0.08 + i * 0.2)))

    if 0 <= current_index < len(replikler):
        r = replikler[current_index]
        speaker = ", ".join(r.get("speakers", []))
        full = r.get("full", "")
        shown = full[:letter_index]
        sp_surf = cached_render(speaker.upper(), font_bold, YELLOW)
        txt_surf = font.render(shown, True, WHITE)  # dinamik yazı efekti cache'lenmiyor
        screen.blit(sp_surf, (WIDTH * 0.06, HEIGHT * 0.65))
        screen.blit(txt_surf, (WIDTH * 0.06, HEIGHT * 0.70))

        if r.get("speakers"):
            name = r["speakers"][0]
            portrait = portraits.get(name)
            if portrait:
                screen.blit(portrait, (WIDTH * 0.75, HEIGHT * 0.55))

import pygame
from data_loader import normalize_name

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def draw_replik_screen(screen, font, font_bold, replikler, portraits, current_index, letter_index, typing_speed, background_img=None, render_cache=None):
    import time
    BLACK = (20, 20, 20)
    GRAY = (150, 150, 150)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 100)
    WIDTH, HEIGHT = screen.get_size()

    if background_img:
        screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
    else:
        screen.fill(BLACK)

    def cached_render(text, font_obj, color):
        key = (text, font_obj.get_height(), color)
        if render_cache is not None and key not in render_cache:
            render_cache[key] = font_obj.render(text, True, color)
        return render_cache[key] if render_cache else font_obj.render(text, True, color)

    for i in range(2, 0, -1):
        idx = current_index - i
        if 0 <= idx < len(replikler):
            r = replikler[idx]
            speaker = ", ".join(r.get("speakers", []))
            full = r.get("full", "")
            sp_surf = cached_render(speaker.upper(), font_bold, GRAY)
            screen.blit(sp_surf, (WIDTH * 0.06, HEIGHT * (0.05 + i * 0.2)))
            lines = wrap_text(full, font, WIDTH * 0.6)
            for j, line in enumerate(lines):
                txt_surf = cached_render(line, font, GRAY)
                screen.blit(txt_surf, (WIDTH * 0.06, HEIGHT * (0.08 + i * 0.2) + j * (font.get_height() + 5)))

    if 0 <= current_index < len(replikler):
        r = replikler[current_index]
        speaker = ", ".join(r.get("speakers", []))
        full = r.get("full", "")
        shown = full[:letter_index]
        sp_surf = cached_render(speaker.upper(), font_bold, YELLOW)
        screen.blit(sp_surf, (WIDTH * 0.06, HEIGHT * 0.65))

        lines = wrap_text(shown, font, WIDTH * 0.6)
        for j, line in enumerate(lines):
            txt_surf = font.render(line, True, WHITE)
            screen.blit(txt_surf, (WIDTH * 0.06, HEIGHT * 0.70 + j * (font.get_height() + 5)))

        if r.get("speakers"):
            name = r["speakers"][0]
            portrait = portraits.get(name)
            if portrait:
                screen.blit(portrait, (WIDTH * 0.75, HEIGHT * 0.55))


import pygame
from data_loader import normalize_name

def character_selection_menu(screen, font, font_bold, replikler, portraits, background_img=None):
    seen = {}
    for r in replikler:
        for k in r.get("speakers", []):
            norm = normalize_name(k)
            if norm not in seen:
                seen[norm] = k
    characters = list(seen.values()) + ["Tümü"]
    characters.sort()
    index = 0
    scroll_offset = 0
    max_display = 15
    WIDTH, HEIGHT = screen.get_size()

    while True:
        if background_img:
            screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 20))

        title = font_bold.render("Bir karakter seçin (Enter ile):", True, (100, 255, 100))
        screen.blit(title, (WIDTH * 0.05, HEIGHT * 0.05))

        view = characters[scroll_offset:scroll_offset+max_display]
        for i, name in enumerate(view):
            real_index = i + scroll_offset
            bg_color = (60, 60, 60) if real_index == index else None
            if bg_color:
                pygame.draw.rect(screen, bg_color, pygame.Rect(WIDTH * 0.075, HEIGHT * 0.15 + i * int(HEIGHT * 0.045), WIDTH * 0.5, font.get_height()))

            color = (255, 255, 100) if real_index == index else (255, 255, 255)
            surf = font.render(name, True, color)
            screen.blit(surf, (WIDTH * 0.08, HEIGHT * 0.15 + i * int(HEIGHT * 0.045)))

        char = characters[index]
        if char in portraits:
            port_img = pygame.transform.smoothscale(portraits[char], (int(WIDTH * 0.2), int(HEIGHT * 0.35)))
            screen.blit(port_img, (WIDTH * 0.75, HEIGHT * 0.15))

        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    index = (index + 1) % len(characters)
                    if index >= scroll_offset + max_display:
                        scroll_offset += 1
                elif ev.key == pygame.K_UP:
                    index = (index - 1 + len(characters)) % len(characters)
                    if index < scroll_offset:
                        scroll_offset -= 1
                elif ev.key == pygame.K_RETURN:
                    return characters[index]

def scene_selection_menu(screen, font, font_bold, replikler):
    scenes = sorted({(r.get("perde", "?"), r.get("bolum", "?"), r.get("tablo", "?")) for r in replikler})
    index = 0
    scroll_offset = 0
    max_display = 15
    WIDTH, HEIGHT = screen.get_size()

    while True:
        screen.fill((20, 20, 20))
        title = font_bold.render("Sahne Seçimi - Perde | Bölüm | Tablo", True, (100, 255, 100))
        screen.blit(title, (WIDTH * 0.05, HEIGHT * 0.05))

        view = scenes[scroll_offset:scroll_offset+max_display]
        for i, (p, b, t) in enumerate(view):
            real_index = i + scroll_offset
            label = f"{p} / {b} / {t}"
            color = (255, 255, 100) if real_index == index else (255, 255, 255)
            surf = font.render(label, True, color)
            screen.blit(surf, (WIDTH * 0.08, HEIGHT * 0.15 + i * int(HEIGHT * 0.045)))

        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    index = (index + 1) % len(scenes)
                    if index >= scroll_offset + max_display:
                        scroll_offset += 1
                elif ev.key == pygame.K_UP:
                    index = (index - 1 + len(scenes)) % len(scenes)
                    if index < scroll_offset:
                        scroll_offset -= 1
                elif ev.key == pygame.K_RETURN:
                    return scenes[index]


import pygame
from collections import Counter
from data_loader import normalize_name

def character_grid_menu(screen, font, font_bold, replikler, portraits, background_img=None):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Karakter replik sayısı
    counter = Counter()
    for r in replikler:
        for k in r.get("speakers", []):
            counter[k] += 1
    characters = sorted(counter.keys())
    items = [(k, counter[k]) for k in characters]

    cols, rows = 3, 3
    cell_w = WIDTH // cols
    cell_h = HEIGHT // rows
    index = 0

    while True:
        if background_img:
            screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 20))

        for i, (name, count) in enumerate(items[:cols*rows]):
            col = i % cols
            row = i // cols
            x, y = col * cell_w, row * cell_h

            rect = pygame.Rect(x + 10, y + 10, cell_w - 20, cell_h - 20)
            bg = (60, 60, 60) if i == index else (30, 30, 30)
            pygame.draw.rect(screen, bg, rect, border_radius=12)

            if name in portraits:
                img = pygame.transform.smoothscale(portraits[name], (int(cell_w*0.6), int(cell_h*0.4)))
                screen.blit(img, (x + cell_w*0.2, y + 20))

            txt = font_bold.render(name, True, (255, 255, 0) if i == index else (255, 255, 255))
            screen.blit(txt, (x + 20, y + cell_h*0.65))

            c_txt = font.render(f"{count} replik", True, (200, 200, 200))
            screen.blit(c_txt, (x + 20, y + cell_h*0.75))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    index = (index + 1) % len(items)
                elif ev.key == pygame.K_LEFT:
                    index = (index - 1 + len(items)) % len(items)
                elif ev.key == pygame.K_DOWN:
                    index = (index + cols) % len(items)
                elif ev.key == pygame.K_UP:
                    index = (index - cols + len(items)) % len(items)
                elif ev.key == pygame.K_RETURN:
                    return items[index][0]
        clock.tick(30)


import pygame
from collections import Counter
from data_loader import normalize_name

def character_grid_menu(screen, font, font_bold, replikler, portraits, background_img=None):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Replik sayıları
    counter = Counter()
    for r in replikler:
        for k in r.get("speakers", []):
            counter[k] += 1
    characters = sorted(counter.keys())
    items = [(k, counter[k]) for k in characters]

    cols = 3
    cell_margin = 20
    cell_w = WIDTH // cols
    cell_h = int(HEIGHT * 0.3)
    max_rows = HEIGHT // cell_h
    per_page = cols * max_rows
    scroll_index = 0
    selected = 0

    while True:
        if background_img:
            screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 20))

        view = items[scroll_index:scroll_index + per_page]
        for i, (name, count) in enumerate(view):
            row = i // cols
            col = i % cols
            x = col * cell_w + cell_margin // 2
            y = row * cell_h + cell_margin // 2
            is_selected = (i == selected % per_page)

            rect = pygame.Rect(x, y, cell_w - cell_margin, cell_h - cell_margin)
            pygame.draw.rect(screen, (60, 60, 60) if is_selected else (30, 30, 30), rect, border_radius=12)

            if name in portraits:
                img = pygame.transform.smoothscale(portraits[name], (int(rect.width * 0.8), int(rect.height * 0.4)))
                screen.blit(img, (rect.centerx - img.get_width() // 2, rect.y + 10))

            name_txt = font_bold.render(name, True, (255, 255, 0) if is_selected else (255, 255, 255))
            screen.blit(name_txt, (rect.x + 10, rect.y + rect.height * 0.6))

            rep_txt = font.render(f"{count} replik", True, (180, 180, 180))
            screen.blit(rep_txt, (rect.x + 10, rect.y + rect.height * 0.75))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(items)
                elif ev.key == pygame.K_LEFT:
                    selected = (selected - 1 + len(items)) % len(items)
                elif ev.key == pygame.K_DOWN:
                    selected = (selected + cols) % len(items)
                elif ev.key == pygame.K_UP:
                    selected = (selected - cols + len(items)) % len(items)
                elif ev.key == pygame.K_RETURN:
                    return items[selected][0]
                elif ev.key == pygame.K_PAGEUP or ev.key == pygame.K_w:
                    scroll_index = max(scroll_index - cols, 0)
                elif ev.key == pygame.K_PAGEDOWN or ev.key == pygame.K_s:
                    scroll_index = min(scroll_index + cols, len(items) - per_page)
        clock.tick(30)


import pygame
from collections import Counter
from data_loader import normalize_name

def character_grid_menu(screen, font, font_bold, replikler, portraits, background_img=None):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Replik sayıları
    counter = Counter()
    for r in replikler:
        for k in r.get("speakers", []):
            counter[k] += 1
    characters = sorted(counter.keys())
    items = [(k, counter[k]) for k in characters]

    cols = 3
    cell_margin = 20
    cell_w = WIDTH // cols
    cell_h = int(HEIGHT * 0.3)
    max_rows = HEIGHT // cell_h
    per_page = cols * max_rows
    selected = 0

    while True:
        scroll_index = (selected // per_page) * per_page
        view = items[scroll_index:scroll_index + per_page]

        if background_img:
            screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 20))

        for i, (name, count) in enumerate(view):
            row = i // cols
            col = i % cols
            x = col * cell_w + cell_margin // 2
            y = row * cell_h + cell_margin // 2
            is_selected = (scroll_index + i == selected)

            rect = pygame.Rect(x, y, cell_w - cell_margin, cell_h - cell_margin)
            pygame.draw.rect(screen, (60, 60, 60) if is_selected else (30, 30, 30), rect, border_radius=12)

            if name in portraits:
                img = pygame.transform.smoothscale(portraits[name], (int(rect.width * 0.8), int(rect.height * 0.4)))
                screen.blit(img, (rect.centerx - img.get_width() // 2, rect.y + 10))

            name_txt = font_bold.render(name, True, (255, 255, 0) if is_selected else (255, 255, 255))
            screen.blit(name_txt, (rect.x + 10, rect.y + rect.height * 0.6))

            rep_txt = font.render(f"{count} replik", True, (180, 180, 180))
            screen.blit(rep_txt, (rect.x + 10, rect.y + rect.height * 0.75))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(items)
                elif ev.key == pygame.K_LEFT:
                    selected = (selected - 1 + len(items)) % len(items)
                elif ev.key == pygame.K_DOWN:
                    selected = (selected + cols) % len(items)
                elif ev.key == pygame.K_UP:
                    selected = (selected - cols + len(items)) % len(items)
                elif ev.key == pygame.K_RETURN:
                    return items[selected][0]
                elif ev.key == pygame.K_PAGEUP or ev.key == pygame.K_w:
                    selected = max(selected - per_page, 0)
                elif ev.key == pygame.K_PAGEDOWN or ev.key == pygame.K_s:
                    selected = min(selected + per_page, len(items) - 1)
        clock.tick(30)


import pygame
from collections import Counter
from data_loader import normalize_name

def character_grid_menu(screen, font, font_bold, replikler, portraits, background_img=None):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    counter = Counter()
    for r in replikler:
        for k in r.get("speakers", []):
            counter[k] += 1
    characters = sorted(counter.keys())
    items = [(k, counter[k]) for k in characters]

    cols = 3
    cell_margin = 20
    cell_w = WIDTH // cols
    cell_h = int(HEIGHT * 0.3)
    max_rows = HEIGHT // cell_h
    per_page = cols * max_rows
    selected_index = 0  # global index

    while True:
        # scroll_index hesaplanır: seçili eleman görünür aralıkta olur
        scroll_index = (selected_index // per_page) * per_page
        view = items[scroll_index:scroll_index + per_page]

        if background_img:
            screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 20))

        for i, (name, count) in enumerate(view):
            idx = scroll_index + i
            row = i // cols
            col = i % cols
            x = col * cell_w + cell_margin // 2
            y = row * cell_h + cell_margin // 2
            is_selected = (idx == selected_index)

            rect = pygame.Rect(x, y, cell_w - cell_margin, cell_h - cell_margin)
            pygame.draw.rect(screen, (60, 60, 60) if is_selected else (30, 30, 30), rect, border_radius=12)

            if name in portraits:
                img = pygame.transform.smoothscale(portraits[name], (int(rect.width * 0.8), int(rect.height * 0.4)))
                screen.blit(img, (rect.centerx - img.get_width() // 2, rect.y + 10))

            name_txt = font_bold.render(name, True, (255, 255, 0) if is_selected else (255, 255, 255))
            screen.blit(name_txt, (rect.x + 10, rect.y + rect.height * 0.6))

            rep_txt = font.render(f"{count} replik", True, (180, 180, 180))
            screen.blit(rep_txt, (rect.x + 10, rect.y + rect.height * 0.75))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(items)
                elif ev.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1 + len(items)) % len(items)
                elif ev.key == pygame.K_DOWN:
                    selected_index = (selected_index + cols) % len(items)
                elif ev.key == pygame.K_UP:
                    selected_index = (selected_index - cols + len(items)) % len(items)
                elif ev.key == pygame.K_RETURN:
                    return items[selected_index][0]
        clock.tick(30)


import pygame
from collections import Counter
from data_loader import normalize_name

def character_grid_menu(screen, font, font_bold, replikler, portraits, background_img=None):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Replik sayıları
    counter = Counter()
    for r in replikler:
        for k in r.get("speakers", []):
            counter[k] += 1
    characters = sorted(counter.keys())
    items = [(k, counter[k]) for k in characters]

    cols = 3
    cell_margin = 16
    cell_w = WIDTH // cols
    cell_h = int(HEIGHT * 0.22)  # daha kompakt
    max_rows = HEIGHT // cell_h
    per_page = cols * max_rows
    selected = 0

    while True:
        scroll_index = (selected // per_page) * per_page
        view = items[scroll_index:scroll_index + per_page]

        if background_img:
            screen.blit(pygame.transform.scale(background_img, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 20))

        for i, (name, count) in enumerate(view):
            row = i // cols
            col = i % cols
            x = col * cell_w + cell_margin // 2
            y = row * cell_h + cell_margin // 2
            is_selected = (scroll_index + i == selected)

            rect = pygame.Rect(x, y, cell_w - cell_margin, cell_h - cell_margin)
            pygame.draw.rect(screen, (60, 60, 60) if is_selected else (30, 30, 30), rect, border_radius=10)

            if name in portraits:
                img = pygame.transform.smoothscale(portraits[name], (int(rect.width * 0.6), int(rect.height * 0.4)))
                screen.blit(img, (rect.centerx - img.get_width() // 2, rect.y + 6))

            name_txt = font_bold.render(name, True, (255, 255, 0) if is_selected else (255, 255, 255))
            screen.blit(name_txt, (rect.x + 10, rect.y + rect.height * 0.58))

            rep_txt = font.render(f"{count} replik", True, (180, 180, 180))
            screen.blit(rep_txt, (rect.x + 10, rect.y + rect.height * 0.75))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(items)
                elif ev.key == pygame.K_LEFT:
                    selected = (selected - 1 + len(items)) % len(items)
                elif ev.key == pygame.K_DOWN:
                    selected = (selected + cols) % len(items)
                elif ev.key == pygame.K_UP:
                    selected = (selected - cols + len(items)) % len(items)
                elif ev.key == pygame.K_RETURN:
                    return items[selected][0]
                elif ev.key == pygame.K_PAGEUP or ev.key == pygame.K_w:
                    selected = max(selected - per_page, 0)
                elif ev.key == pygame.K_PAGEDOWN or ev.key == pygame.K_s:
                    selected = min(selected + per_page, len(items) - 1)
        clock.tick(30)
