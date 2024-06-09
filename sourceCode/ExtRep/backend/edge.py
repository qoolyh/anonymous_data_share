class Edge:
    """
    GUI edge
    """

    def __init__(self, b_id, e_id, n_id):
        self.begin_id = b_id
        self.end_id = e_id
        self.action = 'clicked'

        self.node_id = n_id

def has_same_edge(screens, edges, begin_id, end_id, clicked_node):
    if clicked_node.attrib['resource-id'] != '':
        for edge in edges:
            if edge.begin_id == begin_id and edge.end_id == end_id:
                screen = screens[begin_id]
                node = screen.get_node_by_id(edge.node_id)
                if node.attrib['resource-id'] == clicked_node.attrib['resource-id']:
                    return True

    return False