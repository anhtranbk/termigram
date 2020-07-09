import logging
import asyncio
import sys
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.custom.dialog import Dialog
from colorama import Fore, Back, Style, init
from termcolor import colored


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 1597636
api_hash = '5179b37ec805d06a52d1d2144585e0a9'
client = TelegramClient('anon', api_id, api_hash)


class StdinReader:
    """
    Start monitoring the fd file descriptor for read availability and 
    invoke callback with the specified arguments once fd is available for reading.
    """
    def __init__(self, loop: asyncio.BaseEventLoop):
        self.loop: asyncio.BaseEventLoop = loop

    def start(self, callback):
        self.loop.add_reader(sys.stdin, self.got_stdin_data, callback)

    def stop(self):
        self.loop.remove_reader(sys.stdin)

    def got_stdin_data(self, callback):
        self.loop.create_task(callback(sys.stdin.readline().strip()))


class TermigramError(Exception):
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return str(self.error)


class Termigram:

    def __init__(self, client):
        self.participants = dict()
        self.dialog: Dialog = None
        self.client: TelegramClient = client

        self.client.add_event_handler(self.on_new_message, events.NewMessage)
        self.client.add_event_handler(self.on_user_update, events.UserUpdate)

    def run_forever(self):
        stdin = StdinReader(self.client.loop)
        stdin.start(self.stdin_event_handler)
        self.next_line()

        # The first parameter is the .session file name (absolute paths allowed)
        with self.client:
            # self.client.loop.run_until_complete()
            self.client.run_until_disconnected()

        stdin.stop()

    async def on_new_message(self, event):
        if not self.dialog or self.dialog.entity.id != abs(event.chat_id):
            return
        username = self.participants.get(event.from_id)
        if not username: 
            sender = await event.get_sender()
            username = self.parse_username(sender)
            self.participants[sender.id] = username
        self.print_message(event.date, username, event.text)

    async def on_user_update(self, event):
        pass

    async def stdin_event_handler(self, text: str):
        if not text:
            self.next_line()
        elif text.startswith(':'):
            await self.handle_command(text)
        else:
            await self.send_message(text)

    async def send_message(self, text):
        if not self.dialog:
            self.print_error('You must join a conversation before sending a message')
            return
        await self.dialog.send_message(text)
        self.next_line()

    async def handle_command(self, cmd: str):
        try:
            if cmd.startswith(':join'):
                idx = cmd.find(' ')
                if idx < 0:
                    raise TermigramError('Command malformed')
                await self.join_conv(cmd[idx+1:])
            elif cmd == ':conv_list':
                async for dialog in client.iter_dialogs():
                    print(dialog.title)
                self.next_line()
            elif cmd == ':help':
                self.print_info("""List commands:
                :conv_list:         Print all open conversations/subscribed channels
                :join <conv_name>:  Join into a conversation
                :events [on/off]:   Turn on/off event listener when a new message arrives, 
                                    when a member joins, when someone starts typing, etc
                """)
            elif cmd == ':quit':
                sys.exit(0)
            else:
                raise TermigramError('Command not found')
        except Exception as e:
            self.print_error(e)

    async def join_conv(self, conv):
        self.dialog = None
        async for dialog in client.iter_dialogs():
            if conv == dialog.title:
                self.dialog = dialog
                self.print_info('Joined to {}'.format(self.dialog.title))
                break
        if not self.dialog:
            raise ValueError('Conversation name does not exist')

        chat = self.dialog.entity
        async for user in client.iter_participants(chat):
            self.participants[user.id] = self.parse_username(user).strip()

    def print_message(self, dt, sender, text):
        # [22:58]  Mãi là anh em (MLAE Corp) KhanhTN F9 >>> sample message
        print('\r[{}] {} {} >>> {}'.format(
            dt.strftime('%H:%M'), 
            colored(self.dialog.name, 'yellow') \
                if self.dialog.is_group or self.dialog.is_channel else '', 
            colored(sender, 'magenta'), 
            colored(text, 'green')
        ))
        self.next_line()

    def print_info(self, info):
        print(info)
        self.next_line()

    def print_error(self, error):
        print(colored('FAIL: ' + str(error), 'red'))
        self.next_line()

    def next_line(self):
        msg = '{} >>> '.format(self.dialog.title) if self.dialog else '>>> '
        print(msg, end='', flush=True)

    @staticmethod
    def parse_username(user):
        fname = user.first_name or ''
        lname = user.last_name or ''
        return fname + ' ' + lname


if __name__ == '__main__':
    app = Termigram(client)
    app.run_forever()
