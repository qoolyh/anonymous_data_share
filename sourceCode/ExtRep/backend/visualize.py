import os

import cv2
from graphviz import Digraph


class VisualTool:
    def __init__(self, screens, edges, save_dir):
        self.dot = Digraph(comment='The Round Table')

        self.screens = screens

        self.edges = edges

        self.save_dir = save_dir

    def create_nodes(self):
        for key in self.screens.keys():
            screen = self.screens[key]

            img = cv2.imread(screen.shot_dir)
            small_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

            img_dir = self.save_dir + '/' + 'image'

            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            cv2.imwrite(img_dir + '/' + str(screen.id) + '.png', small_img)

            self.dot.node(str(screen.id), shapefile=img_dir + '/' + str(screen.id) + '.png', fontsize='30')


    def create_edges(self):
        for edge in self.edges:
            node_id = edge.node_id
            clickable_node = self.screens[edge.begin_id].get_node_by_id(node_id)
            if clickable_node.attrib['text'] != '':
                label = clickable_node.attrib['text'] + '-' + clickable_node.attrib['bounds']
            elif clickable_node.attrib['content-desc'] != '':
                label = clickable_node.attrib['content-desc'] + '-' + clickable_node.attrib['bounds']
            elif clickable_node.attrib['resource-id'] != '':
                label = clickable_node.attrib['resource-id'].split('/')[1] + '-' + clickable_node.attrib['bounds']
            else:
                label = clickable_node.attrib['bounds']
            self.dot.edge(str(edge.begin_id), str(edge.end_id), label=label, fontname='SimSun', fontsize='30')


    def save_graph(self):
        self.dot.render(filename='traverse_graph2', directory=self.save_dir, view=True)

    def save_work(self):
        self.create_nodes()
        self.create_edges()
        self.save_graph()
