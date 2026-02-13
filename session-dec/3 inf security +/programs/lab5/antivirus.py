import os
import pygame
from helpers import open_file_dialog_windows, Button

TAIL_TAG = b"$"  # маркер 
PAYLOAD_HEADER = b"\n--- VIRUS999 PAYLOAD ---"  # начало хвоста, который нужно отрезать
ORIG_KEY = b"ORIGINAL_FIRST3: "  # ключ, по которому достаём сохранённые 3 байта
FALLBACK_ORIG3 = b"\x90\x90\x90"  # запасной вариант

TAIL_CHECK_WINDOW = 100  # последние 100 байт
PAYLOAD_LOOKBACK = 100   # ищем ORIGINAL_FIRST3 в пределах 100 байт

# Проверка на маркер
def probe_infection(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            blob = f.read()
        return TAIL_TAG in blob[-TAIL_CHECK_WINDOW:]
    except Exception:
        return False

# лечение
def cleanse_target(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            blob = f.read()

        if TAIL_TAG not in blob:
            return False  # файл не заражён

        marker_pos = blob.rfind(TAIL_TAG)
        if marker_pos == -1:
            return False

        # Область, где ожидаем строку ORIGINAL_FIRST3
        start_zone = max(0, marker_pos - PAYLOAD_LOOKBACK)
        zone = blob[start_zone:marker_pos]

        # Пытаемся извлечь сохранённые первые 3 байта
        if ORIG_KEY in zone:
            try:
                # split оставляет всё после ключа, берём первые 3 байта
                part = zone.split(ORIG_KEY, 1)[1]
                orig3 = part[:3]
            except Exception:
                orig3 = FALLBACK_ORIG3
        else:
            orig3 = FALLBACK_ORIG3

        # Восстановление первых 3 байт
        healed = orig3 + blob[3:]

        # Обрезаем хвост по PAYLOAD_HEADER
        cut_at = blob.rfind(PAYLOAD_HEADER)
        if cut_at != -1:
            healed = healed[:cut_at]
        with open(path, "wb") as f:
            f.write(healed)

        return True

    except Exception:
        return False

#Интерфейс
class AntiVirusPygameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((760, 300))
        pygame.display.set_caption("Учебный антивирус")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 18)
        self.font_small = pygame.font.SysFont("consolas", 16)

        self.selected_path = None
        self.messages = []

        self.btn_open = Button((20, 20, 120, 40), "OPEN", self.open_file)
        self.btn_scan = Button((150, 20, 120, 40), "SCAN", self.scan_file)
        self.btn_cure = Button((280, 20, 120, 40), "CURE", self.cure_file)
        self.btn_quit = Button((410, 20, 120, 40), "QUIT", self.quit)

        self.running = True
        self.push_msg("Готово. OPEN (проводник Windows) или перетащи файл в окно.")

        # разрешим drag&drop файлов
        try:
            pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.DROPFILE, pygame.DROPTEXT])
        except Exception:
            pass

    def push_msg(self, text):
        self.messages.append(text)
        self.messages = self.messages[-6:]  # последние 6 строк

    def open_file(self):
        path = open_file_dialog_windows("*.comtest")
        if path and os.path.isfile(path):
            self.selected_path = path
            self.push_msg(f"Выбран файл: {path}")
        else:
            self.push_msg("Файл не выбран.")

    def scan_file(self):
        if not self.selected_path:
            self.push_msg("SCAN: сначала выберите файл (OPEN или drag&drop).")
            return
        infected = probe_infection(self.selected_path)
        self.push_msg(f"SCAN: {'ЗАРАЖЁН' if infected else 'ЧИСТ'}")

    def cure_file(self):
        if not self.selected_path:
            self.push_msg("CURE: сначала выберите файл (OPEN или drag&drop).")
            return
        if not probe_infection(self.selected_path):
            self.push_msg("CURE: файл не заражён (маркер не найден).")
            return
        ok = cleanse_target(self.selected_path)
        self.push_msg(f"CURE: {'ВЫЛЕЧЕН' if ok else 'НЕ УДАЛОСЬ ВЫЛЕЧИТЬ'}")

    def quit(self):
        self.running = False

    def handle_drop(self, dropped_path):
        if dropped_path and os.path.isfile(dropped_path):
            self.selected_path = dropped_path
            self.push_msg(f"Выбран (drag&drop): {dropped_path}")
        else:
            self.push_msg("Drag&drop: не удалось прочитать файл.")

    def draw(self):
        self.screen.fill((25, 25, 28))

        # кнопки
        for b in (self.btn_open, self.btn_scan, self.btn_cure, self.btn_quit):
            b.draw(self.screen, self.font)

        # выбранный файл
        sel = self.selected_path if self.selected_path else "(файл не выбран)"
        t1 = self.font_small.render("Selected:", True, (200, 200, 200))
        t2 = self.font_small.render(sel, True, (230, 230, 230))
        self.screen.blit(t1, (20, 80))
        self.screen.blit(t2, (20, 102))

        # сообщения
        base_y = 150
        self.screen.blit(self.font.render("STATUS:", True, (220, 220, 220)), (20, base_y))
        for i, line in enumerate(self.messages):
            tx = self.font_small.render(line, True, (230, 230, 230))
            self.screen.blit(tx, (20, base_y + 30 + i * 20))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    self.btn_open.click(pos)
                    self.btn_scan.click(pos)
                    self.btn_cure.click(pos)
                    self.btn_quit.click(pos)

                elif event.type == pygame.DROPFILE:
                    self.handle_drop(event.file)

                elif event.type == pygame.DROPTEXT:
                    self.handle_drop(event.text)

            self.draw()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = AntiVirusPygameApp()
    app.run()
