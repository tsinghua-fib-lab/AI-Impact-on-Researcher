import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','OAGdata')
paper_data_dir=os.path.join(data_dir,'papers')

with open(os.path.join('.',f'paper_selected_dict_title_abstract.pkl'),'rb') as f:
    paper_selected_dict_title_abstract=pickle.load(f)
with open(os.path.join('.',f'paper_selected_dict_venue.pkl'),'rb') as f:
    paper_selected_dict_venue=pickle.load(f)
with open(os.path.join('.',f'paper_selected_dict_year.pkl'),'rb') as f:
    paper_selected_dict_year=pickle.load(f)

with open(os.path.join('.','paper_classify_union.pkl'),'rb') as f:
    paper_classify=pickle.load(f)
    
fos_list=set(['geology','chemistry','materials science','biology','physics','medicine'])
with open(os.path.join('.','paper_root_fos_level0_multi.pkl'),'rb') as f:
    paper_root_fos=pickle.load(f)
with open(os.path.join('.','root_fos_level0_order.pkl'),'rb') as f:
    root_fos=pickle.load(f)

def fun(i):
    author_dict=dict()  
    df = pd.read_json(os.path.join(paper_data_dir,f'mag_papers_{i}.txt'),chunksize=10000,lines=True)

    for chunk in df:
        for _,line in chunk.iterrows():
            try:
                paper_id=line['id']
                paper_year=line['year']
                paper_authors=line['authors']
                classify=paper_classify[paper_id]
                foses=paper_root_fos[paper_id]
            except:
                continue
                
            fos_names=set([root_fos[fos] for fos in foses])
            inter_set=fos_names&fos_list
            if len(inter_set)==0:
                continue
            
            if (paper_id in paper_selected_dict_title_abstract) and (paper_id in paper_selected_dict_venue) and (paper_id in paper_selected_dict_year):
                for author in paper_authors:
                    try:
                        author_id=author['id']
                        if author_id not in author_dict:
                            author_dict[author_id]=[0,9999,9999,9999,9999,0,-1,-1]
                        author_dict[author_id][0]+=1
                        if paper_year<author_dict[author_id][1]:
                            author_dict[author_id][1]=paper_year
                        if paper_year>author_dict[author_id][5]:
                            author_dict[author_id][5]=paper_year
                        if classify==1 and paper_year<author_dict[author_id][4]:
                            author_dict[author_id][4]=paper_year
                    except:
                        continue

                try:
                    author_first=paper_authors[0]
                    author_id=author_first['id']
                    if paper_year<author_dict[author_id][2]:
                        author_dict[author_id][2]=paper_year
                        author_dict[author_id][-2]=classify
                except:
                    pass

                try:
                    author_last=paper_authors[-1]
                    author_id=author_last['id']
                    if paper_year<author_dict[author_id][3]:
                        author_dict[author_id][3]=paper_year
                        author_dict[author_id][-1]=classify
                except:
                    pass
           
    with open(os.path.join('.',f'author_career_{i}.pkl'),'wb') as f:
        pickle.dump(author_dict,f)

if __name__ == '__main__':
    import multiprocessing
    import warnings
    warnings.filterwarnings('ignore')

    MAX_THREADS=26
    p = multiprocessing.Pool(MAX_THREADS)
    result=list()
    
    for i in range(51):
        result.append(p.apply_async(fun,args=(i,)))

    for obj in tqdm(result):
        obj.get()

    def merge(i):
        with open(os.path.join('.',f'author_career_{i}.pkl'),'rb') as f:
            local_author_role=pickle.load(f)
            for author_id,local_record in local_author_role.items():
                if author_id not in author_role:
                    author_role[author_id]=local_record
                else:
                    record=author_role[author_id]
                    record[0]+=local_record[0]
                    if local_record[1]<record[1]:
                        record[1]=local_record[1]
                    if local_record[2]<record[2]:
                        record[2]=local_record[2]
                        record[-2]=local_record[-2]
                    if local_record[3]<record[3]:
                        record[3]=local_record[3]
                        record[-1]=local_record[-1]
                    if local_record[4]<record[4]:
                        record[4]=local_record[4]
                    if local_record[5]>record[5]:
                        record[5]=local_record[5]
                    author_role[author_id]=record

    author_role=dict()
    for i in tqdm(range(51)):
        merge(i)
        
    with open(os.path.join('.',f'author_career.pkl'),'wb') as f:
        pickle.dump(author_role,f)

    for i in tqdm(range(51)):
        os.remove(os.path.join('.',f'author_career_{i}.pkl'))