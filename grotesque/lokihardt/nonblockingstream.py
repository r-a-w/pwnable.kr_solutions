from Queue import Queue
from threading import Thread
import sys

class nonblockingstream:

    def __init__(self, stream, print_stdout=False):
        # stream is the stream your reading from

        self._s=stream
        self._q=Queue()
        self._print=print_stdout
        self._exit=False

        def _fillQueue(stream,queue):
            while(True):
                character=stream.read(1)
                if character:
                    queue.put(character)
                else:
                    pass
                if self._exit:
                    return None

        self._t=Thread(target=_fillQueue, args=(self._s,self._q))
        self._t.daemon=True
        self._t.start()

    def readuntil(self, word, timeout=None):
        data = ''
        fulldata = ''
        letterIndex = 0
        letter = word[0]
        while word != data:
            try:
                character = self._q.get(block=timeout is not None, timeout=timeout)
            except:
                return None
            fulldata+=character
            if self._print:
                sys.stdout.write(character)
            if character == letter:
                data+=character
                letterIndex+=1
                if letterIndex < len(word):
                    letter = word[letterIndex]
            else:
                data = ''
                letterIndex = 0
                letter = word[letterIndex]
        return fulldata

    def readline(self,timeout=None):
        character=''
        data = ''
        while character != '\n':
            try:
                character = self._q.get(block=timeout is not None, timeout=timeout)
                data+=character
            except:
                return ''
            if self._print:
                sys.stdout.write(character)
        return data

    def read(self, n=False):
        #n is number of characters to read
        data=''
        if n is False:
            while(True):
                try:
                    character = self._q.get(block=True, timeout=0.1)
                    data+=character
                except:
                    return data
                if self._print:
                    sys.stdout.write(character)
        else:
            for i in range(0,n):
                try:
                    character = self._q.get(block=True, timeout=0.1)
                    data+=character
                except:
                    return data
                if self._print:
                    sys.stdout.write(character)
            return data


    def close(self):
        self._exit=True
