import logging
from context_vars import user_context

log_format = "%(asctime)s %(name)s %(levelname)s:\tuser: %(user)s: %(messsage)s"

#커스텀 포매터
class CustomFormatter(logging.Formatter):
    def format(self, recode):
        if not hasattr(recode, "user"):
            recode.user = "Anonymous"
        return super().format(recode)
    
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter(log_format))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.user = str(user_context.get())
        return True
    
logger.addFilter(ContextFilter())