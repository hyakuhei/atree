import sys, tempfile, subprocess, os

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


    graph_text = "graph TD\n"
    for node_id in nodes.keys():
        graph_text += f"\t{node_id}[{nodes[node_id]}]\n"
    
    for link in links:
        graph_text += f"\t{link}\n"

    # If no-args just print 
    if len(sys.argv) == 1:    
        print(graph_text)

    if len(sys.argv) == 2:
        if sys.argv[1] in ["-h", "--help", "-help"]:
            print("Read from STDIN and create a mermaid diagram.")
            print("Without modification, atree will read in text and print out mermaid text")
            print("Example: $ cat list.txt | python3 atree.py > tree.mm")
            print("--out <basename>")
            print("Example: $ cat list.txt | python3 atree.py --out tree")
            print("This will create a tree.txt and a tree.png")

    if len(sys.argv) == 3:
        if "--out" == sys.argv[1]:
            # Call the mermaid CLI (expecting Docker) to generate the file
            # 1. Write the tree text
            # 2. Launch docker, have it create the PNG output

            with open(f"{sys.argv[2]}.mm", "w") as f:
                f.write(graph_text)

            _ = subprocess.run(
                ["docker", "run", "--rm", "-u", f"{os.geteuid()}:{os.getegid()}", "-v", f"{os.getcwd()}:/data", "minlag/mermaid-cli", "--input", f"/data/{sys.argv[2]}.mm", "--output", f"/data/{sys.argv[2]}.png"]
            )
            


        