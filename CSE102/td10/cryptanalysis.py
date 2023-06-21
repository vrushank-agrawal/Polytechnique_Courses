# -*- coding: utf-8 -*-
"""
Created on Tue May  4 15:17:27 2021

@author: Vrushank Agrawal
"""

import sys, os, re, pickle

# --------------------------------------------------------------------
class Freq(object):
    CACHE = '.%s.cache'

    def __init__(self, filename, cache = None):
        if cache is not None:
            self.freqs = self._read_from_cache(filename, cache)

        if self.freqs is not None:
            return

        self.freqs = self._read_from_file(filename)
        self._write_to_cache(cache, self.freqs)

    @classmethod
    def _read_from_cache(cls, filename, cache):
        cachename = cls.CACHE % (cache,)
        if not os.path.exists(cachename):
            return
        if os.path.exists(filename):
            ftime = os.path.getmtime(filename)
            ctime = os.path.getmtime(cachename)
            if ftime > ctime: return
        with open(cachename, 'r+b') as stream:
            return pickle.load(stream)

    @classmethod
    def _write_to_cache(cls, cache, freqs):
        cachename = cls.CACHE % (cache,)
        with open(cachename, 'w+b') as stream:
            pickle.dump(freqs, stream)
        
    @classmethod
    def _read_from_file(cls, filename):
        def _parse(x):
            m = re.search('^([A-Z]+)*\s*(\d+)$', x.strip())
            if m is None: raise ValueError(x)
            return (m.groups()[0], int(m.groups()[1]))

        with open(filename, 'r') as stream:
            freqs = [_parse(x) for x in stream.readlines()]
        count = sum(x[1] for x in freqs)
        return { x[0] : x[1] / count for x in freqs } if count else {}

    def __getitem__(self, x):
        return self.freqs.get(x, 0.)

# --------------------------------------------------------------------
# Uncomment to get the freq. 
monograms = Freq('english_monograms.txt', cache = 'monograms')
bigrams   = Freq('english_bigrams.txt'  , cache = 'bigrams'  )
trigrams  = Freq('english_trigrams.txt' , cache = 'trigrams' )
quadgrams = Freq('english_quadgrams.txt', cache = 'quagrams' )
words     = Freq('english_words.txt'    , cache = 'words'    )


