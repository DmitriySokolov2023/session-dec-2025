import sys
import ctypes
from ctypes import wintypes
import pygame


def open_file_dialog_windows(filter_ext="*.comtest", initial_dir=None):
    if sys.platform != "win32":
        return None

    class OPENFILENAMEW(ctypes.Structure):
        _fields_ = [
            ("lStructSize", wintypes.DWORD),
            ("hwndOwner", wintypes.HWND),
            ("hInstance", wintypes.HINSTANCE),
            ("lpstrFilter", wintypes.LPCWSTR),
            ("lpstrCustomFilter", wintypes.LPWSTR),
            ("nMaxCustFilter", wintypes.DWORD),
            ("nFilterIndex", wintypes.DWORD),
            ("lpstrFile", wintypes.LPWSTR),        
            ("nMaxFile", wintypes.DWORD),
            ("lpstrFileTitle", wintypes.LPWSTR),
            ("nMaxFileTitle", wintypes.DWORD),
            ("lpstrInitialDir", wintypes.LPCWSTR), 
            ("lpstrTitle", wintypes.LPCWSTR),
            ("Flags", wintypes.DWORD),
            ("nFileOffset", wintypes.WORD),
            ("nFileExtension", wintypes.WORD),
            ("lpstrDefExt", wintypes.LPCWSTR),
            ("lCustData", wintypes.LPARAM),
            ("lpfnHook", wintypes.LPVOID),
            ("lpTemplateName", wintypes.LPCWSTR),
            ("pvReserved", wintypes.LPVOID),
            ("dwReserved", wintypes.DWORD),
            ("FlagsEx", wintypes.DWORD),
        ]

    flt = f"COMTEST files ({filter_ext})\0{filter_ext}\0All files (*.*)\0*.*\0\0"

    buffer = ctypes.create_unicode_buffer(1024)

    ofn = OPENFILENAMEW()
    ofn.lStructSize = ctypes.sizeof(OPENFILENAMEW)
    ofn.hwndOwner = None
    ofn.hInstance = None
    ofn.lpstrFilter = flt
    ofn.lpstrFile = ctypes.cast(buffer, wintypes.LPWSTR)  
    ofn.nMaxFile = 1024
    ofn.lpstrTitle = "Выберите файл"
    ofn.lpstrInitialDir = initial_dir
    ofn.Flags = 0x00000008 | 0x00080000

    ok = ctypes.windll.comdlg32.GetOpenFileNameW(ctypes.byref(ofn))
    return buffer.value if ok else None


class Button:
    def __init__(self, rect, label, action):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action

    def draw(self, screen, font):
        mx, my = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mx, my)
        pygame.draw.rect(screen, (75, 75, 75) if hover else (55, 55, 55), self.rect, border_radius=10)
        pygame.draw.rect(screen, (140, 140, 140), self.rect, 2, border_radius=10)
        t = font.render(self.label, True, (235, 235, 235))
        screen.blit(t, t.get_rect(center=self.rect.center))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()
