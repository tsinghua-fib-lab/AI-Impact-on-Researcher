import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','OAGdata')
paper_data_dir=os.path.join(data_dir,'papers')

def count(i):
    df = pd.read_json(os.path.join(paper_data_dir,f'mag_papers_{i}.txt'),chunksize=10000,lines=True)
    citation_dict=dict()
    
    chunk_count=0
    for chunk in df:
        for _,line in chunk.iterrows():
            try:
                paper_id=line['id']
                references=line['references']
            except:
                continue

            if isinstance(references,list):
                for ref in references:
                    if ref not in citation_dict:
                        citation_dict[ref]=[paper_id]
                    else:
                        citation_dict[ref].append(paper_id)


        chunk_count+=1
        if chunk_count==-1:
            break

    del df

    with open(os.path.join('.',f'citation_dict_{i}.pkl'),'wb') as f:
        pickle.dump(citation_dict,f)

if __name__ == '__main__':
    import multiprocessing

    MAX_THREADS=51
    p = multiprocessing.Pool(MAX_THREADS)
    result=list()

    for i in range(51):
        result.append(p.apply_async(count,args=(i,)))

    for obj in tqdm(result):
        obj.get()

    def citation_merge(i):
        with open(os.path.join('.',f'citation_dict_{i}.pkl'),'rb') as f:
            local_citation_dict=pickle.load(f)
        
        for paper,citations in local_citation_dict.items():
            if paper in citation_dict:
                citation_dict[paper].extend(citations)
            else:
                citation_dict[paper]=citations

    citation_dict=dict()
    for i in tqdm(range(51)):
        citation_merge(i)

    with open(os.path.join('.',f'citation_dict.pkl'),'wb') as f:
        pickle.dump(citation_dict,f)

    del citation_dict

    for i in tqdm(range(51)):
        os.remove(os.path.join('.',f'citation_dict_{i}.pkl'))