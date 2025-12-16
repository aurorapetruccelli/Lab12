
from model.model import Model

model = Model()
model.build_weighted_graph(2000)
model.get_edges_weight_min_max()
model.count_edges_by_threshold(4)

model.calcolo_cammino_minimo(4)

