from yasuo.config import J_PUSH
import jpush
import logging


_jpush = jpush.JPush(J_PUSH['appKey'], J_PUSH['masterSecret'])
push = _jpush.create_push()
# _jpush.set_logging("DEBUG")


def push_message(tags, message, platform=jpush.all_):
    push.audience = jpush.all_ if tags == jpush.all_ else jpush.audience({"tag": tags})
    push.notification = jpush.notification(alert=message)
    push.platform = platform
    try:
        response = push.send()
    except jpush.common.Unauthorized as e:
        logging.error("JPush Unauthorized: %s" % str(e))
    except jpush.common.APIConnectionException as e:
        logging.error("JPushconn error: %s" % str(e))
    except jpush.common.JPushFailure as e:
        logging.error("JPush Failure: %s" % str(e))
    except Exception as e:
        raise e
    else:
        logging.info(response.payload)
        if response.status_code == 200 and response.payload['sendno'] == '0':
            return True
    return False
