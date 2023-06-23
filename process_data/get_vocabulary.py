import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
    
MAG_data_dir=os.path.join('..','MAGdata')
fos_list=pd.read_table(os.path.join(MAG_data_dir,'FieldsOfStudy.txt'),header=None,names=['ID','Rank','NormalizedName','DisplayName','MainType','Level','PaperCount','PaperFamilyCount','CitationCount','CreatedDate'])

fos_index=dict()
fos_count=np.uint32(0)
for _,line in fos_list.iterrows():
    if line['Level']==1:
        fos_index[line['ID']]=fos_count
        fos_count+=np.uint32(1)

with open(os.path.join('.','paper_classify_union.pkl'),'rb') as f:
    paper_classify=pickle.load(f)
with open(os.path.join('.','paper_root_fos_level0_multi.pkl'),'rb') as f:
    paper_root_fos=pickle.load(f)
with open(os.path.join('.','root_fos_level0.pkl'),'rb') as f:
    root_fos=pickle.load(f)

fos_list=['geology','chemistry','materials science','biology','physics','medicine']

df = pd.read_json(os.path.join('.','paper_fos_level1.txt'),lines=True)

fos_num=292
vocabulary=dict()
for fos,fos_name in root_fos.items():
    vocabulary[fos]=[np.zeros(fos_num,dtype=np.uint32),np.zeros(fos_num,dtype=np.uint32)]

paper_count=0
for i,line in tqdm(df.iterrows()):
    try:
        paper_id=line['paper_id']
        foses=paper_root_fos[paper_id]
        classify=paper_classify[paper_id]
    except:
        continue

    paper_count+=1
    related_foses=[fos_index[related_fos] for related_fos in line[1]]        
    indices_unique,indices_count=np.unique(related_foses,return_counts=True)
    indices_count=np.uint32(indices_count)
    for fos in foses:
        vocabulary[fos][classify][indices_unique]+=indices_count
            
with open(os.path.join('.','vocabulary.pkl'),'wb') as f:
    pickle.dump(vocabulary,f)