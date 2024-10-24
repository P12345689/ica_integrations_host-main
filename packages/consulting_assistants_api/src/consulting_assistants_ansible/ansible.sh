#!/bin/bash

ansible localhost -m consulting_assistants -a "prompt='Hello, world!' assistant_id='3903'" -M .
ansible-playbook consulting_assistants_playbook.yml
