import os
import pickle

from backend.screen import is_same_screen
from scripting.collector import script_replay, event_seq_replay
from utils.operate_current_device import close_app, open_app


class Extender():
    def __init__(self, package_name, locators, w):

        current_dir = os.getcwd()
        tmp = "demo/tmpFIles/ext/scenario"
        tmp_path_list = tmp.split("/")
        self.path = os.path.join(current_dir, *tmp_path_list)

        self.package_name = package_name

        # TODO: coordinate sequence of events from app's main screen to the screen where the test begins
        # if so, add it manually
        self.pre_base_event_sequences = []
        self.base_event_sequences = []
        self.locators = locators

        self.depth = w

        self.cur_replay_sequences_id = 1

        self.base_scenario_model = None
        self.base_screens = []
        self.base_edges = []

        self.auto_part_traversal_model = []
        self.extended_model = None

        self.auto_extend_seqs = [[[]]]
        self.extend_path = [[]]

    def auto_path_extend(self, auto_path_id):
        """
        current round: auto_path_id + 1
        """
        pre_event_sequences = []

        for elem in range(0, len(self.pre_base_event_sequences)):
            pre_event_sequences.append(self.pre_base_event_sequences[elem])

        for elem in range(0, auto_path_id):
            pre_event_sequences.append(self.base_event_sequences[elem])

        # TODO: add your own traversal methods here

        # read model
        current_dir = os.getcwd()
        tmp1 = "demo/tmpFIles/ext/traverse"
        tmp_path_list1 = tmp1.split("/")
        tmp2 = "simple_result/candidate_model"
        tmp_path_list2 = tmp2.split("/")
        tmp_path = os.path.join(current_dir, *tmp_path_list1, str(auto_path_id + 1), *tmp_path_list2)
        f = open(tmp_path, 'rb')
        part_traversal_model = pickle.load(f)

        self.auto_part_traversal_model.append(part_traversal_model)

        part_traversal_model_screens = []
        for key in part_traversal_model.screens:
            screen = part_traversal_model.screens[key]
            part_traversal_model_screens.append(screen)

        part_traversal_model_edges = part_traversal_model.edges

        cur_end_screen_id = -1
        cur_node_id = -1

        cur_bounds = self.base_event_sequences[auto_path_id]

        # find cur_end_screen_id
        for edge in part_traversal_model_edges:
            if edge.begin_id == 1:
                tmp_node = part_traversal_model_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                if cur_bounds[0] == tmp_node.loc_x and cur_bounds[1] == tmp_node.loc_y and cur_bounds[2] == tmp_node.width and cur_bounds[3] == tmp_node.height:
                    cur_end_screen_id = edge.end_id
                    cur_node_id = edge.node_id

        extend_seqs = []

        extend_seqs.append([[cur_bounds[0], cur_bounds[1], cur_bounds[2], cur_bounds[3]]])
        for edge in part_traversal_model_edges:
            if edge.end_id == cur_end_screen_id:
                tmp_begin_screen_id = edge.begin_id
                tmp_node = part_traversal_model_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)

                if tmp_begin_screen_id == 1 and edge.node_id != cur_node_id:
                    tmp_extend_seq = []
                    tmp_extend_seq.append([tmp_node.loc_x, tmp_node.loc_y, tmp_node.width, tmp_node.height])
                    extend_seqs.append(tmp_extend_seq)
                else:
                    for pre_edge in part_traversal_model_edges:
                        if pre_edge.begin_id == 1 and pre_edge.end_id == tmp_begin_screen_id:
                            pre_edge_node = part_traversal_model_screens[pre_edge.begin_id - 1].get_node_by_id(pre_edge.node_id)
                            tmp_extend_seq = []
                            tmp_extend_seq.append([pre_edge_node.loc_x, pre_edge_node.loc_y, pre_edge_node.width, pre_edge_node.height])
                            tmp_extend_seq.append([tmp_node.loc_x, tmp_node.loc_y, tmp_node.width, tmp_node.height])
                            extend_seqs.append(tmp_extend_seq)

        # integrate the extended results
        for pre_elem in self.extend_path[:len(self.extend_path)]:
            tmp_pre_elem = []
            for elem in pre_elem:
                tmp_pre_elem.append(elem)

            for elem in extend_seqs[0]:
                pre_elem.append(elem)

            for succ_elem in extend_seqs[1:len(extend_seqs)]:
                save_extend_path = []
                for elem in tmp_pre_elem:
                    save_extend_path.append(elem)
                for elem in succ_elem:
                    save_extend_path.append(elem)
                self.extend_path.append(save_extend_path)

        cur_begin_screen = part_traversal_model_screens[0]
        cur_end_screen = part_traversal_model_screens[cur_end_screen_id - 1]

        for i in range(0, self.depth - 1):
            tmp_model_id = auto_path_id - i - 1
            if tmp_model_id >= 0:
                tmp_model = self.auto_part_traversal_model[tmp_model_id]

                tmp_screens = []
                for key in tmp_model.screens:
                    screen = tmp_model.screens[key]
                    tmp_screens.append(screen)

                tmp_edges = tmp_model.edges

                model_id = -1
                for screen_id in range(0, len(tmp_screens)):
                    tmp_screen = tmp_screens[screen_id]

                    if is_same_screen(cur_end_screen, tmp_screen, 0.9):
                        model_id = screen_id + 1

                tmp_extend_seqs = []
                for edge in tmp_edges:
                    if edge.end_id == model_id:
                        tmp_begin_screen_id = edge.begin_id
                        tmp_begin_screen = tmp_screens[tmp_begin_screen_id - 1]
                        tmp_node = tmp_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)

                        if tmp_begin_screen_id == 1:
                            tmp_extend_seqs.append([[tmp_node.loc_x, tmp_node.loc_y, tmp_node.width, tmp_node.height]])
                        else:
                            for pre_edge in tmp_edges:
                                if pre_edge.begin_id == 1 and pre_edge.end_id == tmp_begin_screen_id and not is_same_screen(tmp_begin_screen, cur_begin_screen, 0.9):
                                    pre_edge_node = tmp_screens[pre_edge.begin_id - 1].get_node_by_id(pre_edge.node_id)
                                    tmp_extend_seq = []
                                    tmp_extend_seq.append([pre_edge_node.loc_x, pre_edge_node.loc_y, pre_edge_node.width, pre_edge_node.height])
                                    tmp_extend_seq.append([tmp_node.loc_x, tmp_node.loc_y, tmp_node.width, tmp_node.height])
                                    tmp_extend_seqs.append(tmp_extend_seq)

                if len(tmp_extend_seqs) != 0:
                    auto_extend_seq_id = tmp_model_id
                    for pre_elem in self.auto_extend_seqs[auto_extend_seq_id]:
                        for succ_elem in tmp_extend_seqs:
                            save_extend_path = []
                            for elem in pre_elem:
                                save_extend_path.append(elem)
                            for elem in succ_elem:
                                save_extend_path.append(elem)
                            self.extend_path.append(save_extend_path)

        tmp_auto_extend_seq = []
        for path_level in self.extend_path:
            tmp = []
            for event_level in path_level:
                tmp.append(event_level)
            tmp_auto_extend_seq.append(tmp)

        self.auto_extend_seqs.append(tmp_auto_extend_seq)

    def full_path_extend(self):
        for key in self.base_scenario_model.screens:
            screen = self.base_scenario_model.screens[key]
            self.base_screens.append(screen)

        self.base_edges = self.base_scenario_model.edges

        print("the total number of rounds extended: " + str(len(self.base_edges)))
        for auto_path_id in range(0, len(self.base_edges)):
            print("current round: " + str(auto_path_id + 1))
            self.auto_path_extend(auto_path_id)
            print("end of current round")

        self.extend_path.remove(self.base_event_sequences)

    def work(self):
        # If there is a preorder sequence, add the sequence manually and run the code commented below
        print("Replay event sequence from app's main screen to the screen where the test begins.")
        event_seq_replay(self.pre_base_event_sequences, False, "")
        print("Replay successful.")

        print("Replay base event sequences.")
        save_path = os.path.join(self.path, str(self.cur_replay_sequences_id))
        self.base_event_sequences, self.base_scenario_model = script_replay(self.locators, save_path)
        print("Replay successful.")

        print("Extend the basic test script.")
        close_app(self.package_name)
        open_app(self.package_name)
        event_seq_replay(self.pre_base_event_sequences, False, "")
        self.full_path_extend()

        if len(self.extend_path) == 0:
            print("The given test script cannot be extended.")
        else:
            print("The number of alternative paths obtained is " + str(len(self.extend_path)) + ".")
            print("Replay the extension result to get the corresponding scenario model.")
            for path in self.extend_path:
                close_app(self.package_name)
                open_app(self.package_name)
                event_seq_replay(self.pre_base_event_sequences, False, "")
                self.cur_replay_sequences_id += 1
                cur_save_path = os.path.join(self.path, str(self.cur_replay_sequences_id))
                event_seq_replay(path, True, cur_save_path)

        return self.cur_replay_sequences_id + 1