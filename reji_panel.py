
import pygame
import json

def reji_panel(screen, font, font_bold, data_path="ezber_replikleri_temizlenmis.json"):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    input_char = ""
    input_kw = ""
    selected_index = 0
    scroll = 0
    per_page = 10

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def filter_results(character, keyword):
        results = []
        for r in data:
            speakers = r.get("speakers", [])
            if character and not any(character.lower() in k.lower() for k in speakers):
                continue
            if keyword.lower() in r.get("full", "").lower():
                results.append({
                    "speaker": ", ".join(speakers),
                    "text": r.get("full", ""),
                    "scene": f"{r.get('perde','?')} / {r.get('bolum','?')} / {r.get('tablo','?')}"
                })
        return results

    active_field = "character"
    while True:
        screen.fill((15, 15, 15))

        # Başlık
        title = font_bold.render("🎛 Reji Paneli – Replik Arama", True, (100, 255, 100))
        screen.blit(title, (WIDTH * 0.05, 20))

        # Giriş kutuları
        pygame.draw.rect(screen, (50, 50, 50), (80, 80, 300, 30))
        txt1 = font.render(f"Karakter: {input_char}", True, (255, 255, 255))
        screen.blit(txt1, (90, 85))

        pygame.draw.rect(screen, (50, 50, 50), (420, 80, 300, 30))
        txt2 = font.render(f"Anahtar Kelime: {input_kw}", True, (255, 255, 255))
        screen.blit(txt2, (430, 85))

        # Filtrele
        results = filter_results(input_char, input_kw)
        paged = results[scroll:scroll+per_page]

        for i, r in enumerate(paged):
            y = 140 + i * 60
            pygame.draw.rect(screen, (30, 30, 30), (80, y, WIDTH - 160, 55), border_radius=5)
            speaker = font_bold.render(f"{r['speaker']}", True, (255, 255, 0))
            screen.blit(speaker, (90, y + 5))
            scene = font.render(r['scene'], True, (180, 180, 180))
            screen.blit(scene, (90, y + 25))
            snippet = font.render(r['text'][:80] + "...", True, (200, 200, 200))
            screen.blit(snippet, (90, y + 45))

        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return
                elif ev.key == pygame.K_TAB:
                    active_field = "keyword" if active_field == "character" else "character"
                elif ev.key == pygame.K_BACKSPACE:
                    if active_field == "character":
                        input_char = input_char[:-1]
                    else:
                        input_kw = input_kw[:-1]
                elif ev.key == pygame.K_DOWN:
                    scroll = min(scroll + 1, max(0, len(results) - per_page))
                elif ev.key == pygame.K_UP:
                    scroll = max(scroll - 1, 0)
                elif ev.key == pygame.K_RETURN:
                    pass
                else:
                    if active_field == "character":
                        input_char += ev.unicode
                    else:
                        input_kw += ev.unicode

        clock.tick(30)
