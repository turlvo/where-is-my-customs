# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)


import json
import re
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse

from bothub_client.bot import BaseBot
from bothub_client.decorators import channel
from bothub_client.messages import Message
from bothub_client.decorators import command

from .utils import find_by_hbl
from .message_templates import HBL_MESSAGE_TEMPLATE


FIND_BY_HBL = "HBL(송장번호)로 찾기"
FIND_BY_MBL = "MBL로 찾기"
FIND_BY_CRG = "화물관리번호로 찾기"
FIND_BUTTONS = [FIND_BY_HBL, FIND_BY_MBL, FIND_BY_CRG]
QUERY_BY_HBL = 'HBL 번호를 입력후 메시지를 전송해주세요.'
NEW_INPUT = '새 값 입력하기'
EXIST_HISTORY = '최근 1주일 내 조회하신 값들이 있습니다. 아래 중 선택하시거나, 혹은 새 값을 입력해주세요.'

class Bot(BaseBot):
    @command('kakao_init_keyboard')
    def init_handler(self, event, context, args):
        msg = Message(event)
        msg.add_keyboard_button(FIND_BY_HBL)
        self.send_message(msg)

    @command('start')
    def telegram_init_handler(self, event, context, args):
        msg = Message(event)
        msg.add_keyboard_button(FIND_BY_HBL)
        self.send_message(msg)

    @channel()
    def default_handler(self, event, context):
        msg = Message(event)
        content = event['content']

        user_data =  UserData(self, self.get_user_data())
        #user_data.clear_history()
        context = user_data.get_state()

        if context == 'IDLE':
          if content == FIND_BY_HBL:
              user_data.set_state('FIND_BY_HBL')
              history = user_data.get_history('HBL')

              if history and len(history) > 0:
                  msg.set_text(EXIST_HISTORY)
                  for item in history:
                      msg.add_keyboard_button(item)
                  msg.add_keyboard_button(NEW_INPUT)
              else:
                  msg.set_text(QUERY_BY_HBL)
            
              self.send_message(msg)
        elif context == 'FIND_BY_HBL':
            if content == NEW_INPUT or content == FIND_BY_HBL:
                msg.set_text(QUERY_BY_HBL)
                self.send_message(msg)
            else :
                try:
                    hbl_no = re.sub(r"\D", "", content)
                    result = find_by_hbl(hbl_no)

                    user_data.set_state('IDLE')
                    user_data.add_history({'type': 'HBL', 'number': hbl_no, 'date': datetime.today().strftime('%Y-%m-%d')})

                    msg.set_text(HBL_MESSAGE_TEMPLATE.format(**result))
                except IndexError as e:
                    user_data.set_state('IDLE')
                    msg.set_text('<{}>이 잘못된 HBL 번호이거나, 혹은 해당 물품은 아직 통관이 시작되지 않았습니다. 확인후 다시 적어주세요.'.format(content))
                finally:
                    msg.add_keyboard_button(FIND_BY_HBL)
                    self.send_message(msg)
        else:
            msg.set_text(QUERY_BY_HBL)
            self.send_message(msg)


class UserData(object):
    def __init__(self, bot, data):
        self.bot = bot
        self.user_data = {}
        self.user_data['state'] = data.get('state') or 'IDLE'
        self.user_data['history'] = data.get('history') or []

    def get_state(self):
        return self.user_data['state']

    def set_state(self, state):
        self.user_data['state'] = state
        self.bot.set_user_data(self.user_data)

    def add_history(self, item):
        if not item in self.user_data['history']:
            self.user_data['history'].append(item)
            self.bot.set_user_data(self.user_data)
    
    def get_history(self, history_type):
        result = []
        until_date = datetime.now() - timedelta(days=7)

        history = self.user_data['history']
        for item in history:
            date = parse(item['date'])
            if item['type'] == history_type and date > until_date:
                result.append(item['number'])
        
        return result

    def clear_history(self):
        self.user_data['history'] = []
        self.bot.set_user_data(self.user_data)

    def toString(self):
        return 'State: {}\nHistory: {}'.format(self.user_data['state'], self.user_data['history'])

      


