class SuffixTree:
    def __init__(self):
        self.text = ""
        self.root = 0
        self.nodes = {}
        self.new_node_id = 1

        root = Node()
        root.id = 0
        root.leaf = False
        self.nodes[0] = root

    def make_leaf(self, node_id):
        return f"{node_id} [shape=box]\n"

    def rec_write_dot(self, node):
        output = []
        edges = self.nodes[node].edges
        if len(edges) == 0:
            output.append(self.make_leaf(node))
            return output

        for c, e in edges.items():
            end = len(self.text) if e.end is None else e.end
            line = f'{node} -> {e.node} [label="{self.text[e.start:end]}"]\n'
            output.extend(line)
            output.extend(self.rec_write_dot(e.node))
        if self.nodes[node].sufix_link is not None:
            line = f"{node} -> {self.nodes[node].sufix_link} [style=dotted]\n"
            output.extend(line)
        return output

    def write_dot(self, i):
        output = []
        output.append(f"digraph phase{i} {{")

        output.extend(self.rec_write_dot(self.root))

        output.append("}")

        return output

    def add_suffix_link(self, node_i, node_j):
        node_i_ref = self.nodes[node_i]
        node_i_ref.sufix_link = node_j

    def move_down(self, active_pos, c):  # try to consume char and return new pos
        # or returns None
        depth = active_pos[2]
        active_node_id = active_pos[0]
        letter = active_pos[1]
        active_node = self.nodes[active_node_id]
        if depth == 0:  # activ pos direct on node : have more then 1 letters
            edge = active_node.edges.get(c)
            if edge == None:  # no way down
                return None

            if edge.end is None:  # edge to end of string
                length_of_edge = len(self.text) - edge.start
            else:
                length_of_edge = edge.end - edge.start
            if length_of_edge == 1:  # edge with one char, next stop is a node
                return (edge.node, "", 0)

            return (active_node_id, c, 1)
        else:
            edge = active_node.edges.get(letter)  # get the edge to the latter
            if edge is None:
                return None

            next_idx = edge.start + depth
            if c != self.text[next_idx]:
                return None

            edge_end = len(self.text) if edge.end is None else edge.end  # end position
            if next_idx + 1 == edge_end:
                return (edge.node, "", 0)

            return (active_node_id, letter, depth + 1)

    def go_down(self, linked_node_id, pos, depth):  # go recursive down depth time
        if depth == 0:
            return (linked_node_id, "", 0)

        next_char = self.text[pos]  # get the letter
        edge = self.nodes[linked_node_id].edges.get(next_char)

        if edge is None:
            return None

        edge_end = len(self.text) if edge.end is None else edge.end
        edge_depth = edge_end - edge.start

        if edge_depth == depth:
            return (edge.node, "", 0)

        if edge_depth > depth:  # pos insede an edge
            return (linked_node_id, next_char, depth)

        if edge_depth < depth:  # go in next edge
            return self.go_down(edge.node, pos + edge_depth, depth - edge_depth)

    def use_suffix_link(self, active_pos):
        node_id = active_pos[0]
        letter = active_pos[1]
        depth = active_pos[2]

        linked_node_id = self.nodes[node_id].sufix_link

        if node_id == 0:  # root
            if depth > 0:
                old_edge = self.nodes[self.root].edges[letter]
                pos = old_edge.start + 1
                new_depth = depth - 1
                return self.go_down(self.root, pos, new_depth)
            else:
                return None

        if linked_node_id is None:
            return None

        if depth == 0:  # no need to go down
            return (linked_node_id, "", 0)

        old_edge = self.nodes[node_id].edges.get(letter)
        pos = old_edge.start  # pusition of the letter im text

        return self.go_down(linked_node_id, pos, depth)

    def set_id(self):
        node_id = self.new_node_id
        self.new_node_id += 1
        return node_id

    def new_inner_node(self, active_pos):
        new_node = Node()
        new_node.leaf = False
        new_node.id = self.set_id()
        self.nodes[new_node.id] = new_node
        return new_node.id

    def create_leaf(self):
        leaf = Node()
        leaf.leaf = True
        leaf.id = self.set_id()
        self.nodes[leaf.id] = leaf
        return leaf.id

    def new_node(self, active_pos, i, j):
        depth = active_pos[2]
        active_node_id = active_pos[0]
        letter = active_pos[1]

        if depth == 0:  # active pos is on node
            leaf_id = self.create_leaf()

            edge_to_leaf = Edge()
            edge_to_leaf.start = i
            edge_to_leaf.end = j
            edge_to_leaf.node = leaf_id

            self.nodes[active_node_id].edges[
                self.text[i]
            ] = edge_to_leaf  # append on active pos

            return active_node_id

        else:  # inseide an edge
            """
            active_pos -> old_edge -> old_child to:
            active_pos -> shorter_old_edge  -> inner_node
            inner_node -> remaining old_edge part -> old_child
            inner_node -> new edge s[i:j] -> new_leaf
            """
            old_edge = self.nodes[active_node_id].edges[letter]

            old_start = old_edge.start
            old_end = old_edge.end
            old_child = old_edge.node

            inner_id = self.new_inner_node(active_pos)

            old_edge.end = old_start + depth
            old_edge.node = inner_id

            edge_to_old_child = Edge()
            edge_to_old_child.start = old_start + depth
            edge_to_old_child.end = old_end
            edge_to_old_child.node = old_child

            self.nodes[inner_id].edges[
                self.text[edge_to_old_child.start]
            ] = edge_to_old_child

            leaf_id = self.create_leaf()

            edge_to_leaf = Edge()
            edge_to_leaf.start = i
            edge_to_leaf.end = j
            edge_to_leaf.node = leaf_id

            self.nodes[inner_id].edges[self.text[i]] = edge_to_leaf

            return inner_id


class Edge:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.node = 0


class Node:
    def __init__(self):
        self.id = None
        self.edges = {}
        self.leaf = False
        self.sufix_link = None
