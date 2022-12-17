import sys

if __name__ == "__main__":

    map = {'1':'A',
        '2':'B',
        '3':'C',
        '4':'D',
        '5':'E',
        '6':'F',
        '7':'G',
        '8':'H',
        '9':'I',
        '0':'K'}

    nodes = {}
    links = []
    for s in sys.stdin.readlines():
        slices = s.split(" ")
        if len(slices) < 2:
            # skip the line
            continue
        
        # Expect some pattern if integer + period + integer
        # e.g 1.2.2.3.4
        # e.g 1.2.3.4.5.

        node_id = ""
        for c in slices[0]:
            if c in map:
                node_id += map[c]
        
        if node_id != "":
            nodes[node_id] = " ".join(slices[1:]).strip()
        
        #print(f'{node_id} {"".join(slices[1:0])}')
    # At this point we have all the nodes, with hierarchical node names, stored in a flat map (nodes)
    # Should we store it in a tree? 

    for node_id in nodes.keys():
        if node_id[:-1] in nodes:
            links.append(f"{node_id[:-1]} --> {node_id}" )

    print("graph TD")
    for node_id in nodes.keys():
        print(f"\t{node_id}[{nodes[node_id]}]")
    
    for link in links:
        print(f"\t{link}")
            
            


        