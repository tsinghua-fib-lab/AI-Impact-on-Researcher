import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import pickle
from tqdm import tqdm

with open(os.path.join('.','citation_dict.pkl'),'rb') as f:
    citation_dict=pickle.load(f)
with open(os.path.join('.','paper_year.pkl'),'rb') as f:
    paper_year=pickle.load(f)
with open(os.path.join('.','paper_selected_dict_title_abstract.pkl'),'rb') as f:
    paper_selected_dict_title_abstract=pickle.load(f)
with open(os.path.join('.','paper_selected_dict_venue.pkl'),'rb') as f:
    paper_selected_dict_venue=pickle.load(f)

paper_citation_year=dict()
for paper,citation in tqdm(citation_dict.items()):
    if (paper in paper_selected_dict_title_abstract) and (paper in paper_selected_dict_venue):
        citation_year=dict()
        for cite_paper in citation:
            try:
                year=paper_year[cite_paper]
            except:
                continue

            if year not in citation_year:
                citation_year[year]=1
            else:
                citation_year[year]+=1
        paper_citation_year[paper]=citation_year
        
with open(os.path.join('.','paper_citation_year.pkl'),'wb') as f:
    pickle.dump(paper_citation_year,f) 