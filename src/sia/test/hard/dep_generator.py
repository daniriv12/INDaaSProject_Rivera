import networkx as nx
from ft import *
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

class DependencyGenerator:
    def __init__(self, xmlFile):
        doc = ElementTree.parse(xmlFile)
        root = doc.getroot()
        self.faultTree = nx.DiGraph()

        for child in root:
            tmpID = child.attrib['id']
            if tmpID not in self.faultTree.node:
                self.faultTree.add_node(tmpID)
                self.faultTree.node[tmpID] = TreeNode()
                self.faultTree.node[tmpID].ID = tmpID

            
            self.faultTree.node[tmpID].gate = child.find('gate').text

            for depItem in child.findall('dep'):
                tmpID = depItem.text
                if tmpID not in self.faultTree.node:
                    self.faultTree.add_edge(tmpID, child.attrib['id'])
                    self.faultTree.node[tmpID] = TreeNode()
                    self.faultTree.node[tmpID].ID = tmpID
                else:
                    self.faultTree.add_edge(tmpID, child.attrib['id'])
                self.faultTree.node[tmpID].parentList\
                        .append(self.faultTree.node[child.attrib['id']])
                self.faultTree.node[child.attrib['id']].childList\
                        .append(self.faultTree.node[tmpID])
