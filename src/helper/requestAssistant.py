
import os
import random
import numpy as np
from os.path import join, dirname

class RequestHeaderGenerator:
    """
    RequestHeaderGenerator
    It generates a random request header: a random user agent and language.
    User agents are taken from
    > https://udger.com/resources/ua-list
    """

    def __init__(self):
        self.userAgentFile = join(dirname(__file__), 'files/userAgentList.txt')
        self.langCodes = ['en-US,en', 'de-DE,de', 'en-GB,en', 'fr-FR,fr']

    def _buildRequestHeader(self, ua, lang):
        return {
            'User-Agent': ua,
            'accept-encoding': 'gzip, deflate, br',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': lang + ';q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache'
        }

    def getRandomLang(self):
        random.shuffle(self.langCodes)
        return self.langCodes[0]

    def getRandomUserAgent(self):
        randomUA = ""
        try:
            with open(self.userAgentFile) as f:
                lines = f.readlines()
                if len(lines) > 0:
                    prng = np.random.RandomState()
                    index = prng.permutation(len(lines) - 1)
                    idx = np.asarray(index, dtype=np.integer)[0]
                    randomUA = lines[int(idx)]
        except Exception as err:
            print('Exception in getRandomUserAgent')
            print(str(err))
        finally:
            return randomUA

    def getRandomRequestHeader (self):
        randomUA = self.getRandomUserAgent()
        randomLang = self.getRandomLang()
        return self._buildRequestHeader(randomUA.replace("\n", ""), randomLang)
