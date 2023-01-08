#!/bin/python3

from metafs_proxy import MetaFSProxy
from metafs import MetaFS
from fs import open_fs
import fs

print("setting up 'targetfs' and 'metafs'")
targetfs = open_fs('example/fs')
targetfs.writetext('/hello.txt','Hi there, amigo.')
metafs = MetaFS('config-userhome-example.sh')

print("setting up instance of MetaFSProxy")
a = MetaFSProxy(targetfs,metafs)

a.tree()

print("testing 'getinfo()'")
i = a.getinfo('/fruit/apples.txt')
print(i.raw)

print("testing 'listdir()'")
try:
    mylist = a.listdir('/')
except Exception as err:
    print(err)
else:
    print(mylist)

print("testing 'makedir()'")
print("before 'makedir()'")
a.tree()

try:
    a.makedir('/newdir')
except Exception as err:
    print(err)
print("after 'makedir()'")
a.tree()


print("testing 'openbin()' via 'readtext()'")
try:
    s = a.readtext('/hello.txt')
    print(s)
except Exception as err:
    print(err)

print("testing 'remove()'")
try:
    a.remove('/hello.txt')
except Exception as err:
    print(err)
print("after 'remove()'")
a.tree()

print("testing 'removedir()'")
try:
    a.removedir('/newdir')
except Exception as err:
    print(err)
print("after 'removedir()'")
a.tree()
