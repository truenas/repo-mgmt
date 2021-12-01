class CallError(Exception):
    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg


class MissingManifest(CallError):
    def __init__(self):
        super().__init__('Unable to locate manifest file')
