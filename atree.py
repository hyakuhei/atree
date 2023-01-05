import sys, subprocess, os

from typing import Union


def alphaFromDecimals(decimals: str) -> str:
    mapping = {
        "1": "A",
        "2": "B",
        "3": "C",
        "4": "D",
        "5": "E",
        "6": "F",
        "7": "G",
        "8": "H",
        "9": "I",
        "0": "K",
    }

    node_id = ""
    for c in decimals:
        if c in mapping:
            node_id += mapping[c]

    return node_id

def visit(node:dict, new_lines: list, label: str=""):
    l = f"{label}{node['id']}."
    new_lines.append(f"{l} {node['string']}")

    if len(node['children']) > 0:
        for c in node['children']:
            visit(c, new_lines, label=l)

def parseTabbed(lines: list[str]):
    prev_node = None
    root_node = None

    for s in lines:
        if len(s.strip()) == 0:
            continue
        
        depth = len(s.split("    "))

        new_node = {
                    "string": s.strip(),
                    "depth": depth,
                    "children": [],
                    "parent": None,
                    "id":-1
                }

        if prev_node == None:
            new_node['id'] = 1
            prev_node = new_node
            root_node = new_node
        else:
            if depth == prev_node["depth"]:
                # Add a child to the parent of the prev_node
                # Making prev_node a sibiling of this new node
                new_node["parent"] = prev_node["parent"]
                new_node["parent"]["children"].append(new_node)
                new_node['id'] = len(new_node["parent"]["children"])

                #setup for next loop
                prev_node = new_node

            elif depth > prev_node["depth"]:
                # Add a child to prev node
                new_node["parent"] = prev_node
                prev_node["children"].append(new_node)
                new_node['id'] = len(new_node["parent"]["children"])

                #setup for next loop
                prev_node = new_node

            elif depth < prev_node["depth"]:
                #Walk back up the tree 
                ptr = prev_node
                while depth < ptr["depth"]:
                    ptr = ptr["parent"]
                
                new_node["parent"] = ptr["parent"]
                ptr["parent"]["children"].append(new_node)
                new_node['id'] = len(new_node["parent"]["children"])

                #setup for next loop
                prev_node = new_node
    
    new_lines = []
    visit(root_node, new_lines)
    return new_lines

def readIn(nodes: dict, links: list, directives: dict):
    directive_keys = directives.keys()
    lines = sys.stdin.readlines()

    first_id = alphaFromDecimals(lines[0])
    if first_id == "":
        print("No numberered list found - probably tabbed")
        lines = parseTabbed(lines)
    
    first_id = alphaFromDecimals(lines[0])
    if first_id == "":
        print("ERROR")
        sys.exit(-1) 

    for s in lines:
        s = s.strip()
        slices = s.split(" ")
        if len(slices) < 2:
            # skip the line
            continue

        # Expect some pattern if integer + period + integer
        # e.g 1.2.2.3.4
        # e.g 1.2.3.4.5.

        node_id = alphaFromDecimals(slices[0])
        # If the list starts with a number and a period
        # e.g 1. do stuff 
        # Then it's treated as a numbered list

        if node_id != "":
            # Create the node and add text
            nodes[node_id] = {
                'text':" ".join(slices[1:]),
                'directives':{}
            }
            # Add any directives
            text_directives = [i for i in directive_keys if i in nodes[node_id]['text']]
            for dir in text_directives:
                nodes[node_id]['directives'][dir] = directives[dir]

    # Process links
    for node_id in nodes.keys():
        # Add all the hierarchical links
        if node_id[:-1] in nodes:
            links.append(f"{node_id[:-1]} --> {node_id}")

def directive_link(node_id: str, nodes: dict, links: list, anchors: dict):
    # Add additional links (using the #link directive)
    # A user can add a link which will draw from the current node to the specified one
    # 1. Top
    # 1.1 Left #link 1.2.3, 1.2
    # 1.2 Right
    # 1.2.3 Down

    # A link directive (currently "#link") should be followed by a comma separated list of items to link to
    # The string should then either terminate, or another # directive may start.
    # That other directive might be another #link or something unimplemented yet, like maybe #rlink (reversed arrow)...
    link_idx = nodes[node_id]['text'].find("#link")
    while link_idx != -1 and link_idx < len(nodes[node_id]['text']):
        next_directive_idx = nodes[node_id]['text'][link_idx + 1 :].find("#")
        if next_directive_idx == -1:
            next_directive_idx = len(nodes[node_id]['text'])  # (last idx)

        # look for all the number strings between link_idx
        # print(f"Found a directive in {nodes[node_id]} between {link_idx} and {next_directive_idx}")
        for nodeString in (
            nodes[node_id]['text'][link_idx + len("#link") : next_directive_idx]
            .replace(",", " ")
            .split(" ")
        ):
            nodeString = nodeString.strip()
            if nodeString != "":
                # See if this is a node we have, or an anchor, or a broken link 
                natural_node_id = alphaFromDecimals(nodeString)
                if natural_node_id in nodes:
                    links.append(f"{node_id} -.-> {natural_node_id}")
                elif nodeString in anchors:
                    links.append(f"{node_id} -.-> {anchors[nodeString]}")
                else:
                    print(f"Bad Link {nodeString}")
                
        # Skip ahead (or to the end of the string)
        link_idx = next_directive_idx

def directive_AND(node_id: str, nodes: dict, links: list, subgraphs: dict):
    # return
    and_idx = nodes[node_id]['text'].find("#AND")
    if and_idx > -1:    
        # Find immediate children of this node and add them to a subgraph
        subgraph_id = len(subgraphs.items())
        subgraphs[subgraph_id] = [i.split(" ")[-1] for i in links if i.startswith(f"{node_id} -->")]
        subgraphs[subgraph_id].append(node_id)
    
