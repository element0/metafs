#!/bin/python3
from metafs import MetaFS
import fs.errors

a = MetaFS('config-userhome-example.sh')

print(a.makeinode('/hello.txt'))
print(a.getinfo('/hello.txt'))

print(a.makedir('/boats'))
print(a.makeinode('/boats/catamaran.txt'))
print(a.makeinode('/boats/junk.txt'))

print(a.listdir('/boats'))

print(a.makeinode('/yodel.txt'))
a.tree()

print(a.remove('/yodel.txt'))
print(a.getinfo('/yodel.txt'))
print(a.makedir('/hats'))
a.tree()
try:
    print(a.removedir('/boats'))
except fs.errors.DirectoryNotEmpty as error:
    print(error)

print(a.removedir('/hats'))

raw_info = {"basic":{"name":"hello.txt","is_dir":False},"custom":"deadbeef"}

print(a.setinfo('/hello.txt',raw_info))
print(a.getinfo('/hello.txt').raw)
