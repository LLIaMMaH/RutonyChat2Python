from mcrcon import MCRcon
from utils.loader import RCON_HOST, RCON_PORT, RCON_PASSWORD
from utils.logger import log_event

def send_rcon_command(command):
    """Отправляет команду на сервер Minecraft через RCON."""
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            response = mcr.command(command)
            log_event(f"Отправлена команда: {command} | Ответ: {response}")
            return response
    except Exception as e:
        log_event(f"Ошибка отправки RCON команды: {e}", "error")
        return None
