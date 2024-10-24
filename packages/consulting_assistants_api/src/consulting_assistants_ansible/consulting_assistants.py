# -*- coding: utf-8 -*-
"""
libica ansible module: allows running a prompt flow using the ICAClient from the libica library.

Description: Ansible module for IBM Consulting Assistants Extensions.

Author: Mihai Criveti

"""

from __future__ import annotations

import traceback

from ansible.module_utils._text import to_text  # type: ignore
from ansible.module_utils.basic import AnsibleModule  # type: ignore
# Import the ICAClient from the libica library
from libica import ICAClient


def run_module() -> None:
    """
    Execute an Ansible module that integrates with an ICAClient to handle prompt-based workflows.

    This function sets up the necessary parameters for the ICAClient interaction, processes the execution based on the parameters received, and handles the output or errors accordingly.

    Args:
        None

    Returns:
        None: Exits by calling `exit_json` or `fail_json` on the AnsibleModule instance with appropriate results or error messages.

    Raises:
        Exception: Catches any exceptions that might occur during the execution of the ICAClient prompt flow and logs them through Ansible's fail_json method.

    Note:
        This function is specifically designed to be used within an Ansible environment, leveraging the AnsibleModule class for argument specification and exit handling. It supports check mode to ensure that no changes are made when only the state is to be reported.
    """
    module_args: dict = dict(
        prompt=dict(type="str", required=True),
        model_id_or_name=dict(type="str", required=False, default=None),
        assistant_id=dict(type="str", required=False, default=None),
        collection_id=dict(type="str", required=False, default=None),
        system_prompt=dict(type="str", required=False, default=None),
        parameters=dict(type="dict", required=False, default=None),
        substitution_parameters=dict(type="dict", required=False, default=None),
        refresh_data=dict(type="bool", required=False, default=False),
    )

    result = dict(changed=False, response="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        # In check mode, we should not make any changes but return the current state
        result["msg"] = "Check mode is not supported for this module."
        module.exit_json(**result)

    try:
        client = ICAClient()
        response = client.prompt_flow(
            prompt=module.params["prompt"],
            model_id_or_name=module.params["model_id_or_name"],
            assistant_id=module.params["assistant_id"],
            collection_id=module.params["collection_id"],
            system_prompt=module.params["system_prompt"],
            parameters=module.params["parameters"],
            substitution_parameters=module.params["substitution_parameters"],
            refresh_data=module.params["refresh_data"],
        )
        result["response"] = to_text(response)
        result["changed"] = True  # Assuming the prompt flow execution changes the state
        module.exit_json(**result)
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg=str(e), exception=tb)


def main():
    """Define main entry point for the script when run as a standalone program."""
    run_module()


if __name__ == "__main__":
    main()
