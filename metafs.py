import redis

from fs.base import FS



class MetaFS(FS):

    def __init__(self, redis_host, redis_port):
        self.redis = redis.Redis(redis_host,redis_port,db=0)


    def getinfo(self, path, namespaces=None):
        pass

    def listdir(self, path):
        pass
    
    def makedir(self, path, permissions=None, recreate=False):
        pass
    
    def openbin(self, path, mode='r', buffering=-1, **options):
        pass

    def remove(self, path):
        pass

    def removedir(path):
        pass

    def setinfo(self, info):
        pass

