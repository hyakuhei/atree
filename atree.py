import sys, tempfile, subprocess, os

from typing import Union


def alphaFromDecimals(decimals: str) -> str:
    map = {
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
            next_directive_idx = nodes[node_id][link_idx + 1 :].find("#")
            if next_directive_idx == -1:
                next_directive_idx = len(nodes[node_id])  # (last idx)

            # Ok so now we look for all the number strings between link_idx
            # print(f"Found a directive in {nodes[node_id]} between {link_idx} and {next_directive_idx}")

            for nodeString in (
                nodes[node_id][link_idx + len(link_txt) : next_directive_idx]
                .replace(",", " ")
                .split(" ")
            ):
                nodeString = nodeString.strip()
                if nodeString != "":
                    links.append(f"{node_id} --> {alphaFromDecimals(nodeString)}")

            # Skip ahead (or to the end of the string)
            link_idx = next_directive_idx

    # Go through the code and strip out any #directives
    for node_id in nodes.keys():
        link_idx = nodes[node_id].find(link_txt)
        if link_idx > 0:
            nodes[node_id] = nodes[node_id][0 : link_idx - 1]

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
        )
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
            graph_text += f"\t{node_id}[{nodes[node_id]}]\n"

        for link in links:
            graph_text += f"\t{link}\n"
    
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
            s = _wrap(nodes[key], parms["wrap_width"])
            nodes[key] = s
        
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
