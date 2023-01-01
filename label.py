import sys, json

line_ctr = 0
depth = 0
pdepth = 0

prev_node = None
root_node = None

def visit(node, label=""):
    l = f"{label}{node['id']}."
    print(f"{l} {node['string']}")

    if len(node['children']) > 0:
        for c in node['children']:
            visit(c,l)

if __name__ == "__main__":
    for s in sys.stdin.readlines():
        line_ctr += 1
        slices = s.split("    ")
        depth = len(slices)

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

    
    visit(root_node)