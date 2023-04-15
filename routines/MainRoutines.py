## routines/MainRoutines.py
import logging
import asyncio
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
    logging.info ("[MainRoutineCollectMail] CollectMail Main Routine")
    logging.debug ("[MainRoutineCollectMail] Debug mode enabled")
    logging.debug("[MainRoutineCollectMail] Start of MainRoutineCollectMail")
    await SubRoutineSetView5(whocallthisfunction)
    await SubRoutineCloseAnyFrame(whocallthisfunction)
    logging.info ("[MainRoutineCollectMail] Interact with Mailbox")
    BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"right", 1, MailboxPositionWindow1X, MailboxPositionWindow1y, 2)
    logging.info ("[MainRoutineCollectMail] Click - 'OPEN ALL MAIL' TSM Addon Button")
    BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, 615, 350, 2)
    logging.info(f"[MainRoutineCollectMail] Aguardando {TimeWaitCollectMails} Segundos para coletar todos os mails")
    for i in range(TimeWaitCollectMails, 0, -1):
        await asyncio.sleep(1)
        if i % 10 == 0:
            if i != 10 and i !=5 and i !=TimeWaitCollectMails:
                logging.info (f"[MainRoutineCollectMail] Aguardando {i} Segundos para coletar todos os mails")
        if i <= 10:
            logging.info (f"[MainRoutineCollectMail] Aguardando {i} Segundos para coletar todos os mails")


    logging.debug ("[MainRoutineCollectMail] End of MainRoutineCollectMail")

async def MainRoutinePostAuctions():
    whocallthisfunction = "MainRoutinePostAuctions"
    TimeWaitPostScan = config.getint('MainRoutinePostAuctions', 'TimeWaitPostScan')
    TimeKeepPressingTSMPostCancelButtonForPost = config.getint('MainRoutinePostAuctions', 'TimeKeepPressingTSMPostCancelButtonForPost')
    logging.info("[MainRoutinePostAuctions] Post Auctions Main Routine")
    logging.debug ("[MainRoutinePostAuctions] Debug mode enabled")
    logging.debug ("[MainRoutinePostAuctions] Start of MainRoutinePostAuctions")
    await SubRoutineSetView5(whocallthisfunction)
    await SubRoutineCloseAnyFrame(whocallthisfunction)
    await SubRoutineInteractAhNpc(whocallthisfunction)
    await asyncio.sleep(2)
    logging.info ("[MainRoutinePostAuctions] Click TSM 'Auctioning' tab")
    BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, 170, 20, 2)
    logging.info ("[MainRoutinePostAuctions] Click TSM 'Run Post Scan' button")
    BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, 110, 290, 2)
    # Fase TimeWaitCancelScan
    logging.info (f"[MainRoutinePostAuctions] Aguardando {TimeWaitPostScan} segundos pelo o PostScan")
    for i in range(TimeWaitPostScan, 0, -1):
        await asyncio.sleep(1)
        if i % 5 == 0:
            if i != 10 and i !=5 and i !=TimeWaitPostScan:
                    logging.info (f"[MainRoutinePostAuctions] Aguardando {i} segundos pelo o PostScan")
        if i <= 10:
            logging.info (f"[MainRoutinePostAuctions] Aguardando {i} segundos pelo o PostScan")
    # Fase TimeKeepPressingTSMPostCancelButtonForCancel
    logging.info (f"[MainRoutinePostAuctions] Pressionando o botão TSM Post/Cancel Button por {TimeKeepPressingTSMPostCancelButtonForPost} segundos")
    for i in range(TimeKeepPressingTSMPostCancelButtonForPost, 0, -1):
        await SubRoutineTsmPostCancelButton()
        if i % 10 == 0:
            if i != 10 and i !=5 and i !=TimeKeepPressingTSMPostCancelButtonForPost:
                logging.info (f"[MainRoutinePostAuctions] Pressionando o botão TSM Post/Cancel por mais {i} segundos")
        if i <= 10:
            logging.info (f"[MainRoutinePostAuctions] Pressionando o botão TSM Post/Cancel por mais {i} segundos")
    logging.debug (f"[MainRoutinePostAuctions] End of MainRoutinePostAuctions")

async def MainRoutineCancelScanAuctions():
    whocallthisfunction = "MainRoutineCancelScanAuctions"
    TimeWaitCancelScan = config.getint('MainRoutineCancelScanAuctions', 'TimeWaitCancelScan')
    TimeKeepPressingTSMPostCancelButtonForCancel = config.getint('MainRoutineCancelScanAuctions', 'TimeKeepPressingTSMPostCancelButtonForCancel')
    logging.debug ("[MainRoutineCancelScanAuctions] Debug mode enabled")
    logging.debug ("[MainRoutineCancelScanAuctions] Start of MainRoutineCancelScanAuctions")
    await SubRoutineSetView5(whocallthisfunction)
    await SubRoutineCloseAnyFrame(whocallthisfunction)
    await SubRoutineInteractAhNpc(whocallthisfunction)
    await asyncio.sleep(2)
    logging.info ("[MainRoutineCancelScanAuctions] Click TSM 'Auctioning' tab")
    BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, 170, 20, 2)
    logging.info ("[MainRoutineCancelScanAuctions] Click TSM 'Run Cancel Scan' button")
    BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction,"left", 1, 110, 320, 2)
    # Fase TimeWaitCancelScan
    logging.info (f"[MainRoutineCancelScanAuctions] Esperando {TimeWaitCancelScan} segundos para o CancelScan")
    for i in range(TimeWaitCancelScan, 0, -1):
        await asyncio.sleep(1)
        if i % 10 == 0:
            if i != 10 and i !=5 and i !=TimeWaitCancelScan:
                logging.info (f"[MainRoutineCancelScanAuctions] Restam {i} segundos para o CancelScan")
        if i <= 10:
            logging.info (f"[MainRoutineCancelScanAuctions] Restam {i} segundos para o CancelScan")
    # Fase TimeKeepPressingTSMPostCancelButtonForCancel
    logging.info (f"[MainRoutineCancelScanAuctions] Pressionando o botão TSM Post/Cancel Button por {TimeKeepPressingTSMPostCancelButtonForCancel} segundos")
    for i in range(TimeKeepPressingTSMPostCancelButtonForCancel, 0, -1):
        await SubRoutineTsmPostCancelButton(whocallthisfunction)
        if i % 10 == 0:
                if i != 10 and i !=5 and i !=TimeWaitCancelScan:
                    logging.info (f"[MainRoutineCancelScanAuctions] Restam {i} segundos para pressionar o botão TSM Post/Cancel")
        if i <= 10:
            logging.info (f"[MainRoutineCancelScanAuctions] Restam {i} segundos para pressionar o botão TSM Post/Cancel")
    logging.debug ("[MainRoutineCancelScanAuctions] End of MainRoutineCancelScanAuctions")

async def testlog():
    logging.debug("Log Test - DEBUG")
    logging.info("Log Test - INFO")
    logging.warning("Log Test - WARNING")
    logging.error("Log Test - ERROR")
    logging.critical("Log Test - CRITICAL")