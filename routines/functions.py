import asyncio
import win32gui
import win32con
import win32api
import time
import win32con


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

def BasicRoutineSendMouseClickAllWowWindows(mouse_button, window_number, x, y, click_count, debug=False):
    if debug:
        print("Debug mode enabled!")
        
    if not isinstance(mouse_button, str) or mouse_button.lower() not in ["left", "right"]:
        print("Erro: botão do mouse inválido. Use 'left' ou 'right'.")
        return
    if not isinstance(window_number, int) or not (1 <= window_number <= 99):
        print("Erro: número de janela inválido. Use um número entre 1 e 99.")
        return
    if not isinstance(x, int) or not isinstance(y, int):
        print("Erro: coordenadas x e y inválidas. Ambas devem ser números inteiros.")
        return
    if not isinstance(click_count, int) or not (1 <= click_count <= 99):
        print("Erro: número de cliques inválido. Use um número entre 1 e 99.")
        return
    wow_windows = BasicRoutineGetInfoAllWowWindows()
    if window_number not in wow_windows:
        print(f"Erro: a janela {window_number} não foi encontrada.")
        return
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
            if debug:
                print(f"Clicando com botão {mouse_button} na janela {window_num} na posição {window_x - window['x']},{window_y - window['y']}")
        time.sleep(0.5)
    win32api.SetCursorPos(initial_mouse_pos)

def BasicRoutineSendKeyAllWowWindows(window_number, key, key_press_count, debug=False):
    if not isinstance(window_number, int) or not (1 <= window_number <= 99):
        print("Erro: número de janela inválido. Use um número entre 1 e 99.")
        return
    if not isinstance(key, str) or (len(key) != 1 and key not in ['ESC', 'SPACE']):
        print("Erro: a tecla deve ser uma única letra, número, ESC ou SPACE.")
        return
    if not isinstance(key_press_count, int) or not (1 <= key_press_count <= 99):
        print("Erro: número de pressionamentos de tecla inválido. Use um número entre 1 e 99.")
        return
    wow_windows = BasicRoutineGetInfoAllWowWindows()
    if window_number not in wow_windows:
        print(f"Erro: a janela {window_number} não foi encontrada.")
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
        if debug:
            print(f"Tecla '{key}' enviada para a janela {window_number}.")
        # Enviar a tecla para todas as outras janelas do WoW
        for other_window_number, other_window in wow_windows.items():
            if other_window_number != window_number:
                send_key_to_window(other_window["hwnd"])
                if debug:
                    print(f"Tecla '{key}' enviada para a janela {other_window_number}.")
        loop_count += 1
        # aguardar 1 segundo para a próxima rodada de teclas
        time.sleep(0.5)
    if debug:
        print(f"Tecla '{key}' enviada para todas as janelas {key_press_count} vezes.")


## SUBROUTINES ##

async def SubRoutineCloseAnyFrame():
    print("Start of Close Any Frame routine")
    #Send Esc 2 times just to make sure it works
    BasicRoutineSendKeyAllWowWindows(window_number=1, key='ESC', key_press_count=2)
    time.sleep(1)
    #click "Return to game" button if it exists
    BasicRoutineSendMouseClickAllWowWindows("left", 1, 845, 545, 2)
    print("End of Close Any Frame routine")

async def SubRoutineSetView5():
    print("Start of SetView5 routine")
    #macro binded on action bar
    BasicRoutineSendKeyAllWowWindows(window_number=1, key='2', key_press_count=2)
    print("End of SetView5 routine")

async def SubRoutineAntiAfk():
    print("Start of Anti AFK routine")
    SubRoutineCloseAnyFrame()
    #Send Jump 1 times
    BasicRoutineSendKeyAllWowWindows(window_number=1, key='SPACE', key_press_count=1)
    print("End of Anti AFK routine")

async def SubRoutineInteractAhNpc():
    print("Start of Interact AH NPC routine")
    #macro binded on action bar
    BasicRoutineSendKeyAllWowWindows(window_number=1, key='3', key_press_count=2)
    time.sleep(1)
    #In game "Interact with target" binded key
    BasicRoutineSendKeyAllWowWindows(window_number=1, key='k', key_press_count=2)
    print("End of Interact AH NPC routine")

async def SubRoutineTsmPostCancelButton():
    print("Start of TSM Post/Cancel button routine")
    #macro binded on action bar
    BasicRoutineSendKeyAllWowWindows(window_number=1, key='1', key_press_count=1)
    print("End of TSM Post/Cancel button routine")

## MAIN ROUTINES ##

async def MainRoutineCollectMail():
    print ("Start of MainRoutineCollectMail")
    await SubRoutineSetView5()
    await SubRoutineCloseAnyFrame()
    print ("Interact with Mailbox")
    BasicRoutineSendMouseClickAllWowWindows("right", 1, 770, 585, 2)
    print ("Click - 'OPEN ALL MAIL' TSM Addon Button")
    BasicRoutineSendMouseClickAllWowWindows("left", 1, 615, 350, 2)
    print ("End of MainRoutineCollectMail")

async def MainRoutinePostAuctions():
    print ("Start of MainRoutinePostAuctions")
    await SubRoutineSetView5()
    await SubRoutineCloseAnyFrame()
    await SubRoutineInteractAhNpc()
    await asyncio.sleep(2)
    #click "auctioning frame tsm"
    BasicRoutineSendMouseClickAllWowWindows("left", 1, 170, 20, 2)
    #click "Run Post Scan" TSM button
    BasicRoutineSendMouseClickAllWowWindows("left", 1, 110, 290, 2)
    countdown = 20
    for i in range(countdown, 0, -1):
        print("Aguardando:", i)
        await asyncio.sleep(1)
    for i in range(30):
        await SubRoutineTsmPostCancelButton()
    print ("End of MainRoutinePostAuctions")

async def MainRoutineCancelScanAuctions():
    print ("Start of MainRoutineCancelScanAuctions")
    await SubRoutineSetView5()
    await SubRoutineCloseAnyFrame()
    await SubRoutineInteractAhNpc()
    await asyncio.sleep(2)
    #click "auctioning frame" TSM
    BasicRoutineSendMouseClickAllWowWindows("left", 1, 170, 20, 2)
    #click "Run Cancel Scan" TSM button
    BasicRoutineSendMouseClickAllWowWindows("left", 1, 110, 320, 2)
    countdown = 60
    for i in range(countdown, 0, -1):
        print("Aguardando:", i, "Segundos")
        await asyncio.sleep(1)
    for i in range(60):
        await SubRoutineTsmPostCancelButton()
    print ("End of MainRoutinePostAuctions")



#asyncio.run(MainRoutineCancelScanAuctions())
asyncio.run(MainRoutinePostAuctions())