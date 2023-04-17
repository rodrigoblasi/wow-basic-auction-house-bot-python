## routines/SubRoutines.py
import logging
import asyncio
import time
from .BasicRoutines import BasicRoutineSendMouseClickAllWowWindows, BasicRoutineSendKeyAllWowWindows
from .utils.log_setup import setup_logging
from .utils.utilities import CriticalError


#log setup from /routines/utils/log_setup.py#
setup_logging()

async def SubRoutineCloseAnyFrame(whocallthisfunction=False):
    thisroutinename = "SubRoutineCloseAnyFrame"
    logging.info(f"[{whocallthisfunction}]->[SubRoutineCloseAnyFrame] CloseAnyFrame routine")
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineCloseAnyFrame] Debug mode enabled")
    logging.debug(f"[{whocallthisfunction}]->[SubRoutineCloseAnyFrame] Start of Close Any Frame routine")
    #Send Esc 2 times just to make sure it works
    logging.debug(f"[{whocallthisfunction}]->[SubRoutineCloseAnyFrame] Pressing key to close all opened frames (ESC)")
    result = await BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number=1, key='ESC', key_press_count=2)
    if not result:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}]")
        return False
    logging.debug(f"[{whocallthisfunction}]->[SubRoutineCloseAnyFrame] Click 'Return to game' button if it exists")
    result = await BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, 845, 545, 2)
    if not result:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}]")
        return False
    logging.debug(f"[{whocallthisfunction}]->[SubRoutineCloseAnyFrame] End of CloseAnyFrame routine")
    return True


async def SubRoutineSetView5(whocallthisfunction=False):
    thisroutinename = "SubRoutineSetView5"
    logging.info (f"[{whocallthisfunction}]->[SubRoutineSetView5] SetView5 routine")
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineSetView5] Debug mode enabled")
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineSetView5] Start of SetView5 routine")
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineSetView5] Pressing key to macro to 'SetView5' (2)")
    #macro binded on action bar
    result = await BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number=1, key='2', key_press_count=1)
    if not result:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}]")
        return False
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineSetView5] End of SetView5 routine")
    return True

async def SubRoutineAntiAfk(whocallthisfunction=False):
    thisroutinename = "SubRoutineAntiAfk"
    whocallthisfunction="SubRoutineAntiAfk"
    logging.info (f"[SubRoutineAntiAfk] Anti AFK routine")
    logging.debug (f"[SubRoutineAntiAfk] Debug mode enabled")
    logging.debug (f"[SubRoutineAntiAfk] Start of Anti AFK routine")
    #do we need SubRoutineCloseAnyFrame()?
    #await SubRoutineCloseAnyFrame()
    #Send Jump 1 times
    logging.debug (f"[SubRoutineAntiAfk] Pressing key to 'JUMP' (SPACE)")
    result = await BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number=1, key='SPACE', key_press_count=1)
    if not result:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}]")
        return False
    logging.debug (f"[SubRoutineAntiAfk] End of Anti AFK routine")
    return True

async def SubRoutineInteractAhNpc(whocallthisfunction=False):
    thisroutinename = "SubRoutineInteractAhNpc"
    logging.info (f"[{whocallthisfunction}]->[SubRoutineInteractAhNpc] Interact AH NPC routine")
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineInteractAhNpc] Debug mode enabled")
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineInteractAhNpc] Start of Interact AH NPC routine")
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineInteractAhNpc] Pressing key to macro to 'target AH NPC' (3)")
    #macro binded on action bar
    result = await BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number=1, key='3', key_press_count=2)
    if not result:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}]")
        return False
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineInteractAhNpc] Wait 1 sec")
    time.sleep(1)
    #In game "Interact with target" binded key
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineInteractAhNpc] Pressing key 'Interact with target'(k)")
    result = await BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number=1, key='k', key_press_count=2)
    if not result:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}]")
        return False
    logging.debug(f"[{whocallthisfunction}]->[SubRoutineInteractAhNpc] End of Interact AH NPC routine")
    return True

async def SubRoutineTsmPostCancelButton(whocallthisfunction):
    thisroutinename = "SubRoutineTsmPostCancelButton"
    logging.debug (f"[{whocallthisfunction}]->[SubRoutineTsmPostCancelButton] Pressing 'TSM Post/Cancel macro' key (1)")
    #macro binded on action bar
    result = await BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number=1, key='1', key_press_count=1)
    if not result:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}]")
        return False
    return True