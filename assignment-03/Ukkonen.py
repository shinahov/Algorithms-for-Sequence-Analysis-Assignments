from SuffixTree import SuffixTree
import sys
import os

s = sys.argv[1]
os.makedirs("Dot", exist_ok=True)


tree = SuffixTree()  # an empty tree

active_pos = (0, "", 0)  # (node, letter, depth)
# s = "babacacb$"
for i, c in enumerate(s):
    tree.text += c
    visited_nodes = []

    while True:
        new_pos = tree.move_down(active_pos, c)

        if new_pos is None:
            link_target = tree.use_suffix_link(active_pos)
            parent_id = tree.new_node(active_pos, i, None)
            visited_nodes.append(parent_id)

            if link_target is None:
                break  # we have reached the root

            active_pos = link_target

        else:
            visited_nodes.append(active_pos[0])
            active_pos = new_pos
            break

    for j in range(len(visited_nodes) - 1):
        tree.add_suffix_link(visited_nodes[j], visited_nodes[j + 1])

    # print("".join(tree.write_dot(i)))
    dot_text = "".join(tree.write_dot(i))

    with open(os.path.join("Dot", f"phase{i}.dot"), "w", encoding="utf-8") as f:
        f.write(dot_text)
