import re

from telethon import events

from companion.env_vars import CMD_PREFIX
from inspect import iscoroutinefunction
from companion import CMD_HELP, client

def commandhandler(
        command=None,
        incoming=False,
        prefix=CMD_PREFIX,
        args=None,
        args_delimiter=None,
        func=None,
        parse_mode=None,
        private_lock=False,
        **kwargs):
    """
    Custom decorator around `client.add_event_handler(events.NewMessage(..)`
            Unlike the client.on() decorator or add_event_handler() method it allows you to retrieve a command argument
            with the event and also build a help dict using function's docstring

    :param command: (str) the command used to call the decorated function. default == None
    :param prefix: (optional) (str) the prefix of the command. default == "."
    :param args: (optional) (list) a list with accepted arguments that can be retrieved with `event.args.argument`
    :param args_delimiter: (optional) (str) where should the handler split arguments. default == " "
    :param parse_mode: (optional) (str) chose the parse mode for the specific function. default == None
    :param private_lock: (optional) (boll) true if the command should be blocked in PM
    :return: `event.NewMessage` object with a new `args` attribute holding the CommandArgument object.
    """
    def decorator(f):
        _prefix = re.escape(prefix) if prefix else ""
        if not command:
            _pattern = command
        else:
            _pattern = r"{}\b".format(_prefix + command)
        _generate_help(f, command)

        @client.on(
            events.NewMessage(
                pattern=_pattern,
                incoming=incoming,
                outgoing=not incoming,
                func=func,
                **kwargs))
        async def wrapper(event):
            _args = None
            _is_admin = False
            _is_creator = False
            _admin_rights = None

            if private_lock is True and event.is_private:
                await event.edit("This command was made to be used in groups!")
                return

            if args:
                if isinstance(args, list):
                    _args = CommandArguments()
                    nr_args = 0
                    len_args = len(args)

                    split_text = event.text.split(
                        args_delimiter, maxsplit=len_args)
                    split_text.pop(0)
                    for arg in args:
                        try:
                            setattr(
                                _args,
                                args[nr_args],
                                split_text[nr_args])
                        except IndexError:
                            setattr(_args, args[nr_args], None)
                        nr_args += 1

            event.args = _args

            client.parse_mode = parse_mode
            _call_func = await f(event) if iscoroutinefunction(f) else f(event)
            client.parse_mode = None

        return wrapper
    return decorator

class CommandArguments:
    def __init__(self, *args, **kwargs):
        pass

def _generate_help(f, command):
    global CMD_HELP
    if f.__doc__:
        CMD_HELP.update({command: f.__doc__})