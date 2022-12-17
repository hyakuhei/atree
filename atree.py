import sys, tempfile, subprocess, os

def alphaFromDecimals(decimals: str) -> str:
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
    
    node_id = ""
    for c in decimals:
        if c in map:
            node_id += map[c]
            
    return node_id

if __name__ == "__main__":
    # In-tree text directives
    link_txt = "#link"



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

        node_id = alphaFromDecimals(slices[0])
        
        if node_id != "":
            nodes[node_id] = " ".join(slices[1:]).strip()
        
    for node_id in nodes.keys():
        # Add all the hierarchical links
        if node_id[:-1] in nodes:
            links.append(f"{node_id[:-1]} --> {node_id}")

        # Add any additional links (using the #link directive)
        # A user can add a link which will draw from the current node to the specified one
        # 1. Top
        # 1.1 Left #link 1.2.3, 1.2
        # 1.2 Right
        # 1.2.3 Down

        # A link directive (currently "#link") should be followed by a comma separated list of items to link to
        # The string should then either terminate, or another # directive may start.
        # That other directive might be another #link or something unimplemented yet, like maybe #rlink (reversed arrow)...
        link_idx = nodes[node_id].find(link_txt)
        while link_idx != -1 and link_idx < len(nodes[node_id]): 
            next_directive_idx = nodes[node_id][link_idx+1:].find('#')
            if next_directive_idx == -1:
                next_directive_idx = len(nodes[node_id]) #(last idx)

            # Ok so now we look for all the number strings between link_idx
            # print(f"Found a directive in {nodes[node_id]} between {link_idx} and {next_directive_idx}")

            for nodeString in nodes[node_id][link_idx+len(link_txt):next_directive_idx].replace(","," ").split(" "):
                nodeString = nodeString.strip()
                if nodeString != '':
                    links.append(f"{node_id} --> {alphaFromDecimals(nodeString)}")


            #Skip ahead (or to the end of the string)
            link_idx = next_directive_idx

    # Go through the code and strip out any #directives
    for node_id in nodes.keys():
        link_idx = nodes[node_id].find(link_txt)
        if link_idx > 0:
            nodes[node_id] = nodes[node_id][0:link_idx-1]

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
        if sys.argv[1] in ["--out", "-out", "-o"]:
            # Call the mermaid CLI (expecting Docker) to generate the file
            # 1. Write the tree text
            # 2. Launch docker, have it create the PNG output

            with open(f"{sys.argv[2]}.mm", "w") as f:
                f.write(graph_text)

            _ = subprocess.run(
                ["docker", "run", "--rm", "-u", f"{os.geteuid()}:{os.getegid()}", "-v", f"{os.getcwd()}:/data", "minlag/mermaid-cli", "--input", f"/data/{sys.argv[2]}.mm", "--output", f"/data/{sys.argv[2]}.png"]
            )
            
            _ = subprocess.run(
                ["docker", "run", "--rm", "-u", f"{os.geteuid()}:{os.getegid()}", "-v", f"{os.getcwd()}:/data", "minlag/mermaid-cli", "--input", f"/data/{sys.argv[2]}.mm", "--output", f"/data/{sys.argv[2]}.svg"]
            )


        