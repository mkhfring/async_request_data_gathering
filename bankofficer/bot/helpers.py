from datetime import datetime
from balebot.utils.logger import Logger


logger = Logger().get_logger()


def success_sending_message(response, user_data):
    step = user_data['step'] if 'step' in user_data.keys() \
        else user_data['kwargs']['step']
    user_id = user_data['user_id'] if 'user_id' in user_data.keys() \
        else user_data['kwargs']['user_id']

    logger.info(
        'Message was sent from {} was successful'.format(step),
        extra={'user_id': user_id, 'step': step, 'time0': datetime.now()}
    )


def failure_send_message(response, user_data):
    step = user_data['step'] if 'step' in user_data.keys() \
        else user_data['kwargs']['step']
    user_id = user_data['user_id'] if 'user_id' in user_data.keys() \
        else user_data['kwargs']['user_id']

    logger.info(
        'Message from {} was failed'.format(step),
        extra={'user_id': user_id, 'step': step, 'time0': datetime.now()}
    )
