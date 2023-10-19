import random as rand

UPPERCASE = 0x01
LOWERCASE = 0x02
REVERSE = 0x04
SHUFFLE = 0x08
RANDOM = 0x10
    
def uppercase(message:str) -> str:
    return message.upper()


def lowercase(message:str) -> str:
    return message.lower()


def reverse(message:str) -> str:
    return message[::-1]


def shuffle(message:str) -> str:
    message_list = list(message)
    rand.shuffle(message_list)
    return ''.join(message_list)


def random(message:str) -> str:
    def discard():
        return rand.choices([True, False], weights=[1, 5])[0]

    def repeat(char):
        should_repeat = rand.choices([True, False], weights=[1, 5])[0]

        if should_repeat:
            repeat_amount = int(rand.paretovariate(1))
            return char * repeat_amount
        else:
            return char

    transformed_text = [repeat(c) for c in message if not discard()]

    if len(transformed_text) == 0:
        transformed_text = message[0]

    return "".join(transformed_text)