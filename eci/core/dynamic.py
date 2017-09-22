
import heapq
from algorithm import Collective_Influence
temp_fidder = '../temp/'

def reduce_reinert(g,eci_dic,n=50,output_batch=500,model_name="test.csv"):
    gn = g.copy()

    print "begin reduce function"
    nid_btach_list = list()
    f = open(temp_fidder + model_name, 'wb')
    while (len(eci_dic) != 0 ):
        if (len(eci_dic) < n):
            n = len(eci_dic)

        topn = heapq.nlargest(n, eci_dic.values())
        nids = value_find_Key(topn,eci_dic) # [eci_dic.keys()[eci_dic.values().index(index)] for index in topn]
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
        print "reduce number : " + str(len(eci_dic)) + " maxci : " + str(topn[0])

    f.close()
    pass

def key_with_value(value,dicts):
    for k, v in dicts.iteritems():
        if v == value:
            return k
    return None


def value_find_Key(values,dicts):
    result = []
    for v in values:
        k = key_with_value(v,dicts)
        if not k:
            raise ValueError("value can't find")
        del dicts[k]
        result.append(k)

    return result
