#!/usr/bin/env python

import os

from hid import RFIDReader
from config import PadmissConfig
import logging
log = logging.getLogger(__name__)

class FIFOReader(object):
    def __init__(self, path):
        self.path = path
        self.match = {}
        try:
            os.remove(path)
        except:
            pass
        os.mkfifo(path)


    def poll(self):
        with open(self.path, 'r') as fh:
            return fh.readline()


    def release(self):
        os.remove(self.path)


class NULLReader(object):
    def __init__(self, **args):
        pass

    def poll(self):
        return


def construct_readers(config: PadmissConfig):
    readers = {}
    for device in config.devices:
        if device.type == "scanner":
            try:
                readers[device.path] = RFIDReader(device.config)
            except Exception as e:
                log.debug('Failed constructing reader:')
                log.debug(str(e))
#        elif s.type == "fifo":
#            readers[s["path"]] = FIFOReader(s["config"]["swPath"])
#        else:
#            readers[s["path"]] = NULLReader(**s["config"])
    return readers