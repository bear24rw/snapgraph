import sys
import urllib2
from bs4 import BeautifulSoup

root_user = sys.argv[1]
max_depth = int(sys.argv[2])

out_file = open("snapgraph.html", "w")

nodes = []
edges = []

def add_user(name, cur_depth):

    print "\t"*cur_depth, name

    nodes.append('"%s"' % name)

    if (cur_depth == max_depth):
        return

    page = urllib2.urlopen('http://www.snapchat.com/'+name).read()
    soup = BeautifulSoup(page)

    for friend in soup.findAll("div", { "class" : "best_name" }):
        friend_name = friend.find('a')['href'].replace("/","")
        edges.append('"%s", "%s"' % (name, friend_name))
        if (not friend_name in nodes):
            add_user(friend_name, cur_depth + 1)

add_user(root_user, 0)

nodes = list(set(nodes))
edges = list(set(edges))



out_file.write(open("snapgraph.html.top").read())
out_file.write('var graphJSON = {\n')
out_file.write('\t"nodes": [')
out_file.write(', '.join(nodes))
out_file.write('],\n')
out_file.write('\t"edges": [\n')
out_file.write('\t\t[')
out_file.write('],\n\t\t['.join(edges))
out_file.write(']\n')
out_file.write('\t]\n')
out_file.write('};\n')
out_file.write(open("snapgraph.html.bot").read())

