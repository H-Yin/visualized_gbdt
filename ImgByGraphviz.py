#!/bin/python
# -*- coding=utf-8 -*-
import sys, re
import getopt as opt
from graphviz import Digraph


FEATURE_PATH = ''
MODEL_PATH = ''
BOOSTER_NUM = None
DEPTH = None
OUTPUT_PATH = ''

def usage():
    help_text= '''
Usage: ImgByGraphviz [OPTION] args 
       ImgByGraphviz help
options:
    -m, --model MODEL_PATH     model's dump file, specified.
    -f, --feature FEATURE_PATH feature's file, specified.
    -n, --num BOOSTER_NUM      the BOOSTER_NUM’th booster. 
    -d, --depth DEPTH          the depth of tree.
    -o, --output OUTPUT_PATH   output path.
    '''
    print help_text

def getOpts(argv):
    global FEATURE_PATH, MODEL_PATH, BOOSTER_NUM, DEPTH, OUTPUT_PATH
    try:
        options, args = opt.getopt(argv[1:], '-f:-m:-n:-d:-o:-h', ['feature=','model=','num=','depth=','output=','help'])
        for op, value in options:
            if op in ('-h','--help'):
                usage()
                sys.exit()
            if op in ('-f', '--feature'):
                FEATURE_PATH = value
            if op in ('-m', '--model'):
                MODEL_PATH = value
            if op in ('-n', '--num'):
                BOOSTER_NUM = int(value)
            if op in ('-d', '--depth'):
                DEPTH = int(value)
            if op in ('-o', '--output'):
                OUTPUT_PATH = value
        if FEATURE_PATH == '' or MODEL_PATH == '':
            usage()
            sys.exit()
    except opt.GetoptError:
        usage()
        sys.exit()

def getFeature(path):
    keyMap = {}
    with open(path, 'r') as feature_file:
        for feature in feature_file:
            (key, name, num) = tuple(feature.strip().split("\t"))
            keyMap[key] = name.strip()
    # print(keyMap)
    return keyMap

def getModel(path):
    booster_list = []
    nodeMap = {}
    with open(path, 'r') as model_file:
        for node in model_file:
            if node.startswith('booster'):
                booster_list.append(nodeMap)
                nodeMap = {}
                continue
            node_items = re.split(r"[:<>\[\] ]", node.strip("\t").strip("\n"))
            node_depth = node.count('\t') + 1
            if len(node_items) > 2:
                # splited node
                nodeNum = int(node_items[0])
                featureKey = node_items[2]
                featureValue = float(node_items[3])
                params = node_items[5]
            else:
                # leaf node
                nodeNum = int(node_items[0])
                featureKey = ""
                featureValue = ""
                params = node_items[1]
            nodeMap[nodeNum] = (featureKey, featureValue, params, node_depth)
        #  print(nodeMap)
    booster_list.append(nodeMap)
    return booster_list[1:]

def toGraph(booster_list, feature_map):
    gbdt = Digraph(comment='GBDT boosters', format='pdf')
    gbdt.graph_attr['rankdir'] = 'LR'
    i = BOOSTER_NUM
    #for i in range(len(booster_list[booster_num:booster_num+1])):
    with gbdt.subgraph(name = "booster" + str(i+1)) as booster:
        for key, node in booster_list[i].items():
            if DEPTH is not None and node[3] > DEPTH:
		continue
	    name = "%s-%s" % (str(i+1),str(key))
            tag = 'num=%s, depth=%s\n' % (str(key), str(node[3]))
	    if node[0] == '':
                booster.node(name, tag + node[2])
	    else:
                booster.node(name, feature_map.get(node[0]) +"<" + str(node[1])+ '\n'+ tag + node[2])
            	if DEPTH is not None and node[3] >= DEPTH:
                    continue
		children_node = re.split("[,=]", node[2])
		left_node = "%s-%s" % (str(i+1), children_node[1])
		right_node = "%s-%s" % (str(i+1), children_node[3])
		booster.edge(name, left_node, 'Yes')
		booster.edge(name, right_node, 'No')
    # default output file
    output = 'test'
    if OUTPUT_PATH != '':
	output = OUTPUT_PATH
    gbdt.render(output)

def toJson(booster_list, feature_map):
    
    def getNode(nodeMap, nId):
        node = {}
        if nodeMap[nId][0] == '':
            node['name'] = nodeMap[nId][2]
            # node['size']
        else:
            node['name'] = feature_map.get(nodeMap[nId][0])[0]
            node['text'] = nodeMap[nId][2]
            children_node = re.split("[,=]", nodeMap[nId][2])
            left_node = int(children_node[1])
            right_node = int(children_node[3])
            node['children'] = [getNode(nodeMap, left_node), getNode(nodeMap, right_node)]
        return node

    temp_list = []
    #  for booster in booster_list:
        #  temp_list.append(getNode(booster, 0))

    temp_list.append(getNode(booster_list[0], 0))
    return json.dumps(temp_list)


def buildTree(nodeMap):
    tree = {}
    pass


if __name__ == '__main__':
    # get options
    getOpts(sys.argv)
    # get Feature
    feature_map = getFeature(FEATURE_PATH)
    # get Model
    booster_list = getModel(MODEL_PATH)
    # to Json
    #  print toJson(booster_list, feature_map)
    toGraph(booster_list, feature_map)
