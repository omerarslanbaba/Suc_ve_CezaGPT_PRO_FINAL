"""Pytest ortak yardımcıları."""
import json
import types
from pathlib import Path
import pytest

@pytest.fixture()
def sample_replikler(tmp_path):
    """Geçici JSON dosyasında üç sahte replik döndürür."""
    data = [
        {"perde": 1, "bolum": 1, "tablo": 1, "speakers": ["Raskolnikov"], "text": "..."},
        {"perde": 1, "bolum": 1, "tablo": 1, "speakers": ["Razumikin"], "text": "..."},
        {"perde": 1, "bolum": 2, "tablo": 3, "speakers": ["Sonya"], "text": "..."},
    ]
    f = tmp_path / "replikler.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    return f

@pytest.fixture(autouse=True)
def no_pygame_display(monkeypatch):
    """Pygame'in display init çağrılarını stub'lar, CI'da X sunucusu gerektirmez."""
    import pygame
    monkeypatch.setattr(pygame, "init", lambda: None)
    monkeypatch.setattr(pygame, "display", types.SimpleNamespace(set_mode=lambda *a, **k: None))