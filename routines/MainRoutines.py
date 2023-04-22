## routines/MainRoutines.py
import logging
import asyncio
import time
from .BasicRoutines import BasicRoutineSendMouseClickAllWowWindows, BasicRoutineSendKeyAllWowWindows
from .SubRoutines import SubRoutineCloseAnyFrame, SubRoutineSetView5, SubRoutineInteractAhNpc, SubRoutineAntiAfk, SubRoutineTsmPostCancelButton
from configparser import ConfigParser
from .utils.log_setup import setup_logging


#log setup from /routines/utils/log_setup.py#
setup_logging()

## PARSING CONFIG FILE ##
config = ConfigParser()
config.read('config/config_default.ini')

## MAIN ROUTINES ##

async def MainRoutineCollectMail():
    whocallthisfunction = "MainRoutineCollectMail"  
    TimeWaitCollectMails = config.getint('MainRoutineCollectMail', 'TimeWaitCollectMails')
    MailboxPositionWindow1X = config.getint('MainRoutineCollectMail', 'MailboxPositionWindow1X')
    MailboxPositionWindow1y = config.getint('MainRoutineCollectMail', 'MailboxPositionWindow1y')
    TSMOpenAllMailWindow1X = config.getint('MainRoutineCollectMail', 'TSMOpenAllMailWindow1X')
    TSMOpenAllMailWindow1Y = config.getint('MainRoutineCollectMail', 'TSMOpenAllMailWindow1Y')
    logging.info ("[MainRoutineCollectMail] CollectMails Main Routine")
    logging.debug ("[MainRoutineCollectMail] Debug mode enabled")
    logging.debug("[MainRoutineCollectMail] Start of MainRoutineCollectMail")
    result = await SubRoutineSetView5(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    result = await SubRoutineCloseAnyFrame(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    logging.info ("[MainRoutineCollectMail] Interact with Mailbox")
    result = await BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"right", 1, MailboxPositionWindow1X, MailboxPositionWindow1y, 2)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    logging.info ("[MainRoutineCollectMail] Click - 'OPEN ALL MAIL' TSM Addon Button")
    result = await BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, TSMOpenAllMailWindow1X, TSMOpenAllMailWindow1Y, 2)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    logging.info(f"[MainRoutineCollectMail] Aguardando {TimeWaitCollectMails} Segundos para coletar todos os mails")
    for i in range(TimeWaitCollectMails, 0, -1):
        await asyncio.sleep(1)
        if i % 10 == 0:
            if i != 10 and i !=5 and i !=TimeWaitCollectMails:
                logging.info (f"[MainRoutineCollectMail] Waiting {i} Seconds to collect all mails")
        if i < 10:
            logging.info (f"[MainRoutineCollectMail] Waiting {i} Seconds to collect all mails")
    logging.debug ("[MainRoutineCollectMail] End of MainRoutineCollectMail")
    return True

