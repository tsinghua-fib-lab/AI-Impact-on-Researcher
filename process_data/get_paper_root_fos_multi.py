import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
from tqdm import tqdm

with open(os.path.join('.',f'root_fos_level0.pkl'),'rb') as f:
    root_fos=pickle.load(f)
root_fos_index=list()
for fos in root_fos:
    root_fos_index.append(fos)
num_root_fos=len(root_fos_index)

with open(os.path.join('.','paper_root_fos_score_level0.pkl'),'rb') as f:
    paper_root_fos_score=pickle.load(f)
    
paper_root_fos=dict()
for paper,scores in tqdm(paper_root_fos_score.items()):
    paper_fos=list()

    for i in range(num_root_fos):
        if scores[i]>0:
            paper_fos.append(root_fos_index[i])
    paper_root_fos[paper]=paper_fos
    
with open(os.path.join('.','paper_root_fos_level0_multi.pkl'),'wb') as f:
    pickle.dump(paper_root_fos,f)