def directive_anchor(node_id: str, nodes: dict, anchors:dict):
    anchor_idx = nodes[node_id]['text'].find("#anchor")
    if anchor_idx > -1:
        #The anchor should be the next word after the #anchor directive
        anchor_id = nodes[node_id]['text'][anchor_idx + len("#anchor")+1:].split(" ")[0]
    
        anchors[anchor_id]=node_id

def process_directives(nodes: dict, links: list, subgraphs: dict, anchors: dict):
    # We want to make sure that all the Anchors are processed before any links get processed
    for node_id in nodes.keys():
        if "#anchor" in nodes[node_id]['directives']:
            directive_anchor(node_id, nodes, anchors)

    for node_id in nodes.keys():
        if "#link" in nodes[node_id]['directives']:
            directive_link(node_id, nodes, links, anchors)
        
        if "#AND" in nodes[node_id]['directives']:
            directive_AND(node_id, nodes, links, subgraphs)

if __name__ == "__main__":
    # In-tree text directives
    link_txt = "#link"
    and_txt = "#AND"

    directives = {
        "#link":{
            'function':directive_link
        },
        "#AND":{
            'function':directive_AND
        },
        "#anchor":{
            'function':directive_anchor
        }
    }

    nodes = {}
    links = []
    subgraphs = {}
    anchors = {} #Map "anchor name" to "node_id"

    readIn(nodes, links, directives)

    process_directives(nodes, links, subgraphs, anchors)

    # Go through the code and strip out any #directives
    for node_id in nodes.keys():
        if len(nodes[node_id]['directives'].keys()) == 0:
            continue # go to the next iteration of the node_id loop
        else:
            for directive_key in directives.keys():
                idx = nodes[node_id]['text'].find(directive_key)
                if idx > -1:
                    nodes[node_id]['text'] = nodes[node_id]['text'][0: idx -1]
                    continue # go to the next iteration of the directive_key loop

    ## Argument Handling
    commands = {
        "--help": (
            "--help",
            "Read from STDIN and create a mermaid diagram.",
        ),
        "--out": (
            "--out base",
            "Generate a series of files, base.mm, base.png, base.svg",
        ),
        "--wrap": (
            "--wrap 20",
            "Wrap each box at _roughly_ 20 characters - will try not to break words up",
        ),
        "--lr":(
            "--lr",
            "Print graph left-to-right rather than top down"
        ),
    }

    parms = {"exec_mermaid": False, "print": True, "wrap": False, "orientation": "TD"}

    def _variableArg(flag: str) -> Union[str, None]:
        if flag in sys.argv:
            assert len(sys.argv) > sys.argv.index(
                flag
            )  # Check there's at least one more item
            assert not sys.argv[sys.argv.index(flag) + 1].startswith("-")
            return sys.argv[sys.argv.index(flag) + 1]
        else:
            return None

    def _wrap(s: str, width: int) -> str:
        n = ""
        ctr = 0
        for c in s:
            ctr += 1
            if ctr > width and c == " ":
                n += "\\n"
                ctr = 0
            else:
                n += c

        return n

    def _genGraphText(nodes):
        graph_text = f"graph {parms['orientation']}\n"
        for node_id in nodes.keys():
            graph_text += f"\t{node_id}[{nodes[node_id]['text']}]\n"

        for link in links:
            graph_text += f"\t{link}\n"

        for subgraph_id in subgraphs.keys():
            graph_text += f"\tsubgraph {subgraph_id} [ ]\n"
            for node_id in subgraphs[subgraph_id]:
                graph_text += f"\t\t {node_id}\n"
            graph_text += f"\tend\n"

        return graph_text

    if "--out" in sys.argv:
        parms["print"] = False
        parms["exec_mermaid"] = True
        parms["exec_mermaid_filename"] = _variableArg("--out")

    if "--wrap" in sys.argv:
        parms["wrap"] = True
        parms["wrap_width"] = _variableArg("--wrap")

        if parms["wrap_width"] != None:
            parms["wrap_width"] = int(parms["wrap_width"])
        else:
            assert("Incorrect wrap parameter")

    if "--lr" in sys.argv:
        parms["orientation"] = "LR"

    if "--help" in sys.argv:
        parms["print"] = False
        print("Generate graphs from numbered list input")
        print("e.g: $ cat file.txt | python3 atree.py")
        print("e.g: $ cat file.txt | python3 atree.py --out mydiagrams")
        print("")
        for c in commands.keys():
            print(f"{c}\t{commands[c][0]} \t | {commands[c][1]}")

    if parms["wrap"]:
        for key in nodes.keys():
            s = _wrap(nodes[key]['text'], parms["wrap_width"])
            nodes[key]['text'] = s
        
    if parms["exec_mermaid"]:
        # Call the mermaid CLI (expecting Docker) to generate the file
        # 1. Write the tree text
        # 2. Launch docker, have it create the PNG output
        with open(f"{parms['exec_mermaid_filename']}.mm", "w") as f:
            f.write(_genGraphText(nodes))


        def _dockerMermaid(basefile, extension):
            _ = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-u",
                    f"{os.geteuid()}:{os.getegid()}",
                    "-v",
                    f"{os.getcwd()}:/data",
                    "minlag/mermaid-cli",
                    "--input",
                    f"/data/{basefile}.mm",
                    "--output",
                    f"/data/{basefile}.{extension}",
                ]
            )

        _dockerMermaid(f"{parms['exec_mermaid_filename']}", "png")
        _dockerMermaid(f"{parms['exec_mermaid_filename']}", "svg")

    # If no-args just print
    if parms["print"]:
        print(_genGraphText(nodes))
