from metafs import MetaFS

a = MetaFS('config-userhome-example.sh')

a.makeinode('/hello.txt')

a.pathwalk('/hello.txt')
