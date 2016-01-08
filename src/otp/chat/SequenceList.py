class SequenceList:

    def __init__(self, wordlist):
        self.list = {}
        for line in wordlist:
            if line is '':
                continue
            split = line.split(':')
            
    def getList(self, word):
        if word in self.list:
            return self.list[word]
        else:
            return []
