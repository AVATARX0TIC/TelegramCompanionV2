2.2.0:

    - Remove the custom markdown formatter.
    - Add support for kanging/copying animated stickers
    - Fix the responses not parsing correctly
    - Add `remind` and `remindme` commands to send reminders to yourself or chats
    - Add some old commands like `upload`, `disconnect`, `logout`, `mute` and `packinfo`
    - Other bug fixes


2.1.2:

    - Add heroku support for the plugin manager. Read https://github.com/nitanmarcel/TelegramCompanionV2#plugins
    - Add `admin` command to get a chat's admins!
    - Add back the global notes module
    - Add private lockables
    - Other bug fixes!

2.0.2:

    - Don't let CommandHandler args propagate to different events (by @YouTwitFace)
    - Add back the plugin manager functionality. Also all the plugins on https://github.com/nitanmarcel/TgCompanionPlugins have been updated to work on the new version!

2.0.1:
    
    - Add back anti-spam feature for private messages
    - Add workaround for users spamming each others with anti spam messages!
    - Set a custom anti spam message using the 'setpm' command!
    - Add fully woking Non-SQL MODE

2.0.0:
    
    - Rework the code to use lesser API requests
    - Bug fixes