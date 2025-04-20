
import os
import json
import unicodedata
import pygame

def normalize_name(name):
    substitutions = {
        "ç": "c", "ş": "s", "ğ": "g", "ı": "i", "ö": "o", "ü": "u"
    }
    key = name.strip().lower().replace(" ", "")
    for src, tgt in substitutions.items():
        key = key.replace(src, tgt)
    key = unicodedata.normalize("NFKD", key)
    return ''.join([c for c in key if not unicodedata.combining(c)])

def load_replikler(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_portraits(replikler, settings):
    portraits = {}
    for r in replikler:
        for k in r.get("speakers", []):
            if k not in portraits:
                norm = normalize_name(k)
                fn = f"{norm}.png"
                path = os.path.join(settings.PORTRAIT_FOLDER, fn)
                try:
                    portraits[k] = pygame.image.load(path)
                except:
                    default_path = os.path.join(settings.PORTRAIT_FOLDER, settings.DEFAULT_PORTRAIT)
                    portraits[k] = pygame.image.load(default_path)
    return portraits
