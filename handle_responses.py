def handle_responses(message):
    msg_lower = message.lower()

    # for intial testing, I'll get the bot to listen out for specific messages
    listen_list = ['hello bot', 'start game', 'bot die']
    if msg_lower not in listen_list:
        return

    # if we've reached this code, the bot has seen a message it should respond to.
    if msg_lower == 'hello bot':
        return 'Hello user'
    elif msg_lower == 'start game':
        return 'That\'s not implemented yet'
    elif msg_lower == 'bot die':
        return 'no u.'
    else:
        print('somethings gone wrong, we shouldn\'t be here...')
        return 'uh oh'