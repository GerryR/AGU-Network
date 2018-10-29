from agu_api import AguApi
import string
import math
import json

# Year: CHANGE THIS PARAMETER TO LOAD DIFFERENT MEETINGS
year = 2017

# get an instance of the API
api = AguApi()

# get all the program ids
pIds = api.programsIds(year)

for program_id in pIds:
    json_file = 'graphs/coeffs_pid{}_alpha001_minc01.json'.format(program_id)
    print('WORKING ON {}'.format(json_file))

    try:
        with open(json_file, 'r') as f:
            coeffs = json.load(f)
    except:
        print('ERROR: file for program {} not found.'.format(program_id))
        continue

    raw_abstracts = api.abstracts(year, program_id)

    abstracts = {}
    for a in raw_abstracts:
        abstracts[str(a['abstractId'])] = a['title']

    # Export nodes (edges file are enough)
    # with open('graphs/nodes-pid{}-{}.json'.format(program_id, year), 'w') as f:
    #     f.write('Id\n')
    #     for a in abstracts:
    #         f.write('{}\n'.format(a))

    # Prepare edges
    edges = {}
    for a in abstracts:
        top_connections = sorted(coeffs[a].items(), key=lambda t: t[1], reverse=True)[:5]
        # keep connections if weight is greater than 0.5,
        # but be sure there is a least one connection per abstract
        if top_connections:
            best_connections = [top_connections[0]]
            for c, w in top_connections[1:]:
                if w >= 0.5:
                    best_connections.append((c, w))

            for b, w in best_connections:
                if b not in edges or a not in edges[b]:
                    if a not in edges:
                        edges[a] = []
                    edges[a].append((b, w))
    # Export edges
    with open('graphs/edges-pid{}-{}.json'.format(program_id, year), 'w') as f:
        f.write('Source,Target,Weight,Type\n')
        for a in edges:
            for b, w in edges[a]:
                f.write('{},{},{},Undirected\n'.format(a,b,w))
