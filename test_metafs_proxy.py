#!/bin/python3

from metafs_proxy import MetaFSProxy
from metafs import MetaFS
from fs import open_fs


targetfs = open_fs('example/fs')
metafs = MetaFS('config-userhome-example.sh')

a = MetaFSProxy(targetfs,metafs)

i = a.getinfo('/fruit/apples.txt')
print(i.raw)
a.metafs.tree()
