from parse.file_parsing import parsing
from analysis.solMatrix import solMatEquv
import matplotlib.pyplot as plt

def main(filename, option):
    filename = "file/" + filename
    element, _, command = parsing(filename)
    volTR, curTR, _ = solMatEquv(element, command, 'TR')
    #volBE, curBE, _ = solMatEquv(element, command, 'BE')
    """
    l1, = plt.plot(_, curTR['c1'], 'b')
    l2, = plt.plot(_, curBE['c1'], 'r')
    """
    """
    l1, = plt.plot(_, curTR['l1'], 'b')
    l2, = plt.plot(_, curBE['l1'], 'r')
    """
    """
    l1, = plt.plot(_, volTR['1'], 'black')
    l2, = plt.plot(_, volTR['2'], 'red')
    l3, = plt.plot(_, volTR['3'], 'yellow')
    l4, = plt.plot(_, volTR['4'], 'green')
    l5, = plt.plot(_, volTR['5'], 'orange')
    l6, = plt.plot(_, volTR['6'], 'brown')
    plt.legend(handles = [l1, l2, l3, l4, l5, l6], labels = ['node1', 'node2', 'node3', 'node4', 'node5', 'node6'])
    """
    l1, = plt.plot(_, volTR['9'], 'b')
    l2, = plt.plot(_, volTR['7'], 'r')
    plt.xlabel('time')
    plt.ylabel('V')
    #plt.ylim(min(volTR['1'][1:]) - 0.2, max(volTR['1'][1:]) + 0.2)
    plt.legend(handles=[l1, l2], labels = ['Vin', 'Vout'])
    plt.title('opamp')
    plt.show()	
    
if __name__ == "__main__":
    filename = raw_input("input filename:")
    main(filename, "TR")
