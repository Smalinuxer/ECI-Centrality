# -*- coding: UTF-8 -*-
from load import *
from core.algorithm import *

g = load_data("../data/test_data.csv")
eci_dic = Collective_Influence(g,2)

print eci_dic