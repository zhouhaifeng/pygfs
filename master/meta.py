package master

class Slice(object):
    def __init__(self):
        self.chunk_index = 0
        self.slice_index = 0
        self.fd = 0
        self.offset = 0
        self.length = 0

class File(object):
    def __init__(self):
        self.fd = 0
        self.create_time = 0
        self.delete_time = 0
        self.slices = {}
        self.state = 0

class Chunk(object):
    def __init__(self):
        self.slice = {}
        self.node = 0
        self.index = 0
        self.length = 0
        self.time = 0
        self.state = 0

class ChunkServer(object):
    def __init__(self):
        self.index = 0
        self.state = 0
        self.chunks = {}
        
class Meta(object):
    def __init__(self):
        #key: file fd; value: 
        self.files = {}
        self.chunkservers = {}
        #key: chunk index; value: chunk object
        self.chunks = {}
