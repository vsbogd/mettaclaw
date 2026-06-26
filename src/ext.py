import importlib

_mod = None

def commchannel(extname):
    global _mod
    try:
        _mod = importlib.import_module(extname)
        if _mod is not None:
            return 1
    except Exception as e:
        return 0

def commChannelReceiveMessage():
    global _mod
    return _mod.commChannelReceiveMessage()

def commChannelSendMessage(msg):
    global _mod
    return _mod.commChannelSendMessage(msg)
