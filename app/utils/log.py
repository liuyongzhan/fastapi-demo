from inspect import getframeinfo, stack

from fastapi.logger import logger


class Logger(object):

    def __init__(self):
        pass

    def generate_msg(self, caller, region, user_name, action, msg, **kwargs):
        m = {"file_name": caller.filename.split("/")[-1],
             "line_num": caller.lineno,
             "region": region,
             "user_name": user_name,
             "action": action,
             "msg": msg,
             "resource": kwargs}
        message = "[{file_name}:{line_num}] [{region}]-[{user_name}]-[{action}]-[{msg}]-[{resource}]".format(**m)
        return message

    def debug(self, region, user_name, action, msg, **kwargs):
        caller = getframeinfo(stack()[1][0])
        message = self.generate_msg(caller, region, user_name, action, msg, **kwargs)
        logger.debug(message)

    def info(self, region, user_name, action, msg, **kwargs):
        caller = getframeinfo(stack()[1][0])
        message = self.generate_msg(caller, region, user_name, action, msg, **kwargs)
        logger.info(message)

    def error(self, region, user_name, action, msg, **kwargs):
        caller = getframeinfo(stack()[1][0])
        message = self.generate_msg(caller, region, user_name, action, msg, **kwargs)
        logger.error(message)

    def warning(self, region, user_name, action, msg, **kwargs):
        caller = getframeinfo(stack()[1][0])
        message = self.generate_msg(caller, region, user_name, action, msg, **kwargs)
        logger.warning(message)