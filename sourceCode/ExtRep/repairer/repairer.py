import os
import pickle
import shutil
import time
import xml.etree.ElementTree as xeTree

from backend.xml_tree import parse_nodes_patch
from scripting.collector import visual, event_seq_replay
from scripting.writer import write_repaired_test_script, locate_element
from utils.calculate_similarity import get_screen_sim_score, get_node_sim, get_ext_sim
import gensim.models.keyedvectors as word2vec

from utils.operate_current_device import close_app, open_app


class Repairer():
    """
    Repair the given test script
    """

    def __init__(self, package_name, total_scenario_num, w, caps, result_save_path):

        self.package_name = package_name

        current_dir = os.getcwd()
        tmp = "demo/tmpFIles/rep"
        tmp_path_list = tmp.split("/")
        self.path = os.path.join(current_dir, *tmp_path_list)
        self.result_save_path = result_save_path

        self.base_scenario_model = None
        self.scenario_model = None
        self.screens = {}
        self.edges = []

        self.target_seqs = [[]]

        # TODO: coordinate sequence of events from app's main screen to the screen where the test begins
        # TODO: if so, add it manually
        self.update_pre_event_sequences = []
        self.pre_event_sequences = []
        for elem in self.update_pre_event_sequences:
            self.pre_event_sequences.append(elem)

        self.screen_id = 1
        self.cur_screen_id = -1
        self.clicked_node = None

        self.distinct_rate = 0.9
        self.text_sim = 0.4
        self.sims = {}

        self.flag = -1
        self.tmp_model = None
        self.w = w

        self.total_scenario_num = total_scenario_num

        self.cur_repair_path_id = -1

        self.wv2_model = None

        self.ori_event_detail = []
        self.match_detail_info = []

        self.caps = caps

    def extract_candidate_seqs(self, candidate_model):
        """
        extract all acyclic sequences of length up to w from the given candidate model
        """

        candidate_model_edges = candidate_model.edges
        candidate_seqs_dict = {}

        for i in range(0, self.w):
            length = i + 1
            print("all candidate sequences of length " + str(length) + " are being extracted ...")
            tmp_candidate_seqs = []

            if length == 1:
                for edge in candidate_model_edges:
                    if edge.begin_id == 1:
                        tmp_seq = []
                        tmp_seq.append(edge)
                        tmp_candidate_seqs.append(tmp_seq)
            else:
                for pre_seq in candidate_seqs_dict[length - 1]:
                    screen_ids = []
                    screen_ids.append(1)
                    for edge in pre_seq:
                        screen_ids.append(edge.end_id)

                    for edge in candidate_model_edges:
                        if edge.begin_id == screen_ids[-1] and (edge.end_id not in screen_ids):
                            tmp_seq = []
                            tmp_seq.extend(pre_seq)
                            tmp_seq.append(edge)
                            tmp_candidate_seqs.append(tmp_seq)

            print("the total number of candidate sequences of length " + str(length) + " is: " + str(len(tmp_candidate_seqs)) + ".")
            candidate_seqs_dict[length] = tmp_candidate_seqs

        candidate_seqs = []

        for length in range(1, len(candidate_seqs_dict)+1):
            candidate_seqs.extend(candidate_seqs_dict[length])

        print("the total number of candidate sequences obtained is: " + str(len(candidate_seqs)))

        return candidate_seqs

    def calculate_seq_trans_prob(self, original_seq, candidate_seq, candidate_model_screens, null_sim):
        """
        similarity between STLs
        """

        max_score = -1
        k = len(original_seq)
        l = len(candidate_seq)
        normalize_param = max(k, l)
        first_node_match_seq = []

        for i in range(0, self.w+1):
            first_part_prob = -1

            first_original_seq = original_seq[0]
            first_candidate_seq = []
            for j in range(1, i+1):
                if j <= len(candidate_seq):
                    first_candidate_seq.append(candidate_seq[j - 1])

            first_base_screen = self.screens[first_original_seq.end_id - 1]
            first_base_edge = self.screens[first_original_seq.begin_id - 1].get_node_by_id(first_original_seq.node_id)

            first_node_match_index = -1
            if len(first_candidate_seq) == 0:
                first_part_prob = null_sim
            else:
                for j in range(0, len(first_candidate_seq)):
                    cur_match_node = first_candidate_seq[j]
                    matched_updated_screen = candidate_model_screens[cur_match_node.end_id - 1]
                    matched_updated_edge = candidate_model_screens[cur_match_node.begin_id - 1].get_node_by_id(cur_match_node.node_id)

                    screen_sim = get_screen_sim_score(first_base_screen, matched_updated_screen)
                    tmp_flag, edge_sim = get_node_sim(first_base_edge, matched_updated_edge, self.wv2_model)

                    match_pair_score = (screen_sim + edge_sim) / 2
                    all_pair_multiply_score = pow(null_sim, (len(first_candidate_seq) - 1)) * match_pair_score

                    cur_first_part_prob = pow(all_pair_multiply_score, 1/len(first_candidate_seq))
                    if cur_first_part_prob > first_part_prob:
                        first_part_prob = cur_first_part_prob
                        first_node_match_index = j

            second_original_seq = original_seq[1:]
            second_candidate_seq = candidate_seq[i:]

            if len(second_original_seq) == 0 or len(second_candidate_seq) == 0:
                if len(second_original_seq) == 0 and len(second_candidate_seq) == 0:
                    second_part_prob = 1
                else:
                    second_part_prob = null_sim
            else:
                second_part_prob, inter = self.calculate_seq_trans_prob(second_original_seq, second_candidate_seq, candidate_model_screens, null_sim)

            cur_score = pow(first_part_prob*second_part_prob, 1/normalize_param)

            if cur_score > max_score or (cur_score == max_score and abs(i - 1) <= abs(len(first_node_match_seq) - 1)):
                max_score = cur_score
                first_node_match_seq = []
                for j in range(0, first_node_match_index+1):
                    first_node_match_seq.append(first_candidate_seq[j])

        return max_score, first_node_match_seq

    def find_matched_seq(self, autoseq_id):
        """
        given a small segment in the base scenario model, find candidate sequences in the updated app that match it
        """
        original_seq = []
        for i in range(0, self.w):
            if (autoseq_id + i) < len(self.edges):
                original_seq.append(self.edges[autoseq_id + i])

        print("segment under repair details: ")
        original_seq_node = []
        original_seq_screen = []
        for edge in original_seq:
            end_screen = self.screens[edge.end_id - 1]
            original_seq_screen.append(end_screen)
            tmp_node = self.screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
            original_seq_node.append(tmp_node)
            tmp_str = str(tmp_node.attrib)
            print(tmp_str)

        if self.flag == 0:
            candidate_model = self.tmp_model
        else:

            # TODO: add your own traversal methods here

            tmp_path1 = os.path.join(self.path, str(self.cur_repair_path_id), "traverse", str(autoseq_id + 1))
            tmp_path2 = "simple_result/candidate_model"
            tmp_path_list2 = tmp_path2.split("/")
            tmp_model_path = os.path.join(tmp_path1, *tmp_path_list2)
            with open(tmp_model_path, 'rb') as f:
                candidate_model = pickle.load(f)

        print("extract all candidate sequences in the model ...")
        candidate_seqs = self.extract_candidate_seqs(candidate_model)

        # find matching sequences
        max_score = 0
        target_seq = []

        candidate_model_screens = []
        for key in candidate_model.screens:
            screen = candidate_model.screens[key]
            # patch
            screen_xml_file = os.path.join(str(screen.act_name) + '-' + str(screen.id), '1.xml')
            if self.flag == 0:
                tmp_file_index = 1
                for index in range((len(self.match_detail_info)-1), -1, -1):
                    if self.match_detail_info[index] == 0 and self.match_detail_info[index-1] == 1:
                        tmp_file_index = index + 1
                        break
                screen_xml_path = os.path.join(self.path, str(self.cur_repair_path_id), "traverse", str(tmp_file_index), screen_xml_file)
            else:
                screen_xml_path = os.path.join(self.path, str(self.cur_repair_path_id), "traverse", str(autoseq_id + 1), screen_xml_file)
            with open(screen_xml_path, encoding='utf-8') as f:
                xml_str = f.read()
            root = xeTree.fromstring(xml_str)
            screen_ori_nodes = parse_nodes_patch(root)

            for node in screen.nodes:
                node_str = ''
                for attrib_key in node.attrib:
                    node_str = node_str + node.attrib[attrib_key]
                node_str = node_str.replace(' ', '').lower()
                for ori_node in screen_ori_nodes:
                    ori_node_str = ''
                    for attrib_key in ori_node.attrib:
                        ori_node_str = ori_node_str + ori_node.attrib[attrib_key]
                    ori_node_str = ori_node_str.replace(' ', '').lower()
                    if node_str == ori_node_str:
                        node.attrib = ori_node.attrib
                        break
            candidate_model_screens.append(screen)

        for seq in candidate_seqs:
            print("segment details currently being repaired: ")
            for node in original_seq_node:
                node_str = str(node.attrib)
                print(node_str)

            print("details of the candidate sequences currently being compared")
            seq_node = []
            seq_screen = []
            for edge in seq:
                end_screen = candidate_model_screens[edge.end_id - 1]
                seq_screen.append(end_screen)
                tmp_node = candidate_model_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                seq_node.append(tmp_node)
                tmp_str = str(tmp_node.attrib)
                print(tmp_str)

            # calculate the similarity between null and non-null events
            # sim = min(sim(screenx, screeny)) + min(sim(edgem, edgen))
            null_screen_sim = 1
            null_edge_sim = 1
            print("calculate the similarity between null and non-null events")
            print("finding minimum screen similarity ...")
            for i in range(0, len(original_seq_screen)):
                for j in range(0, len(seq_screen)):
                    screen1 = original_seq_screen[i]
                    screen2 = seq_screen[j]
                    tmp_screen_sim = get_screen_sim_score(screen1, screen2)
                    if tmp_screen_sim < null_screen_sim:
                        null_screen_sim = tmp_screen_sim
            print("the minimum screen similarity is: " + str(null_screen_sim))

            print("finding minimum edge similarity ...")
            for i in range(0, len(original_seq_node)):
                for j in range(0, len(seq_node)):
                    edge1 = original_seq_node[i]
                    edge2 = seq_node[j]
                    tmp_flag, tmp_edge_sim = get_node_sim(edge1, edge2, self.wv2_model)
                    if tmp_edge_sim < null_edge_sim:
                        null_edge_sim = tmp_edge_sim
            print("the minimum edge similarity is: " + str(null_edge_sim))

            null_sim = (null_screen_sim + null_edge_sim) / 2
            print("the similarity between null and non-null events is: " + str(null_sim))

            cur_sim, match_seq = self.calculate_seq_trans_prob(original_seq, seq, candidate_model_screens, null_sim)


            print("cur_sim = " + str(cur_sim))
            print("len(match_seq) = " + str(len(match_seq)))

            if cur_sim > max_score or (cur_sim == max_score and abs(len(match_seq) - 1) <= abs(len(target_seq) - 1)):
                max_score = cur_sim
                target_seq = []
                for elem in match_seq:
                    target_seq.append(elem)

        print("\nmax_score = " + str(max_score) + '\n')


        self.match_detail_info.append(len(target_seq))
        self.flag = len(target_seq)
        if self.flag == 0:
            self.tmp_model = candidate_model

        target_seq_bounds = []
        for seq in target_seq:
            tmp_node = candidate_model_screens[seq.begin_id - 1].get_node_by_id(seq.node_id)
            tmp_bounds = [tmp_node.loc_x, tmp_node.loc_y, tmp_node.width, tmp_node.height]
            target_seq_bounds.append(tmp_bounds)

        for bounds in target_seq_bounds:
            self.update_pre_event_sequences.append(bounds)

        if len(target_seq) == 1:
            for pre_target_seq in self.target_seqs:
                pre_target_seq.append(target_seq_bounds[0])

        if len(target_seq) >= 2:
            total_pre_target_seqs = []
            total_pre_match_score = []
            total_target_bounds = []
            for seq in candidate_seqs:
                if len(seq) == len(target_seq):
                    if seq[-1].begin_id == target_seq[-1].begin_id and seq[-1].end_id == target_seq[-1].end_id and seq[-1].node_id == target_seq[-1].node_id:
                        pre_seqs_match_score = 0

                        pre_seq_node = []
                        pre_seq_screen = []
                        for edge in seq[0:-1]:
                            end_screen = candidate_model_screens[edge.end_id - 1]
                            pre_seq_screen.append(end_screen)
                            tmp_node = candidate_model_screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                            pre_seq_node.append(tmp_node)

                        pre_original_seq = []
                        for i in range(1, len(seq)):
                            if (autoseq_id - i) >= 0:
                                pre_original_seq.append(self.edges[autoseq_id - i])
                        pre_original_seq_node = []
                        pre_original_seq_screen = []
                        for edge in pre_original_seq:
                            end_screen = self.screens[edge.end_id - 1]
                            pre_original_seq_screen.append(end_screen)
                            tmp_node = self.screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                            pre_original_seq_node.append(tmp_node)

                        for i in range(0, len(pre_original_seq_node)):
                            screen_sim = get_screen_sim_score(pre_original_seq_screen[i], pre_seq_screen[i])
                            tmp_flag, node_sim = get_node_sim(pre_original_seq_node[i], pre_seq_node[i], self.wv2_model)
                            total_sim = (screen_sim + node_sim) / 2
                            pre_seqs_match_score += total_sim

                        if len(total_pre_match_score) == 0:
                            total_pre_match_score.append(pre_seqs_match_score)
                            total_pre_target_seqs.append(pre_seq_node)
                        else:
                            tmp_index = -1
                            for i in range(0, len(total_pre_match_score)):
                                if pre_seqs_match_score > total_pre_match_score[i]:
                                    tmp_index = i
                                    total_pre_match_score.insert(i, pre_seqs_match_score)
                                    total_pre_target_seqs.insert(i, pre_seq_node)
                                    break
                            if tmp_index == -1:
                                total_pre_match_score.append(pre_seqs_match_score)
                                total_pre_target_seqs.append(pre_seq_node)

            for pre_seq in total_pre_target_seqs:
                cur_target_bounds = []
                for elem_node in pre_seq:
                    elem_bounds = [elem_node.loc_x, elem_node.loc_y, elem_node.width, elem_node.height]
                    cur_target_bounds.append(elem_bounds)
                cur_target_bounds.append(target_seq_bounds[-1])
                total_target_bounds.append(cur_target_bounds)

            print("total_target_bounds = " + str(total_target_bounds))
            print("len(total_target_bounds) = " + str(len(total_target_bounds)))

            cur_target_seqs = []
            for cur_target_seq in self.target_seqs:
                cur_target_seqs.append(cur_target_seq)

            for pre_target_seq in cur_target_seqs:
                cur_pre_target_seq = []
                for pre_elem in pre_target_seq:
                    cur_pre_target_seq.append(pre_elem)

                for cur_elem in total_target_bounds[0]:
                    pre_target_seq.append(cur_elem)

                for cur_seq in total_target_bounds[1:len(total_target_bounds)]:
                    new_target_seq = []
                    for pre_elem in cur_pre_target_seq:
                        new_target_seq.append(pre_elem)
                    for cur_elem in cur_seq:
                        new_target_seq.append(cur_elem)
                    self.target_seqs.append(new_target_seq)

        return max_score

    def save_work(self):
        result_dir = os.path.join(self.path, str(self.cur_repair_path_id), 'result')
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        count = 1
        for target_seq in self.target_seqs:
            self.cur_screen_id = -1
            self.screen_id = 1
            close_app(self.package_name)
            open_app(self.package_name)

            if len(target_seq) != 0:
                tmp_dir = os.path.join(result_dir, str(count))

                print("replay event sequence from app's main screen to the screen where the test begins")
                if len(self.pre_event_sequences) != 0:
                    event_seq_replay(self.pre_event_sequences, False, "")
                    time.sleep(2)
                count += 1

                screens, edges, record_node_attrib = event_seq_replay(target_seq, True, tmp_dir)
                codes = []
                for i in range(0, len(record_node_attrib)):
                    xml_file_path = os.path.join(tmp_dir, "scenario_screens", str(i+1)+".xml")
                    code = locate_element(record_node_attrib[i], xml_file_path)
                    codes.append(code)
                write_repaired_test_script(codes, tmp_dir, self.caps)

                # visual(screens, edges, tmp_dir)

    def work(self):
        for i in range(1, self.total_scenario_num + 1):
            self.cur_repair_path_id = i
            print("The current repair path: " + str(self.cur_repair_path_id) + ".")

            print("Read current scenario model.")
            current_dir = os.getcwd()
            tmp = "demo/tmpFIles/ext/scenario"
            tmp_path_list = tmp.split("/")
            scenario_model_path = os.path.join(current_dir, *tmp_path_list, str(i), "scenario_model")
            f = open(scenario_model_path, 'rb')
            self.scenario_model = pickle.load(f)
            print("Read successful.")

            if i==1:
                self.base_scenario_model = self.scenario_model

            source_screens = []
            for key in self.scenario_model.screens:
                screen = self.scenario_model.screens[key]
                # patch
                screen_xml_file = str(key) + '.xml'
                screen_xml_path = os.path.join(current_dir, *tmp_path_list, str(i), "scenario_screens", screen_xml_file)
                with open(screen_xml_path, encoding='utf-8') as f:
                    xml_str = f.read()
                root = xeTree.fromstring(xml_str)
                screen_ori_nodes = parse_nodes_patch(root)

                for node in screen.nodes:
                    node_str = ''
                    for attrib_key in node.attrib:
                        node_str = node_str + node.attrib[attrib_key]
                    node_str = node_str.replace(' ', '').lower()
                    for ori_node in screen_ori_nodes:
                        ori_node_str = ''
                        for attrib_key in ori_node.attrib:
                            ori_node_str = ori_node_str + ori_node.attrib[attrib_key]
                        ori_node_str = ori_node_str.replace(' ', '').lower()
                        if node_str == ori_node_str:
                            node.attrib = ori_node.attrib
                            break
                source_screens.append(screen)

            self.screens = source_screens

            source_edges = self.scenario_model.edges
            self.edges = source_edges

            for edge in self.edges:
                tmp_node = self.screens[edge.begin_id - 1].get_node_by_id(edge.node_id)
                self.ori_event_detail.append(str(tmp_node.attrib))

            print("The total number of rounds matched: " + str(len(self.edges)) + ".")
            autoseq_match_result = []
            length = 0

            print("Loading the trained word2vec model for subsequent similarity calculations ...")
            tmp = "w2v/w2v-googleplay.model"
            tmp_path_list = tmp.split("/")
            load_path = os.path.join(current_dir, *tmp_path_list)
            try:
                self.wv2_model = word2vec.KeyedVectors.load_word2vec_format(load_path, binary=True)
            except UnicodeDecodeError:
                self.wv2_model = word2vec.KeyedVectors.load(load_path)
            print("Finished loading.")

            self.sims[i] = 0
            for autoseq_id in range(0, len(self.edges)):
                print("Current round: " + str(autoseq_id + 1))
                cur_rep_sim = self.find_matched_seq(autoseq_id)
                cur_ext_sim = get_ext_sim(self.base_scenario_model, self.scenario_model, autoseq_id)
                self.sims[i] += (cur_rep_sim*cur_ext_sim)
                elem = []
                for seq in self.target_seqs[0][length : ]:
                    elem.append(seq)
                autoseq_match_result.append(elem)
                length = len(self.target_seqs[0])
            self.sims[i] /= len(self.edges)

            time.sleep(1)

            self.save_work()

            # parameter clear
            self.update_pre_event_sequences = []
            self.target_seqs = [[]]
            self.flag = -1
            self.tmp_model = None
            self.ori_event_detail = []

        max_index = -1
        max_sim = 0
        for index in self.sims:
            print("path id: " + str(index) + ", sim: " + str(self.sims[index]))
            if self.sims[index] > max_sim:
                max_sim = self.sims[index]
                max_index = index
        print("The recommended path id is: " + str(max_index) + ".")

        current_dir = os.getcwd()
        tmp1 = "demo/tmpFIles/rep"
        tmp_path_list1 = tmp1.split("/")
        tmp2 = "/result/1/repaired_script.py"
        tmp_path_list2 = tmp2.split("/")
        recommend_script_path = os.path.join(current_dir, *tmp_path_list1, str(max_index), *tmp_path_list2)
        shutil.copy(recommend_script_path, self.result_save_path)




