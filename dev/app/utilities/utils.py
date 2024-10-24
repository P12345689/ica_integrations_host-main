# -*- coding: utf-8 -*-
import asyncio
import threading
from asyncio import AbstractEventLoop
from typing import Callable


def run_in_background(func: Callable, *args, **kwargs) -> threading.Thread:
    def loop_in_thread(loop: AbstractEventLoop, func: Callable, *args, **kwargs):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func(*args, **kwargs))

    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=loop_in_thread, args=(loop, func, *args), kwargs=kwargs)
    thread.start()
    return thread
