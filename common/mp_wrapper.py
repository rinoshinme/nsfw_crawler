

class MultiprocessWrapper(object):
    def __init__(self, nproc=10):
        self.fn = None
        self.nproc = nproc

    def bind(self, fn):
        self.fn = fn
    
    def run(self):
        if self.fn is None:
            return
        


if __name__ == '__main__':
    pass
