import logging
import datetime
logger = logging.getLogger(__name__)


# class LoggerMiddleware(object):
def LoggerMiddleware(get_response):
# One-time configuration and initialization.
    def middleware(request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
        response = get_response(request)
        logger.warning('\nRequest done by: '+request.user.username)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
