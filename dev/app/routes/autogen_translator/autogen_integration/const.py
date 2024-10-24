# -*- coding: utf-8 -*-
"""Constant values used in our nested group chats."""

import os

# General
SYS_MSG = "sys_msg"
DESC = "description"
ALLOWED = "allowed"
DISALLOWED = "disallowed"
NEVER = "NEVER"
ALWAYS = "ALWAYS"
OPENAI_API_VERSION = "2023-05-15"
MESSAGE_SENT = "MESSAGE_SENT"
WAIT_FOR_USER = "WAIT_FOR_USER"

# Websurfer
VIEWPORTAL_SIZE = 10000

# Email setup
AUDIO = os.path.abspath(
    "./dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/audio/audio.mp3"
)
MAIL_IMAGE_PATH_LOGO = os.path.abspath(
    "./dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/mail_img/watsonx.png"
)
MAIL_IMAGE_PATH_FOOTER = os.path.abspath(
    "./dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/mail_img/ibm_logo.png"
)
SENDER = "ibm.consulting.assistant@example.com"
