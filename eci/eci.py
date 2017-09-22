# -*- coding: UTF-8 -*-
from load import *
from core.algorithm import Collective_Influence
from core.dynamic import reduce_reinert
import os.path
try:
    import cPickle as pickle
except ImportError:
    import pickle

temp_file_ci_init = '../temp/ci.txt'

g = load_data("../data/test_data.csv")
if not os.path.isfile(temp_file_ci_init) :
    eci_dic = Collective_Influence(g,2)
    f = open(temp_file_ci_init, 'wb')
    pickle.dump(eci_dic, f)
    f.close()
eci_dic = pickle.load(open(temp_file_ci_init, "r"))

# eci_dic = Collective_Influence(g,2)
reduce_reinert(g,eci_dic)

# print eci_dic