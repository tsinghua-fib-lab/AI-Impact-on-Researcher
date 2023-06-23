import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

data_dir=os.path.join('..','OAGdata')
paper_data_dir=os.path.join(data_dir,'papers')

with open(os.path.join('.','fos_index_level1.pkl'),'rb') as f:
    fos_index=pickle.load(f)
    
with open(os.path.join('.',f'paper_selected_dict_title_abstract.pkl'),'rb') as f:
    paper_selected_dict_title_abstract=pickle.load(f)
with open(os.path.join('.',f'paper_selected_dict_venue.pkl'),'rb') as f:
    paper_selected_dict_venue=pickle.load(f)
with open(os.path.join('.',f'paper_selected_dict_year.pkl'),'rb') as f:
    paper_selected_dict_year=pickle.load(f)
    
def count(i):
    save_chunksize=100
    result_df=pd.DataFrame(columns=('paper_id','fos_level1'))
    save_count=0

    df = pd.read_json(os.path.join(paper_data_dir,f'mag_papers_{i}.txt'),chunksize=10000,lines=True)
    f = open(os.path.join('.',f'paper_fos_level1_{i}.txt'), 'a')

    chunk_count=0
    for chunk in df:
        for _,line in chunk.iterrows():
            try:
                paper_id=line['id']
                foses=line['fos']
            except:
                continue
            
            if isinstance(foses,list):
                if (paper_id in paper_selected_dict_title_abstract) and (paper_id in paper_selected_dict_venue) and (paper_id in paper_selected_dict_year):
                    level1_list=list()
                    for fos in foses:
                        try:
                            level1_id=fos_index[fos['name']]
                            level1_list.extend(level1_id)
                        except:
                            continue

                    if len(level1_list)>0:
                        result_df=result_df.append({'paper_id':paper_id,'fos_level1':list(set(level1_list))},ignore_index=True)
                        save_count+=1

                        if save_count==save_chunksize:
                            for _,result_line in result_df.iterrows():
                                f.writelines(result_line.to_json()+'\n')
                            result_df.drop(index=result_df.index,inplace=True)
                            save_count=0

        chunk_count+=1
        if chunk_count==-1:
            break

    del df
    
    for _,result_line in result_df.iterrows():
        f.writelines(result_line.to_json()+'\n')
    result_df.drop(index=result_df.index,inplace=True)
    f.close()
   
if __name__ == '__main__':
    import multiprocessing

    MAX_THREADS=51
    p = multiprocessing.Pool(MAX_THREADS)
    result=list()

    for i in range(51):
        result.append(p.apply_async(count,args=(i,)))

    for obj in tqdm(result):
        obj.get()

    f=open(os.path.join('.','paper_fos_level1.txt'),'a')
    def merge(i):
        with open(os.path.join('.',f'paper_fos_level1_{i}.txt'),'r') as f_src:
            f.writelines(f_src.read())

    for i in tqdm(range(51)):
        merge(i)

    for i in tqdm(range(51)):
        os.remove(os.path.join('.',f'paper_fos_level1_{i}.txt'))