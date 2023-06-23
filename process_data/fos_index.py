import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm

MAG_data_dir=os.path.join('..','MAGdata')
fos_list=pd.read_table(os.path.join(MAG_data_dir,'FieldsOfStudy.txt'),header=None,names=['ID','Rank','NormalizedName','DisplayName','MainType','Level','PaperCount','PaperFamilyCount','CitationCount','CreatedDate'])
fos_child=pd.read_table(os.path.join(MAG_data_dir,'FieldOfStudyChildren.txt'),header=None,names=['ID','ChildID'])

target_level=0

root_fos=dict()
for _,line in fos_list.iterrows():
    if line['Level']==target_level:
        root_fos[line['ID']]=line['NormalizedName']
        
with open(os.path.join('.',f'root_fos_level{target_level}.pkl'),'wb') as f:
    pickle.dump(root_fos,f)
        
fos_index=dict()
for i,line in tqdm(fos_list.iterrows()):
    fos_name=line['NormalizedName']
    fos_id=line['ID']
    fos_level=line['Level']
    
    if fos_level>=target_level:
        current=[fos_id]
        for level in range(fos_level-target_level):
            parent=list()
            for ID in current:
                parent.extend(fos_child[fos_child['ChildID']==ID]['ID'].tolist())
            current=list(set(parent))
        fos_index[fos_name]=current

with open(os.path.join('.',f'fos_index_level{target_level}.pkl'),'wb') as f:
    pickle.dump(fos_index,f)

target_level=1

root_fos=dict()
for _,line in fos_list.iterrows():
    if line['Level']==target_level:
        root_fos[line['ID']]=line['NormalizedName']
        
with open(os.path.join('.',f'root_fos_level{target_level}.pkl'),'wb') as f:
    pickle.dump(root_fos,f)
        
fos_index=dict()
for i,line in tqdm(fos_list.iterrows()):
    fos_name=line['NormalizedName']
    fos_id=line['ID']
    fos_level=line['Level']
    
    if fos_level>=target_level:
        current=[fos_id]
        for level in range(fos_level-target_level):
            parent=list()
            for ID in current:
                parent.extend(fos_child[fos_child['ChildID']==ID]['ID'].tolist())
            current=list(set(parent))
        fos_index[fos_name]=current

with open(os.path.join('.',f'fos_index_level1.pkl'),'wb') as f:
    pickle.dump(fos_index,f)