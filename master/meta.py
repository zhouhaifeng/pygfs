package master

class File(object):
    def __init__(self):
        self.chunk_index = 0
        self.create_time = 0
        self.delete_time = 0
        self.state = 0

class Chunk(object):
    def __init__(self):
        self.node = 0
        self.index = 0
        self.offset = 0
        self.end = 0
        self.time = 0
        self.state = 0

class Meta(object):
    def __init__(self):
        self.chunks = []
        self.slice = {}