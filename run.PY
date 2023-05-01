import asyncio
import logging
import time
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
logging.info("######### STARTING IN #############")
logging.info("######### 10 SECONDS ##############")
logging.info("###################################")
logging.info("")
logging.info("")
time.sleep(10)

async def anti_afk_loop():
    while True:
        try:
            result = await SubRoutineAntiAfk()
            if not result:
                return
            await asyncio.sleep(480)
        except KeyboardInterrupt:
            logging.info("Anti-AFK loop interrupted by user ")
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
            logging.info("Next: Routines complete, lets wait 4 MINUTES to restart routines")
            logging.info("-----------------------------------")            
            await asyncio.sleep(240)
        except KeyboardInterrupt:
            logging.info("Auctions loop interrupted by user")
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
        logging.info("Script interrupted by user")

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