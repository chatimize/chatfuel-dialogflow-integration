class FromChatfuelDTO:
    user_id: int
    language_code: str
    input_text: str

    def __init__(self, user_id, language_code, input_text):
        self.user_id = user_id
        self.language_code = language_code
        self.input_text = input_text

class ToChatfuelDTO:
    token: str
    user_id: int
    bot_id: int
    block_name: str
    chatfuel_message_tag: str
    user_attribute: str

    def __init__(self, token, user_id, bot_id, block_name, chatfuel_message_tag, user_attribute):
        self.token = token
        self.user_id = user_id
        self.bot_id = bot_id
        self.block_name = block_name
        self.chatfuel_message_tag = chatfuel_message_tag
        self.user_attribute = user_attribute
