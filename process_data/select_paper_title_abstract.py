import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','OAGdata')
paper_data_dir=os.path.join(data_dir,'papers')

def fun(i):
    selected_dict=dict()  
    df = pd.read_json(os.path.join(paper_data_dir,f'mag_papers_{i}.txt'),chunksize=10000,lines=True)

    for chunk in df:
        for _,line in chunk.iterrows():
            try:
                paper_id=line['id']
                title=line['title'].lower()
                indexed_abstract=eval(line['indexed_abstract'])
                length=indexed_abstract['IndexLength']
                words=indexed_abstract['InvertedIndex']
            except:
                continue
                
            temp=[None] * length

            try:
                for word,indexes in words.items():
                    for index in indexes:
                        temp[index]=word
                abstract=(' '.join(temp)).lower()
            except:
                continue

            if ord(max(title))<=126 and ord(min(title))>=32 and ord(max(abstract))<=126 and ord(min(abstract))>=32:
                selected_dict[paper_id]=1
                
    with open(os.path.join('.',f'selected_dict_title_abstract_{i}.pkl'),'wb') as f:
        pickle.dump(selected_dict,f)

if __name__ == '__main__':
    import multiprocessing
    import warnings
    warnings.filterwarnings('ignore')

    MAX_THREADS=51
    p = multiprocessing.Pool(MAX_THREADS)
    result=list()
    
    for i in range(51):
        result.append(p.apply_async(fun,args=(i,)))

    for obj in tqdm(result):
        obj.get()

    def merge(i):
        with open(os.path.join('.',f'selected_dict_title_abstract_{i}.pkl'),'rb') as f:
            local_selected_dict=pickle.load(f)

        selected_dict.update(local_selected_dict)

    selected_dict=dict()
    for i in tqdm(range(51)):
        merge(i)
        
    with open(os.path.join('.',f'paper_selected_dict_title_abstract.pkl'),'wb') as f:
        pickle.dump(selected_dict,f)

    del selected_dict

    for i in tqdm(range(51)):
        os.remove(os.path.join('.',f'selected_dict_title_abstract_{i}.pkl'))