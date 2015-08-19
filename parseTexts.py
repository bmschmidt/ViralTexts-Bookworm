import json
import sys
import gzip
import re
import copy

file = gzip.open(sys.argv[1])

catalog = open('jsoncatalog.txt','w')
input = open('input.txt','w')

def chunker():
    """
    Break David's input into chunks.
    """
    cluster = []
    for line in file:
        #sys.stderr.write(line)
        cluster.append(line)
        if re.search(r"\}\]\}$",line):
            yield json.loads("".join(cluster))
            cluster = []

for chunk in chunker():
    data = dict()
    data['chunk'] = chunk['id']
    if data['chunk'] > 10000:
        break
    for snippet in chunk['members']:
        metadata = copy.deepcopy(data)
        for key in ['date','name','url']:
            metadata[key] = snippet[key]
        metadata['filename'] = "-".join([snippet['name'],snippet['date']])
        metadata['searchstring'] = '<a href="%s">%s</a>' % (str(snippet['url']),snippet['title'])
        text = snippet['text']
        text = text.replace("<br/>"," ")
        try:
            """
            Major unicode hackage here, must fix
            """
            input.write(metadata['filename'].encode('utf-8') + "\t" + text.encode('utf-8') + "\n")
        except:
            print text

            raise
        catalog.write(json.dumps(metadata) + "\n")


