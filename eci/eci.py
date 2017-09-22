# -*- coding: UTF-8 -*-
from load import *
from core.algorithm import Collective_Influence
from core.dynamic import reduce_reinert
import os.path
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle

temp_file_ci_init = '../temp/ci.txt'

if len(sys.argv) != 3:
    print "python eci.py *.csv clear|noclear"
    sys.exit()

model_name = sys.argv[1]
if sys.argv[2] == "clear":
    print "clear cache file"
    os.remove(temp_file_ci_init)
    pass

g = load_data("../data/%s.csv" % model_name )
if not os.path.isfile(temp_file_ci_init) :
    eci_dic = Collective_Influence(g,2)
    f = open(temp_file_ci_init, 'wb')
    pickle.dump(eci_dic, f)
    f.close()
eci_dic = pickle.load(open(temp_file_ci_init, "r"))

# eci_dic = Collective_Influence(g,2)
reduce_reinert(g,eci_dic,"%s.csv.out" % model_name)

# print eci_dic