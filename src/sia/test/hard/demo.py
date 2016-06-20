import matplotlib.pyplot as plt
import graphviz as gv
from cra import *
from dep_generator import *
import sys
import re


def get_probability(A, root):
        
    currentNode = A.get_node(root)



    if(not A.get_node(root).attr['color']): #We don't colour them until we estimate their probabilities, that's how we know the root has not been estimated
        
        for i in range(len(A.successors(currentNode))):
            edge =  A.get_edge(currentNode,  A.successors(currentNode)[i] )
            if (edge.attr['label']): #already done
                pass
            else: 
                label = str(int(100/len(A.successors(currentNode)))) + '%'
                A.add_edge(currentNode, A.successors(currentNode)[i], fontcolor = 'purple', fontsize = 10)
                get_probability(A,A.successors(currentNode)[i])


        probabilities = []
        tmpProb =[]
        for i in range(len(A.successors(currentNode))):
            if (edge.attr['label']):
                
                edge =  A.get_edge(currentNode, A.successors(currentNode)[i])
                edgeValue = float(edge.attr['label'][:-1])/100

                nodeLabel = A.get_node(A.successors(currentNode)[i]).attr['label']
                tmp = nodeLabel.index('\n')
                nodeValue = float(nodeLabel[tmp:])
                # tmpProb.append(edgeValue*nodeValue) #revisit
                tmpProb.append(1*nodeValue) #revisit
        probabilities.append(tmpProb)



        if len(probabilities[0]) == 1:
            Prob = probabilities[0][i] #here we will put the actual probability of that node failing, still need to decide how to set that

        else:
            tmp = 1
            for i in range(len(probabilities[0])):
                tmp = tmp * probabilities[0][i] #replace 0.1 with the actual probability
            Prob = tmp


        label = str(str(currentNode) + ": \n" + str(Prob))
        A.add_node(A.get_node(currentNode), color='green', style='filled', label=label, fontsize =10.0)





if __name__ == '__main__':

    
    if(len(sys.argv)>1):
        generator = DependencyGenerator(sys.argv[1])
    else:
        generator = DependencyGenerator("result2.xml")

    c = CRA(generator.faultTree)
    service = "ownCloud"
    risk_groups = c.minimal_cut_set_approach(generator.faultTree, service)

    G = generator.faultTree
    A = nx.nx_agraph.to_agraph(G)
    A = A.reverse()
    A.layout(prog='dot')

    TEMPORAL_PROBABILITY = 0.01 #replace with some sort of smarter probabilities 



    #dealing with probabilities - depending on the node type we assign a probability associated to it. note that this requires extra information
    #on the node. For now we have a dictionary of predefined values associated to node type, and we specify node type in its name

    probabilities = {'VM':0.1, 'SW':0.05, 'NM':0.1, 'RT':0.05, 'SE': 0.01} #virtual machines, switches, machines, router, service

    RGProbabilities = []
    for risk_group in risk_groups:    
        current = []
        if len(risk_group) == 1:
            RG = (risk_group[0])
            Prob = (0.01) #here we will put the actual probability of that node failing, still need to deide how to set that
            current = {RG:Prob}
            RGProbabilities.append(current)

        else:
            tmp = 1
            RG = []
            current = []
            for i in range(len(risk_group)):
                RG.append(risk_group[i])
                tmp = tmp * (0.01) #replace 0.1 with the actual probability
            Prob = tmp
            final = ""
            for item in RG:
                final += (item + ',') 
            current = {final:Prob}
            RGProbabilities.append(current) 



    tmp = 1
    for item in RGProbabilities:
        tmp = tmp * (1-item.values()[0])
    serviceFailureProbability = 1-tmp

    # for node in A.nodes():
    #     A.add_node(A.get_node(node), style='filled',color='green',)

    for edge in A.edges():
        A.add_edge(A.get_edge(edge[0],edge[1])) #add style here if I want, such as colour or anything else


    
    for i in range(len(risk_groups)):
        risk_nodes = []
        for j in range(len(risk_groups[i])):
            if (len(risk_groups[i]) == 1):
                color = "red"
            else:
                color = "yellow"
            currentNode = A.get_node(risk_groups[i][j])
            risk_nodes.append(currentNode)
            label = str(str(currentNode) + ": \n" + str(TEMPORAL_PROBABILITY))
            A.add_node(currentNode, style='filled',color=color, label=label, fontsize= 10.0)
        # A.add_subgraph(risk_nodes, name = 'cluster_' + str(i), color=color) # NOT WORKING I DON'T KNOW WHY 


    for i in range(len(risk_groups)):
        for j in range(len(risk_groups[i])):

            

            currentNode = A.get_node(risk_groups[i][j])
            parents = A.predecessors(currentNode)

            for parentNode in parents:
                # label = str(100/len(A.successors(parentNode)))+'%'
                label = str(100/len(risk_groups[i]))+'%'
                A.add_edge(A.get_edge(parentNode,currentNode),label=label, fontsize=10.0, fontcolor='purple')
            # A.add_node(currentNode, style='filled',color=color)



    print "Individual probabilities for each risk group:"
    for item in RGProbabilities:
        print item

    print "Probability of a service outtage (any risk group failing):"
    chance = (serviceFailureProbability*100)
    print "%.2f" % chance + '%'


    someNode = A.get_node('Ceph')
    
    get_probability(A, A.get_node('ownCloud'))
    

    currentNode = A.get_node(service)
    A.add_node(currentNode, style='filled',color='blue', label=service + '\n' + str(round(chance,2)) + '%', fontsize= 10.0)


    A.write('file.dot')
    if (len(sys.argv)>1):
        i = re.search("\d", sys.argv[1])
        A.draw('results/graph' + str(sys.argv[1][i.start()]) + '.png')
    else:
        A.draw('results/graph.png')



  


