import redis
import json

from fs.base import FS
from fs.path import split as path_split
from fs.info import Info
from dotenv import dotenv_values



class MetaFS(FS):

    def __init__(self, userhome_config_path, redis_config_path="config-redis.sh"):
        config = {
            **dotenv_values(redis_config_path),
            **dotenv_values(userhome_config_path)
        }
        fsurn = f'fs:{config["USERPUBLICID"]}:{config["USERHOMENAME"]}:{config["USERFSURL"]}'

        print(f"MetaFS::__init__::fsurn: {fsurn}")
        
        self.config = config
        self.fsurn = fsurn

        self.redis = redis.Redis(
                config['REDIS_CONTAINER_HOST'],
                config['REDIS_CONTAINER_PORT'],
                db=0)

        if(self.redis.get('curino') == None):
            self.redis.set('curino',1)

        self.fsnokey = self.redis.get(fsurn)
        if(self.fsnokey == None):
            ino = self.getnextino()
            print(f"self.getnextino(): {ino}")
            fsnokey = self.makefsnokey(ino)
            inokey = self.makeinokey(ino)

            self.fsnokey = fsnokey

            self.redis.set(fsurn,fsnokey)

            self.redis.set(fsnokey,
                json.dumps({
                    "root":inokey,
                    "urn":fsurn,
                    "user":config['USERPUBLICID'],
                    "url":config['USERFSURL']
                })
            )
        fsrecord = json.loads(self.redis.get(self.fsnokey))
        print(f'MetaFS::__init__::fsnokey: {self.fsnokey}')
        print(f'MetaFS::__init__::<fs record>: {fsrecord}')

        self.rootinokey = fsrecord['root']

    def lookup(self, inokey, pathseg):
        recordstr = self.redis.get(inokey)
        record = json.loads(recordstr)
        if "dir" in record:
            for entrykey in record["dir"]:
                entrystr = self.redis.get(entrykey)
                entry = json.loads(entrystr)
                if entry["info"]["basic"]["name"] == pathseg:
                    return entrykey
        return None

    def pathwalk(self, path):
        if path == "/" or path == "":
            return self.rootinokey
        path = path.lstrip('/')
        segs = path.split('/')
        nextinokey = self.rootinokey
        for pathseg in segs:
            nextinokey = self.lookup(nextinokey, pathseg)
            if nextinokey == None:
                return None
        return nextinokey

    def getnextino(self):
        nextino = self.redis.incr('curino') 
        return nextino

    def makerootinode(self):
        rootinokey = self.rootinokey
        record_dict = {
            "info":{"basic":{"name":"","is_dir":True}},
            "dir": [],
            "par": self.fsnokey.decode(),
        }
        self.redis.set(rootinokey, json.dumps(record_dict))
        return rootinokey


    def makefsnokey(self, num):
        return f'fs:{num}'

    def makeinokey(self,num):
        return f'ino:{num}'

    def getinfo(self, path, namespaces=None):
        target_inokey = self.pathwalk(path)
        if not target_inokey:
            return None

        target_record_str = self.redis.get(target_inokey)
        target_record = json.loads(target_record_str)
        if "info" in target_record:
            info_raw = target_record["info"]
            info = Info(info_raw)
            return info

        return None

    def listdir(self, path):
        pass
    
    def makedir(self, path, permissions=None, recreate=False):
        pass

    def makeinode(self, path):
        existing_inokey = self.pathwalk(path)
        if existing_inokey:
            return existing_inokey

        _dirname, _basename = path_split(path)

        parent_inokey = self.pathwalk(_dirname)
        parent_record_str = self.redis.get(parent_inokey)
        parent_record = json.loads(parent_record_str)
        
        new_ino = self.getnextino()
        new_inokey = self.makeinokey(new_ino)
        new_record = {"info":{"basic":{"name":_basename}}}
        new_record_str = json.dumps(new_record)
       
        if "dir" not in parent_record:
            parent_record["dir"] = list()

        parent_record["dir"].append(new_inokey)
        parent_record_str = json.dumps(parent_record)
        
        self.redis.set(new_inokey,new_record_str.encode())
        self.redis.set(parent_inokey,parent_record_str.encode())
        
        return new_inokey
    
    def openbin(self, path, mode='r', buffering=-1, **options):
        pass

    def remove(self, path):
        pass

    def removedir(self, path):
        pass

    def setinfo(self, path, info):
        pass

