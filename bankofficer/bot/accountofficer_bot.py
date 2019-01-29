# This code should be used with balebot 1.3.9
# The latest balebot have some bug

import sys
import asyncio
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from khayyam import JalaliDatetime
from balebot.updater import Updater
from balebot.models.messages import TextMessage
from balebot.models.base_models import Peer
from balebot.models.constants.peer_type import PeerType
from balebot.utils.logger import Logger

from bankofficer.models import BaseModel, BotUser
from bankofficer.bot.helpers import success_sending_message,\
    failure_send_message
from bankofficer.mimetype import MimeType
from bankofficer.config import BotConfig
from bankofficer.bot.constants import ConstantMessage
from bankofficer import MAIN_DIRECTORY
from bankofficer.create_report import create_report


supported_users = BotConfig.supported_users
file_path = '{}/data/vip_report.xlsx'.format(MAIN_DIRECTORY)
loop = asyncio.get_event_loop()
updater = Updater(token=BotConfig.token, loop=loop)
dispatcher = updater.dispatcher
engine = create_engine('sqlite:///{}'.format(BotConfig.database_url),)
BaseModel.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
bot = updater.dispatcher.bot
send_flag = False
logger = Logger().get_logger()


def send_time():
    return (datetime.datetime.now().hour == BotConfig.sending_hour and \
            datetime.datetime.now().minute == BotConfig.sending_minute)


def report_time():
    return (datetime.datetime.now().hour == BotConfig.report_hour and \
            datetime.datetime.now().minute == BotConfig.report_minute)


def get_peers(users):
    return [Peer(
        peer_type=PeerType.user,
        peer_id=user.peer_id,
        access_hash=user.access_hash,
    ) for user in users]


@dispatcher.command_handler(['/start'])
def start_app(bot, update):
    user_peer = update.get_effective_user()
    kwargs = {
        'update': update,
        'user_id': user_peer.peer_id,
        'step': sys._getframe().f_code.co_name
    }
    if user_peer.peer_id in supported_users:
        bot.send_message(
            TextMessage(ConstantMessage.start_message),
            user_peer, success_callback=success_sending_message,
            failure_callback=failure_send_message,
            **kwargs
        )
        if not BotUser.is_exist(session, user_peer.peer_id):
            user = BotUser(
                peer_id=user_peer.peer_id,
                access_hash=user_peer.access_hash
            )
            session.add(user)
            session.commit()
    else:
        bot.send_message(
            TextMessage(ConstantMessage.not_registered_message),
            user_peer,
            success_callback=success_sending_message,
            failure_callback=failure_send_message,
            **kwargs
        )


@dispatcher.command_handler(['/end'])
def terminate_app(bot, update):
    user_peer = update.get_effective_user()
    kwargs = {
        'user_id': user_peer.peer_id,
        'step': sys._getframe().f_code.co_name
    }
    bot.send_message(
        TextMessage(ConstantMessage.terminate_message),
        user_peer, success_callback=success_sending_message,
        failure_callback=failure_send_message,
        **kwargs
    )
    BotUser.delete_user(user_peer.peer_id, session)


def send_report():
    global send_flag
    users = session.query(BotUser).all()
    peers_list = get_peers(users)
    logger.info(BotConfig.sending_hour)
    logger.info(BotConfig.sending_minute)
    logger.info(str(datetime.datetime.today()))
    jalali = JalaliDatetime.now()
    if report_time() and not send_flag:
        create_report(loop)
        send_flag = True

    if len(users) > 0:
        logger.info('send_time:{}, flag:{}'.format(send_time(), send_flag))
        if send_time() and send_flag:
            for peer in peers_list:
                kwargs = {
                    'user_id': peer.peer_id,
                    'step': sys._getframe().f_code.co_name
                }
                bot.send_document(
                    peer,
                    doc_file=file_path,
                    mime_type=MimeType.xlsx,
                    file_type='file',
                    name=str(jalali.year) + '-' + str(jalali.month) + '-' + \
                        str(jalali.day) + '-Report.xlsx',
                    caption_text='report',
                    success_callback=success_sending_message,
                    failure_callback=failure_send_message,
                    **kwargs
                )
            send_flag = False
            loop.call_later(60, send_report)
        else:
            loop.call_later(30, send_report)


loop.call_soon(send_report)
updater.run()
