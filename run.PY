import asyncio
import logging
from routines.MainRoutines import MainRoutineCollectMail, MainRoutineCancelScanAuctions, MainRoutinePostAuctions
from routines.SubRoutines import SubRoutineAntiAfk
from routines.utils.log_setup import setup_logging, LogLevel

logging.info("-------------------------------------------------------")
logging.info("")
logging.info("")
logging.info("###################################")
logging.info("###################################")
logging.info("######### START EXECUTION #########")
logging.info("###################################")
logging.info("###################################")
logging.info("")
logging.info("")

async def anti_afk_loop():
    while True:
        try:
            result = await SubRoutineAntiAfk()
            if not result:
                return
            await asyncio.sleep(300)
        except KeyboardInterrupt:
            logging.info("Loop anti-afk interrompido pelo usuário")
            break

async def auctioning_loop():
    while True:
        try:
            logging.info("-----------------------------------")
            logging.info("Next: MainRoutineCollectMail")
            logging.info("-----------------------------------")
            result = await MainRoutineCollectMail()
            if not result:
                return
            logging.info("-----------------------------------")
            logging.info("Next: MainRoutineCancelScanAuctions")
            logging.info("-----------------------------------")
            result = await MainRoutineCancelScanAuctions()
            if not result:
                return
            logging.info("-----------------------------------")
            logging.info("Next: MainRoutineCollectMail")
            logging.info("-----------------------------------")
            result = await MainRoutineCollectMail()
            if not result:
                return
            logging.info("-----------------------------------")
            logging.info("Next: MainRoutinePostAuctions")
            logging.info("-----------------------------------")
            result = await MainRoutinePostAuctions()
            if not result:
                return
            logging.info("-----------------------------------")
            logging.info("Next: Routines complete, lets wait 60 seconds to restart routines")
            logging.info("-----------------------------------")            
            await asyncio.sleep(60)
        except KeyboardInterrupt:
            logging.info("Loop de leilões interrompido pelo usuário")
            logging.info("-----------------------------------")
            logging.info("-----------------------------------")
            logging.info("-----------------------------------")
            logging.info("-----------------------------------")
            logging.info("-----------------------------------")
            logging.info("-----------------------------------")
            break


async def main():
    try:
        afk_task = asyncio.create_task(anti_afk_loop())
        auctioning_task = asyncio.create_task(auctioning_loop())
        await asyncio.gather(afk_task, auctioning_task)
    except KeyboardInterrupt:
        logging.info("Script interrompido pelo usuário")

asyncio.run(main())

logging.info("")
logging.info("")
logging.info("###################################")
logging.info("###################################")
logging.info("########## END EXECUTION ##########")
logging.info("###################################")
logging.info("###################################")
logging.info("")
logging.info("")