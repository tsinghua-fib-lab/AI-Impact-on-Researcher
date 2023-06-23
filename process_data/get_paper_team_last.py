import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm
import numpy as np

data_dir=os.path.join('..','OAGdata')
paper_data_dir=os.path.join(data_dir,'papers')

with open(os.path.join('.',f'paper_selected_dict_title_abstract.pkl'),'rb') as f:
    paper_selected_dict_title_abstract=pickle.load(f)
with open(os.path.join('.',f'paper_selected_dict_venue.pkl'),'rb') as f:
    paper_selected_dict_venue=pickle.load(f)
with open(os.path.join('.',f'paper_selected_dict_year.pkl'),'rb') as f:
    paper_selected_dict_year=pickle.load(f)

with open(os.path.join('.','author_career.pkl'),'rb') as f:
    author_role=pickle.load(f)

def count(i):
    paper_dict=dict()

    df = pd.read_json(os.path.join(paper_data_dir,f'mag_papers_{i}.txt'),chunksize=10000,lines=True)

    chunk_count=0
    for chunk in df:
        for _,line in chunk.iterrows():
            try:
                paper_id=line['id']
                authors=line['authors']
                year=line['year']
            except:
                continue
               
            if (paper_id in paper_selected_dict_title_abstract) and (paper_id in paper_selected_dict_venue) and (paper_id in paper_selected_dict_year):
            
                leading_num=1
                supporting_num=0
                for author in authors[:-1]:
                    try:
                        author_id=author['id']
                        role=author_role[author_id]
                    except:
                        supporting_num+=1
                        continue

                    if year<role[3]:
                        supporting_num+=1
                    else:
                        leading_num+=1
                                          
                paper_dict[paper_id]=(supporting_num,leading_num)

    del df

    with open(os.path.join('.',f'paper_team_last_{i}.pkl'),'wb') as f:
        pickle.dump(paper_dict,f)

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
        with open(os.path.join('.',f'paper_team_last_{i}.pkl'),'rb') as f:
            local_paper_team=pickle.load(f)
        paper_team.update(local_paper_team)
    
    paper_team=dict()
    for i in tqdm(range(51)):
        merge(i)

    with open(os.path.join('.',f'paper_team_last.pkl'),'wb') as f:
        pickle.dump(paper_team,f)

    for i in tqdm(range(51)):
        os.remove(os.path.join('.',f'paper_team_last_{i}.pkl'))