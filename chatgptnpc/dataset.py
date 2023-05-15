import pandas as pd

class make_dataset():
    def __init__(self, data_dir):
        self.data = pd.read_csv(data_dir, sep='\t')
        
    def npc_load(self, npc_name):
        return self.data[self.data['npc'] == npc_name]
        