async def MainRoutinePostAuctions():
    whocallthisfunction = "MainRoutinePostAuctions"
    TSMRunPostScanButtonWindow1X = config.getint('MainRoutinePostAuctions', 'TSMRunPostScanButtonWindow1X')
    TSMRunPostScanButtonWindow1Y = config.getint('MainRoutinePostAuctions', 'TSMRunPostScanButtonWindow1Y')
    TimeKeepPressingTSMPostCancelButtonForPost = config.getint('MainRoutinePostAuctions', 'TimeKeepPressingTSMPostCancelButtonForPost')
    TimeWaitPostScan = config.getint('MainRoutinePostAuctions', 'TimeWaitPostScan')
    TSMAuctioningTabWindow1X = config.getint('GeneralSettings', 'TSMAuctioningTabWindow1X')
    TSMAuctioningTabWindow1Y = config.getint('GeneralSettings', 'TSMAuctioningTabWindow1Y')
    TSMAuctioningTabWindow1Y = config.getint('GeneralSettings', 'TSMAuctioningTabWindow1Y')
    logging.info("[MainRoutinePostAuctions] Post Auctions Main Routine")
    logging.debug ("[MainRoutinePostAuctions] Debug mode enabled")
    logging.debug ("[MainRoutinePostAuctions] Start of MainRoutinePostAuctions")
    result = await SubRoutineSetView5(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    result = await SubRoutineCloseAnyFrame(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    result = await SubRoutineInteractAhNpc(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    await asyncio.sleep(2)
    logging.info ("[MainRoutinePostAuctions] Click TSM 'Auctioning' tab")
    result = await BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, TSMAuctioningTabWindow1X, TSMAuctioningTabWindow1Y, 2)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    logging.info ("[MainRoutinePostAuctions] Click TSM 'Run Post Scan' button")
    result = await BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, TSMRunPostScanButtonWindow1X, TSMRunPostScanButtonWindow1Y, 2)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    # Fase TimeWaitPostScan
    logging.info (f"[MainRoutinePostAuctions] Waiting {TimeWaitPostScan} seconds for PostScan")
    for i in range(TimeWaitPostScan, 0, -1):
        await asyncio.sleep(1)
        if i % 5 == 0:
            if i != 10 and i !=5 and i !=TimeWaitPostScan:
                    logging.info (f"[MainRoutinePostAuctions] Waiting {i} seconds for PostScan")
        if i <= 10:
            logging.info (f"[MainRoutinePostAuctions] Waiting {i} seconds for PostScan")
    # Fase TimeKeepPressingTSMPostCancelButtonForPost
    logging.info (f"[MainRoutinePostAuctions] Pressing TSM Post/Cancel Button for {TimeKeepPressingTSMPostCancelButtonForPost} seconds")
    start_time = time.time()
    last_update_time = 0
    while time.time() - start_time < TimeKeepPressingTSMPostCancelButtonForPost:
        result = await SubRoutineTsmPostCancelButton(whocallthisfunction)
        if not result:
            logging.critical(f"[{whocallthisfunction}] -> Closing APP")
            return False
        elapsed_time = time.time() - start_time
        remaining_time = TimeKeepPressingTSMPostCancelButtonForPost - elapsed_time
        if 2 <= remaining_time <= 10:
            logging.info (f"[MainRoutinePostAuctions] {int(remaining_time)} seconds left to press Post/Cancel")
        elif int(elapsed_time) % 10 == 0 and int(elapsed_time) != last_update_time:
            last_update_time = int(elapsed_time)
            logging.info(f"[MainRoutinePostAuctions] {int(remaining_time)} seconds left to press Post/Cancel")
        await asyncio.sleep(0.2)
    logging.debug ("[MainRoutinePostAuctions] End of MainRoutinePostAuctions")
    return True

async def MainRoutineCancelScanAuctions():
    whocallthisfunction = "MainRoutineCancelScanAuctions"
    TimeWaitCancelScan = config.getint('MainRoutineCancelScanAuctions', 'TimeWaitCancelScan')
    TimeKeepPressingTSMPostCancelButtonForCancel = config.getint('MainRoutineCancelScanAuctions', 'TimeKeepPressingTSMPostCancelButtonForCancel')
    TSMRunCancelScanButtonWindow1X = config.getint('MainRoutineCancelScanAuctions', 'TSMRunCancelScanButtonWindow1X')
    TSMRunCancelScanButtonWindow1Y = config.getint('MainRoutineCancelScanAuctions', 'TSMRunCancelScanButtonWindow1Y')
    TSMAuctioningTabWindow1X = config.getint('GeneralSettings', 'TSMAuctioningTabWindow1X')
    TSMAuctioningTabWindow1Y = config.getint('GeneralSettings', 'TSMAuctioningTabWindow1Y')
    logging.info("[MainRoutineCancelScanAuctions] Cancel Auctions Main Routine")
    logging.debug ("[MainRoutineCancelScanAuctions] Debug mode enabled")
    logging.debug ("[MainRoutineCancelScanAuctions] Start of MainRoutineCancelScanAuctions")
    result = await SubRoutineSetView5(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    result = await SubRoutineCloseAnyFrame(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    result = await SubRoutineInteractAhNpc(whocallthisfunction)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    await asyncio.sleep(2)
    logging.info ("[MainRoutineCancelScanAuctions] Click TSM 'Auctioning' tab")
    result = await BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, TSMAuctioningTabWindow1X, TSMAuctioningTabWindow1Y, 2)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    logging.info ("[MainRoutineCancelScanAuctions] Click TSM 'Run Cancel Scan' button")
    result = await BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, TSMRunCancelScanButtonWindow1X, TSMRunCancelScanButtonWindow1Y, 2)
    if not result:
        logging.critical(f"[{whocallthisfunction}] -> Closing APP")
        return False
    # Fase TimeWaitCancelScan
    logging.info (f"[MainRoutineCancelScanAuctions] Waiting {TimeWaitCancelScan} seconds for CancelScan")
    for i in range(TimeWaitCancelScan, 0, -1):
        await asyncio.sleep(1)
        if i % 10 == 0:
            if i != 10 and i !=5 and i != TimeWaitCancelScan:
                logging.info (f"[MainRoutineCancelScanAuctions] {i} seconds left for CancelScan")
        if i < 10:
            logging.info (f"[MainRoutineCancelScanAuctions] {i} seconds left for CancelScan")
    # Fase TimeKeepPressingTSMPostCancelButtonForCancel
    logging.info (f"[MainRoutineCancelScanAuctions] Pressing TSM Post/Cancel Button for {TimeKeepPressingTSMPostCancelButtonForCancel} seconds")
    start_time = time.time()
    last_update_time = 0
    while time.time() - start_time < TimeKeepPressingTSMPostCancelButtonForCancel:
        result = await SubRoutineTsmPostCancelButton(whocallthisfunction)
        if not result:
            logging.critical(f"[{whocallthisfunction}] -> Closing APP")
            return False
        elapsed_time = time.time() - start_time
        remaining_time = TimeKeepPressingTSMPostCancelButtonForCancel - elapsed_time
        if 2 <= remaining_time <= 10:
            logging.info (f"[MainRoutineCancelScanAuctions] {int(remaining_time)} seconds left to press Post/Cancel")
        elif int(elapsed_time) % 10 == 0 and int(elapsed_time) != last_update_time:
            last_update_time = int(elapsed_time)
            logging.info(f"[MainRoutineCancelScanAuctions] {int(remaining_time)} seconds left to press Post/Cancel")
        await asyncio.sleep(0.2)
    logging.debug ("[MainRoutineCancelScanAuctions] End of MainRoutineCancelScanAuctions")
    return True