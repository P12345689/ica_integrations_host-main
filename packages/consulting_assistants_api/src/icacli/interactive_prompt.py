# -*- coding: utf-8 -*-
"""
icacli interactive.

Description: IBM Consulting Assistants Extensions API - Interactive REPL CLI

Authors: Mihai Criveti
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Tuple

from libica import ICAClient, Settings
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from rich import print  # pylint: disable=redefined-builtin
from rich.console import Console
from rich.markdown import Markdown

# --------------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------

# Render markdown output
RENDER_MARKDOWN_OUTPUT = False


# Define the style for the prompt
style = Style.from_dict(
    {
        "prompt": "bold",
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


# --------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------

# Configure a console object
console = Console()

# Configure settings
settings = Settings()


# --------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------
def list_and_choose(options_func: Callable[..., Any], display_attr: str, id_attr: str) -> Tuple[str, str]:
    """
    Presents a list of options to the user and allows them to choose one.

    Args:
        options_func (Callable[..., Any]): A callable that when called returns a list of options to choose from.
        display_attr (str): The attribute of the options to display to the user.
        id_attr (str): The attribute of the options that uniquely identifies them.

    Returns:
        Tuple[str, str]: A tuple containing the display value and the identifier of the chosen option.

    Examples:
        >>> def options_func():
        ...     return [{'id': '1', 'name': 'Option 1'}, {'id': '2', 'name': 'Option 2'}]
        ...
        >>> list_and_choose(options_func, 'name', 'id')  # doctest: +SKIP
        This will print:
        1. Option 1
        2. Option 2
        and wait for user input. Assuming the user enters '1', the function will return:
        ('1', 'Option 1')

    Note:
        This function involves user interaction and hence cannot be fully tested using doctest.
    """
    while True:
        response = options_func()
        options = response.get("collections", []) if isinstance(response, dict) else response
        if "error" in options:
            print(f"[red]Error fetching data: {options['error']}")
            return ("", "")
        options_list = options if isinstance(options, list) else []
        for idx, option in enumerate(options_list, start=1):
            print(f"{idx}. {option.get(display_attr, 'Unnamed')}")
        choice = input("Choose by number (or 'cancel' to return): ").strip().lower()
        if choice == "cancel":
            return ("", "")
        if not choice.isdigit() or not 0 < int(choice) <= len(options_list):
            print("[orange]Invalid choice. Please enter a valid number or 'cancel'.")
            continue
        chosen_option = options_list[int(choice) - 1]
        return (chosen_option.get(id_attr), chosen_option.get(display_attr))


def list_and_choose_model(client: ICAClient) -> Tuple[str, str]:
    """
    List available models and allows the user to choose one.

    Args:
        client (ICAClient): An instance of ICAClient to retrieve models.

    Returns:
        Tuple[str, str]: A tuple containing the name and the identifier of the chosen model.

    Example:
        >>> client = ICAClient()
        >>> list_and_choose_model(client)  # doctest: +SKIP
        This will print a list of models and wait for user input. Assuming the user enters '1',
        the function will return the ID and name of the first model.

    Note:
        This function involves user interaction and hence cannot be fully tested using doctest.
    """
    models = client.get_models()
    if "error" in models:
        print(f"[red]Error fetching models: {models}")
        return ("", "")
    model_list = models if isinstance(models, list) else []
    for idx, model in enumerate(model_list, start=1):
        print(f"{idx}. {model.get('name', 'Unnamed Model')} - ID: {model.get('id', 'N/A')}")
    model_choice = input("Choose a model by number (or 'cancel' to return): ").strip().lower()
    if model_choice == "cancel":
        return ("", "")
    if not model_choice.isdigit() or not 0 < int(model_choice) <= len(model_list):
        print("[orange]Invalid choice. Please enter a valid number or 'cancel'.")
        return ("", "")
    chosen_model = model_list[int(model_choice) - 1]
    return (chosen_model.get("id", ""), chosen_model.get("name", ""))


def print_help() -> None:
    """
    Print the help message for the interactive prompt.

    Example:
        >>> print_help()  # doctest: +NORMALIZE_WHITESPACE
        ░▀█▀░█▀▄░█▄█░░░█▀▀░█▀█░█▀█░█▀▀░█░█░█░░░▀█▀░▀█▀░█▀█░█▀▀
        ░░█░░█▀▄░█░█░░░█░░░█░█░█░█░▀▀█░█░█░█░░░░█░░░█░░█░█░█░█
        ░▀▀▀░▀▀░░▀░▀░░░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀
            ░█▀█░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀█░█▀█░▀█▀░█▀▀
            ░█▀█░▀▀█░▀▀█░░█░░▀▀█░░█░░█▀█░█░█░░█░░▀▀█
            ░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀
        Interactive CLI commands:
        /quit - Exit the interactive CLI.
        /file <file> - Add a text file to the chat for editing.
        /help - Display this help message.
        /model - Change to a different model with tab completion.
        /collection - Change to a different collection.
        /assistant - Change to a different assistant.
    """
    help_text = (
        "░▀█▀░█▀▄░█▄█░░░█▀▀░█▀█░█▀█░█▀▀░█░█░█░░░▀█▀░▀█▀░█▀█░█▀▀\n"
        "░░█░░█▀▄░█░█░░░█░░░█░█░█░█░▀▀█░█░█░█░░░░█░░░█░░█░█░█░█\n"
        "░▀▀▀░▀▀░░▀░▀░░░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀\n"
        "      ░█▀█░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀█░█▀█░▀█▀░█▀▀\n"
        "      ░█▀█░▀▀█░▀▀█░░█░░▀▀█░░█░░█▀█░█░█░░█░░▀▀█\n"
        "      ░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀░▀░░▀░░▀▀▀\n"
        "Interactive CLI commands:\n"
        "/quit - Exit the interactive CLI.\n"
        "/file <file> - Add a text file to the chat for editing.\n"
        "/help - Display this help message.\n"
        "/model - Change to a different model with tab completion.\n"
        "/collection - Change to a different collection.\n"
        "/assistant - Change to a different assistant.\n"
    )
    console.print(help_text)


def change_context(args: Any, context_type: str, value: Tuple[str, str] = ("", "")) -> None:
    """
    Change the context of the interactive prompt session.

    Args:
        args (Any): The arguments passed to the interactive prompt.
        context_type (str): The type of context to change (e.g., 'model', 'assistant').
        value (Tuple[str, str], optional): A tuple containing the display value and the identifier of the context item. Defaults to None.

    Example:
        Assuming 'args' is an object with attributes 'model_id_or_name' and 'assistant_id':

        >>> change_context(args, 'model', ('1', 'Model 1')) # doctest: +SKIP
        This will set 'args.model_id_or_name' to '1'.

        >>> change_context(args, 'assistant', ('2', 'Assistant 2')) # doctest: +SKIP
        This will set 'args.assistant_id' to '2' and 'args.model_id_or_name' to None.

        >>> change_context(args, 'model') # doctest: +SKIP
        This will set 'args.assistant_id' to '2' and 'args.model_id_or_name' to None.

        >>> change_context(args, 'model') # doctest: +SKIP
        This will print the current model ID and prompt the user to enter a new one.

    Note:
        This function involves user interaction and hence cannot be fully tested using doctest.
    """
    if context_type == "collection_id" and value:
        # Clear other contexts to avoid ValueError when setting collection_id
        setattr(args, "model_id_or_name", None)
        setattr(args, "model_id_or_name_name", None)
        setattr(args, "assistant_id", None)
        setattr(args, "assistant_id_name", None)
        setattr(args, context_type, value[0])
        setattr(args, f"{context_type}_name", value[1])
    elif value:
        # Unset model_id_or_name if assistant_id is being set, and vice versa
        if context_type == "assistant_id":
            setattr(args, "model_id_or_name", None)
            setattr(args, "model_id_or_name_name", None)
        elif context_type == "model_id_or_name":
            setattr(args, "assistant_id", None)
            setattr(args, "assistant_id_name", None)
        setattr(args, context_type, value[0])
        setattr(args, f"{context_type}_name", value[1])
    else:
        print(f"Current {context_type}: {getattr(args, context_type, 'None')}")
        new_value = input(f"Enter new {context_type} ID or name: ").strip()
        setattr(args, context_type, new_value)


class CommandStartCompleter(Completer):
    """
    A custom completer for a command-line interface.

    Provides completions for commands when the input starts specifically with '/' at the start of the prompt.

    Attributes:
        commands (list of str): A list of commands to provide completions for.
    """

    def __init__(self, commands):
        """
        Initialize the completer with a list of commands.

        Args:
            commands (list of str): A list of commands that the completer can autocomplete.
        """
        self.commands = commands

    def get_completions(self, document, complete_event):
        """
        Yield completions based on the current position within the input document.

        This method provides completions only if the cursor is at the start of the text
        and the text starts with '/', ensuring that completions are relevant to command inputs only.

        Args:
            document (Document): The current document state of the input text.
            complete_event (CompleteEvent): An event instance containing information about the completion request.

        Yields:
            Completion: Possible completions at the current cursor position.

        Examples:
            >>> from prompt_toolkit.document import Document
            >>> from prompt_toolkit.completion import CompleteEvent, Completion
            >>> completer = CommandStartCompleter(["/quit", "/help", "/file"])

            >>> doc = Document(text="/", cursor_position=1)
            >>> list(completer.get_completions(doc, CompleteEvent()))
            [Completion(text='/quit', start_position=-1, display=FormattedText([('', '/quit')])), Completion(text='/help', start_position=-1, display=FormattedText([('', '/help')])), Completion(text='/file', start_position=-1, display=FormattedText([('', '/file')]))]

            >>> doc = Document(text="  /", cursor_position=3)  # Not at the start, with leading spaces
            >>> list(completer.get_completions(doc, CompleteEvent()))
            [Completion(text='/quit', start_position=-1, display=FormattedText([('', '/quit')])), Completion(text='/help', start_position=-1, display=FormattedText([('', '/help')])), Completion(text='/file', start_position=-1, display=FormattedText([('', '/file')]))]

            >>> doc = Document(text="/qu", cursor_position=3)
            >>> list(completer.get_completions(doc, CompleteEvent()))
            [Completion(text='/quit', start_position=-3, display=FormattedText([('', '/quit')]))]

            >>> doc = Document(text="Hello /qu", cursor_position=9)  # Not at the start
            >>> list(completer.get_completions(doc, CompleteEvent()))
            []
        """
        text_before_cursor = document.text_before_cursor.lstrip()  # Ignore leading whitespaces
        if text_before_cursor.startswith("/"):
            for command in self.commands:
                if command.startswith(text_before_cursor):
                    yield Completion(command, start_position=-len(text_before_cursor))


def interactive_prompt_flow(client: ICAClient, args: Any) -> None:
    """
    Run main flow of the interactive prompt, handling user input and actions.

    Args:
        client (ICAClient): An instance of ICAClient to interact with the API.
        args (Any): The arguments passed to the interactive prompt.

    Example:
        Assuming 'client' is an instance of ICAClient and 'args' is an object with the necessary attributes:
        >>> client = ICAClient()
        >>> interactive_prompt_flow(client, args) # doctest: +SKIP

    Note:
        This function involves user interaction and hence cannot be fully tested using doctest.
        A separate `pexpect` test is provided in `test/test_interactive_prompt.py`
    """
    # Set default model name for display if not provided
    if not getattr(args, "model_id_or_name", None):
        setattr(args, "model_id_or_name", settings.assistants_default_model_id_or_name)
    if not getattr(args, "model_id_or_name_name", None):
        setattr(args, "model_id_or_name_name", settings.assistants_default_model_id_or_name)

    print_help()
    emojis = {"model_id_or_name": "📄", "assistant_id": "🤖", "collection_id": "📚"}

    # Set up auto-completion
    commands = ["/quit", "/file", "/help", "/model", "/collection", "/assistant"]
    command_completer = CommandStartCompleter(commands)
    session: PromptSession = PromptSession(completer=command_completer, style=style)

    try:
        while True:
            new_model_id = ""
            new_model_name = ""
            new_collection_id = ""
            new_collection_name = ""
            new_assistant_id = ""
            new_assistant_name = ""
            active_context = next((k for k, v in vars(args).items() if v and k in emojis), None)
            active_context_emoji = emojis[active_context] if active_context else ""
            active_context_name = getattr(args, f"{active_context}_name", "None") if active_context else "None"
            prompt = session.prompt(f"\n{active_context_emoji} [{active_context_name}]> ").strip().lower()
            if prompt.startswith("/") and not prompt.startswith("/assistant"):
                # --------------------------------------------------------------------
                # /quit
                # --------------------------------------------------------------------
                if prompt == "/quit":
                    break

                # --------------------------------------------------------------------
                # /file: currently breaks session prompt after usage so only ALT+ENTER works
                # --------------------------------------------------------------------
                if prompt.startswith("/file "):
                    file_path = prompt.split(" ", 1)[1]
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            chat_content = file.read()
                            print(
                                f"File content from {file_path} loaded. Press Alt Enter to continue or edit as needed:"
                            )
                        # Reset the prompt with the file content as the default text for editing or direct submission
                        prompt = session.prompt(
                            f"\n{active_context_emoji} [{active_context_name}]> ",
                            default=str(chat_content).strip(),
                            multiline=True,  # Ensure this is set to handle multiline text input properly
                        )
                    except FileNotFoundError:
                        print(f"[red]Error: File not found - {file_path}")

                # --------------------------------------------------------------------
                # /help
                # --------------------------------------------------------------------
                if prompt == "/help":
                    print_help()

                # --------------------------------------------------------------------
                # /model
                # --------------------------------------------------------------------
                if prompt == "/model":
                    new_model_id, new_model_name = list_and_choose_model(client)
                    if new_model_id:
                        change_context(args, "model_id_or_name", (new_model_id, new_model_name))

                # --------------------------------------------------------------------
                # /collection
                # --------------------------------------------------------------------
                if prompt.startswith("/collection"):
                    new_collection_id, new_collection_name = list_and_choose(
                        lambda: client.get_collections(), "collectionName", "_id"
                    )  # pylint: disable=unnecessary-lambda
                    if new_collection_id:
                        change_context(
                            args,
                            "collection_id",
                            (new_collection_id, new_collection_name),
                        )

                # --------------------------------------------------------------------
                # Unknown command
                # --------------------------------------------------------------------
                if prompt not in ["/quit", "/add ", "/help", "/model", "/collection"]:
                    print("Unknown command. Type '/help' for a list of commands.")
                continue

            # --------------------------------------------------------------------
            # /assistant
            # --------------------------------------------------------------------
            if prompt.startswith("/assistant"):
                while True:
                    tag = session.prompt("Enter a tag for the assistant: ").strip()
                    if tag:
                        break
                    print("Tag cannot be empty. Please enter a valid tag.")
                new_assistant_id, new_assistant_name = list_and_choose(
                    lambda: client.get_assistants(tags=[tag]), "title", "id"
                )  # pylint: disable=unnecessary-lambda
                if new_assistant_id is None:  # This also covers the case when user chooses 'cancel'
                    print("Operation cancelled or invalid choice. Returning to main menu.")
                    continue  # Return to the start of the loop
                if new_assistant_id:
                    change_context(args, "assistant_id", (new_assistant_id, new_assistant_name))
                else:
                    new_model_id, new_model_name = list_and_choose_model(client)
                    if new_model_id:
                        change_context(args, "model_id_or_name", (new_model_id, new_model_name))
                    elif prompt.startswith("/collection"):
                        new_collection_id, new_collection_name = list_and_choose(
                            lambda: client.get_collections(), "collectionName", "_id"
                        )  # pylint: disable=unnecessary-lambda
                    if new_collection_id:  # pyright error: "new_collection_id" is possibly unbound
                        change_context(
                            args,
                            "collection_id",
                            (new_collection_id, new_collection_name),
                        )
                    print("Unknown command. Type '/help' for a list of commands.")
                continue
            if not prompt:
                print("Prompt cannot be empty. Please enter a valid prompt.")
                continue
            prompt_output = client.prompt_flow(
                system_prompt=args.system_prompt,
                model_id_or_name=args.model_id_or_name,
                assistant_id=args.assistant_id,
                collection_id=args.collection_id,
                prompt=prompt,
                parameters=args.parameters,
                substitution_parameters=args.substitution_parameters,
                refresh_data=args.refresh_data,
            )
            if RENDER_MARKDOWN_OUTPUT:
                markdown = Markdown(str(prompt_output).strip())
                console.print(markdown)
            else:
                print(str(prompt_output).strip())
    except (EOFError, KeyboardInterrupt):
        print("\nExiting interactive mode.")
