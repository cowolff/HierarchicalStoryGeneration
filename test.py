import torch as th
import fairseq

PATH = "/users/cowolff/Downloads/models/fusion_checkpoint.pt"
model = th.load(PATH)
model.keys()