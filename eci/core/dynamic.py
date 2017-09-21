
import heapq
from algorithm import Collective_Influence
temp_fidder = '../temp/'

def reduce_reinert(g,eci_dic,n=50,output_batch=500,model_name="test.csv"):
    dict().values()
    gn = g.copy()

    print "begin reduce function"
    nid_btach_list = list()
    f = open(temp_fidder + model_name, 'wb')
    print "len(eci_dic) : " + str(len(eci_dic))
    while (len(eci_dic) != 0 ):
        if (len(eci_dic) < n):
            n = len(eci_dic)

        topn = heapq.nlargest(n, eci_dic.values())
        nids = [eci_dic.keys()[eci_dic.values().index(index)] for index in topn]
        nid_btach_list += nids
        if (len(nid_btach_list) == output_batch):
            batch = ','.join(nid_btach_list)
            final = model_name + ("," + batch)
            f.writelines(final)
            nid_btach_list = list()
            pass

        if (len(nid_btach_list) > output_batch):
            raise ValueError('nid_btach_list more than 500')

        for nid in nids :
            gn.remove_node(nid)

        eci_dic = Collective_Influence(gn, 2)
        print "reduce number : " + str(len(eci_dic)) + " maxci : " + topn[0]

    f.close()
    # mydict.keys()[mydict.values().index(16)]

    # while ()

    pass