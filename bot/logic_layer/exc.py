class BotLogicError(Exception):
    """Base exception for bot system errors"""

    pass


class GPTConnectionError(BotLogicError):
    """aiohttp.ClientError wrapper"""

    pass


class UserHasNotCompanionError(BotLogicError):
    """
    Will be raised if user doesn't change companion
    before sending messages
    """

    pass
