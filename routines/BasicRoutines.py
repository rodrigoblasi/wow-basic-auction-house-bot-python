## routines/BasicRoutines.py

import logging
import win32gui
import win32con
import win32api
import time
import win32con
from .utils.log_setup import setup_logging

#log setup from /routines/utils/log_setup.py#
setup_logging()

## BASIC FUNCTIONS ##
def BasicRoutineGetInfoAllWowWindows():
    # Função para obter informações sobre todas as janelas do World of Warcraft (WoW)
    # Retorna um dicionário com informações sobre cada janela identificada
    # Cria um dicionário vazio para armazenar as informações das janelas do WoW
    wow_windows = {}
    # Loop de 1 a 99 para buscar janelas com títulos que começam com "is" + número do loop
    for i in range(1, 100):
        window_title_prefix = "is" + str(i)  # Prefixo do título da janela
        hwnd = win32gui.FindWindow(None, None)  # Obtém o identificador da primeira janela encontrada
        # Loop para percorrer todas as janelas encontradas
        while hwnd:
            window_title = win32gui.GetWindowText(hwnd)  # Obtém o título da janela
            if window_title.startswith(window_title_prefix):  # Verifica se o título começa com o prefixo esperado
                window_rect = win32gui.GetWindowRect(hwnd)  # Obtém as coordenadas e tamanho da janela
                window_x = window_rect[0]  # Coordenada X da janela
                window_y = window_rect[1]  # Coordenada Y da janela
                window_width = window_rect[2] - window_x  # Largura da janela
                window_height = window_rect[3] - window_y  # Altura da janela
                window_info = {
                    "number": i,  # Número da janela
                    "title": window_title,  # Título da janela
                    "height": window_height,  # Altura da janela
                    "width": window_width,  # Largura da janela
                    "x": window_x,  # Coordenada X da janela
                    "y": window_y,  # Coordenada Y da janela
                    "hwnd": hwnd  # Identificador da janela
                }
                wow_windows[i] = window_info  # Adiciona as informações da janela ao dicionário
                break
            hwnd = win32gui.FindWindowEx(None, hwnd, None, None)  # Obtém o identificador da próxima janela
    return wow_windows  # Retorna o dicionário com as informações das janelas do WoW

def BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,mouse_button, window_number, x, y, click_count):
    logging.debug("[BasicRoutineSendMouseClickAllWowWindows] Debug mode enabled")    
    if not isinstance(mouse_button, str) or mouse_button.lower() not in ["left", "right"]:
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] botão do mouse inválido. Use 'left' ou 'right'.")
        return False
    if not isinstance(window_number, int) or not (1 <= window_number <= 99):
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] número de janela inválido. Use um número entre 1 e 99.")
        return False
    if not isinstance(x, int) or not isinstance(y, int):
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] coordenadas x e y inválidas. Ambas devem ser números inteiros.")
        return False
    if not isinstance(click_count, int) or not (1 <= click_count <= 99):
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] número de cliques inválido. Use um número entre 1 e 99.")
        return False
    wow_windows = BasicRoutineGetInfoAllWowWindows()
    if window_number not in wow_windows:
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] a janela {window_number} não foi encontrada.")
        return False
    mouse_button_event = win32con.MOUSEEVENTF_LEFTDOWN if mouse_button.lower() == "left" else win32con.MOUSEEVENTF_RIGHTDOWN
    mouse_button_event_up = win32con.MOUSEEVENTF_LEFTUP if mouse_button.lower() == "left" else win32con.MOUSEEVENTF_RIGHTUP
    initial_mouse_pos = win32api.GetCursorPos()
    for _ in range(click_count):
        for window_num, window in wow_windows.items():
            window_x = window["x"] + int(x * window["width"] / wow_windows[window_number]["width"])
            window_y = window["y"] + int(y * window["height"] / wow_windows[window_number]["height"])
            win32api.SetCursorPos((window_x, window_y))
            win32api.mouse_event(mouse_button_event, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(mouse_button_event_up, 0, 0, 0, 0)
            time.sleep(0.1)
            logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] Clicando com botão {mouse_button} na janela {window_num} na posição {window_x - window['x']},{window_y - window['y']}")
        time.sleep(0.5)
        logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] Retornando o mouse para a posição inicial")
        win32api.SetCursorPos(initial_mouse_pos)
        return True

def BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number, key, key_press_count):
    logging.debug("[BasicRoutineSendKeyAllWowWindows] Debug mode enabled")
    if not isinstance(window_number, int) or not (1 <= window_number <= 99):
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] número de janela inválido. Use um número entre 1 e 99.")
        return
    if not isinstance(key, str) or (len(key) != 1 and key not in ['ESC', 'SPACE']):
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] a tecla deve ser uma única letra, número, ESC ou SPACE.")
        return
    if not isinstance(key_press_count, int) or not (1 <= key_press_count <= 99):
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] número de pressionamentos de tecla inválido. Use um número entre 1 e 99.")
        return
    wow_windows = BasicRoutineGetInfoAllWowWindows()
    if window_number not in wow_windows:
        logging.critical(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] a janela {window_number} não foi encontrada.")
        return
    target_window = wow_windows[window_number]
    if key == 'ESC':
        vk_code = win32con.VK_ESCAPE
    elif key == 'SPACE':
        vk_code = win32con.VK_SPACE
    else:
        vk_code = win32api.VkKeyScanEx(key, 0)
    def send_key_to_window(window_hwnd):
        win32gui.SendMessage(window_hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        time.sleep(0.1)
        win32gui.SendMessage(window_hwnd, win32con.WM_KEYUP, vk_code, 0)
        time.sleep(0.1)
    loop_count = 0
    while loop_count < key_press_count:
        # Enviar a tecla para a janela alvo
        send_key_to_window(target_window["hwnd"])
        logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] Tecla '{key}' enviada para a janela {window_number}.")
        # Enviar a tecla para todas as outras janelas do WoW
        for other_window_number, other_window in wow_windows.items():
            if other_window_number != window_number:
                send_key_to_window(other_window["hwnd"])
                logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] Tecla '{key}' enviada para a janela {other_window_number}.")
        loop_count += 1
    logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] Tecla '{key}' enviada para todas as janelas {key_press_count} vezes.")