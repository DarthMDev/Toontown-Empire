import random
class ChatGarbler(object):
    def __init__(self, messages):
        self.messages = messages

    def garble(self, avatar, numwords):
        new_message = ''

        if avatar.style:
            avatartype = avatar.style.getType()
            wordlist = self.messages[avatartype if avatartype in self.messages else 'default']

        for i in xrange(1, numwords + 1):
            wordindex = random.randint(0, len(wordlist) - 1)
            new_message = new_message + wordlist[wordindex]

            if i < numwords:
                new_message = new_message + ' '

        return '\x01WLDisplay\x01%s\x02' % new_message
