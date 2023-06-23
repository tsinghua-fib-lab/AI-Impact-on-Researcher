import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','OAGdata')
paper_data_dir=os.path.join(data_dir,'papers')

def count(i):
    paper_year=dict()
    df = pd.read_json(os.path.join(paper_data_dir,f'mag_papers_{i}.txt'),chunksize=10000,lines=True)

    chunk_count=0
    for chunk in df:
        for _,line in chunk.iterrows():
            try:
                paper_id=line['id']
                year=line['year']
            except:
                continue

            if isinstance(year,int):
                paper_year[paper_id]=year

        chunk_count+=1
        if chunk_count==-1:
            break

    del df

    with open(os.path.join('.',f'paper_year_{i}.pkl'),'wb') as f:
        pickle.dump(paper_year,f)

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
        with open(os.path.join('.',f'paper_year_{i}.pkl'),'rb') as f:
            local_paper_year=pickle.load(f)

        paper_year.update(local_paper_year)

    paper_year=dict()
    for i in tqdm(range(51)):
        merge(i)
        
    with open(os.path.join('.',f'paper_year.pkl'),'wb') as f:
        pickle.dump(paper_year,f)

    del paper_year

    for i in tqdm(range(51)):
        os.remove(os.path.join('.',f'paper_year_{i}.pkl'))