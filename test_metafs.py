#!/bin/python3
from metafs import MetaFS
import fs.errors

a = MetaFS('config-userhome-example.sh')

a.tree()

print(a.makeinode('/hello.txt'))
print(a.getinfo('/hello.txt'))

print(a.makedir('/boats'))
print(a.makeinode('/boats/catamaran.txt'))
print(a.makeinode('/boats/junk.txt'))

print(a.listdir('/boats'))

print(a.makeinode('/yodel.txt'))
a.tree()

print(a.remove('/yodel.txt'))
try:
    print(a.getinfo('/yodel.txt'))
except fs.errors.ResourceNotFound as error:
    print(error)


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

i = a.getinfo('/')
print(i.is_dir)
print(a.makedir('/paints'))
i = a.getinfo('/paints')
print(i.is_dir)

print(a.makedirs('/paints/primary',recreate=True))
a.tree()
