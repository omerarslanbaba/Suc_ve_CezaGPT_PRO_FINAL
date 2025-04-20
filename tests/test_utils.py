import json
import types
from pathlib import Path
from data_loader import normalize_name
from game_engine import Game

def test_normalize_name_basic():
    assert normalize_name("Razumíkin ") == "razumikin"
    assert normalize_name("SONYA") == "sonya"

class DummyGame(Game):
    """Gerçek pygame'e ihtiyaç duymayan hafif alt sınıf."""

    def __init__(self, sample_replikler_path):
        # pygame mock'landığından üst sınıf init'ine gitmiyoruz
        self.settings = types.SimpleNamespace(
            WIDTH=800, HEIGHT=600, FONT_NAME="Arial", FONT_SIZE=24, FONT_BOLD_SIZE=26,
            REPLIKLER_DOSYA=str(sample_replikler_path),
            PORTRAIT_FOLDER="assets/portraits",
            BACKGROUND_FOLDER="assets/backgrounds",
            DEFAULT_BG="default.jpg",
            DEFAULT_PORTRAIT="default.png",
            DEFAULT_BACKGROUND_PATH="assets/backgrounds/default.jpg",
            DEFAULT_PORTRAIT_PATH="assets/portraits/default.png",
            FPS=60,
        )
        self.replikler = json.loads(Path(sample_replikler_path).read_text())
        self.scene = (1, 1, 1)
        self.character = "Razumikin"

    def filter(self):
        return super().filter_replikler()

def test_filter_replikler(sample_replikler):
    g = DummyGame(sample_replikler)
    result = g.filter()
    assert len(result) == 1
    assert result[0]["speakers"] == ["Razumikin"]