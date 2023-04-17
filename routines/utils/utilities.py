import logging

class CriticalError(Exception):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logging.critical(str(self))
            logging.critical("Erro critico, encerrado aplicação")

