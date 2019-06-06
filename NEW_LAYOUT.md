# About the new layout

If you are familiar with the old version you should notice that a lot of things have changed in the V2 Release. Here are more details!

## New CommandHandler decorator

In the old version we import the CommandHandler from client. Now we use `from companion.utils import CommandHandler`. This new command handler has also new arguments:


### Command Handler docstring:

Custom decorator around `client.add_event_handler(events.NewMessage(..)`
        Unlike the client.on() decorator or add_event_handler() method it allows you to retrieve a command argument
        with the event and also build a help dict using function's docstring

- :param command: (str) the command used to call the decorated function. default == None
- :param prefix: (optional) (str) the prefix of the command. default == "."
- :param args: (optional) (list) a list with accepted arguments that can be retrieved with `event.args.argument`
- :param args_delimiter: (optional) (str) where should the handler split arguments. default == " "
- :param parse_mode: (optional) (str) chose the parse mode for the specific function. default == None
- :param private_lock: (optional) (boll) true if the command should be blocked in PM
- :return: `event.NewMessage` object with a new `args` attribute holding the CommandArgument object.

### Calling the client

We also change the way we import the client and use it's method. Instead of importing it from the companion we call it from within the event using: `event.client`

