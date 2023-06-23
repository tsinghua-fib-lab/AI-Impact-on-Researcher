import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','OAGdata')
paper_data_dir=os.path.join(data_dir,'papers')
target_level=0

with open(os.path.join('.',f'fos_index_level{target_level}.pkl'),'rb') as f:
    fos_index=pickle.load(f)

with open(os.path.join('.',f'root_fos_level{target_level}.pkl'),'rb') as f:
    root_fos=pickle.load(f)
root_fos_index=list()
for fos in root_fos:
    root_fos_index.append(fos)
num_root_fos=len(root_fos_index)
    
def count(i):
    paper_root_fos_score=dict()
    df = pd.read_json(os.path.join(paper_data_dir,f'mag_papers_{i}.txt'),chunksize=10000,lines=True)

    chunk_count=0
    for chunk in df:
        for _,line in chunk.iterrows():
            try:
                paper_id=line['id']
                foses=line['fos']
            except:
                continue

            if isinstance(foses,list):
                temp_count=dict()
                for fos in foses:
                    try:
                        root_ids=fos_index[fos['name']]
                        weight=fos['w']
                    except:
                        continue
                    
                    for root_id in root_ids:
                        if root_id not in temp_count:
                            temp_count[root_id]=weight
                        else:
                            temp_count[root_id]+=weight
                    
                if len(temp_count)>0:
                    classify_foses=sorted(temp_count.items(),key=lambda x:x[1],reverse=True)
                    classify_foses=dict(classify_foses)
                    paper_root_fos_score[paper_id]=[(classify_foses[root_fos_index[k]] if root_fos_index[k] in classify_foses else 0) for k in range(num_root_fos)]

        chunk_count+=1
        if chunk_count==-1:
            break

    del df

    with open(os.path.join('.',f'paper_root_fos_score_level{target_level}_{i}.pkl'),'wb') as f:
        pickle.dump(paper_root_fos_score,f)
        
if __name__ == '__main__':
    import multiprocessing

    MAX_THREADS=51
    p = multiprocessing.Pool(MAX_THREADS)
    result=list()

    for i in range(51):
        result.append(p.apply_async(count,args=(i,)))

    for obj in tqdm(result):
        obj.get()

    def merge(i):        
        with open(os.path.join('.',f'paper_root_fos_score_level{target_level}_{i}.pkl'),'rb') as f:
            local_paper_root_fos_score=pickle.load(f)

        paper_root_fos_score.update(local_paper_root_fos_score)

    paper_root_fos_score=dict()
    for i in tqdm(range(51)):
        merge(i)
        
    with open(os.path.join('.',f'paper_root_fos_score_level{target_level}.pkl'),'wb') as f:
        pickle.dump(paper_root_fos_score,f)

    for i in tqdm(range(51)):
        os.remove(os.path.join('.',f'paper_root_fos_score_level{target_level}_{i}.pkl'))