Terrmigram
========
.. epigraph::

  ⭐️ A simple but effective **Terminal-styled Telegram client**. Thanks million for starring and contributing. Hope you enjoy it!

**Termigram** is a Telegram clients for the Linux command line, mainly based on Telethon_ which is an asyncio_ **Python 3** MTProto_ library to interact with Telegram_'s API.

Demo
-------------

![demo](https://raw.githubusercontent.com/tjeubaoit/termigram/master/termigram_demo.gif)

What is this?
-------------

Telegram_ is a cloud-based instant messaging service, that allows users to send multimedia messages and make voice and video calls. **Termigram** is created to help you keep up with your friends on Telegram without leaving the terminal. It lets you interact with your Telegram account in a number of ways, including reading and sending messages, as well as viewing a list of your conversations and joining them with just one line of code. On top of that, this command-line client is fast, and its interface is generally quite clean.


Installing
----------

.. code-block:: sh

  pip3 install -r requirements.txt


Important
-----------------

In order to use **Termigram**, you need to get your own **api_id** and
**api_hash** from https://my.telegram.org, under API Development and then edit these lines in **termigram.py** to make things work!

.. code-block:: python

    api_id = 12345
    api_hash = '0123456789abcdef0123456789abcdef'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()


Next steps
----------

More cool features are expected to be released soon along with an in-depth explanation, with examples, troubleshooting issues, and more useful information.

.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _MTProto: https://core.telegram.org/mtproto
.. _Telegram: https://telegram.org
.. _Telethon: https://github.com/LonamiWebs/Telethon




