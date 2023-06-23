## Step1: Environment Setup
Operating system
- Ubuntu 20.04.5 LTS

Softwares
- python==3.9.13
- numpy==1.21.5
- scipy==1.9.3
- pandas==1.4.3
- matplotlib==3.5.2
- seaborn==0.12.0
- tqdm==4.64.0

You can use Anaconda to build an environment
``` bash
wget -c https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
./Anaconda3-2022.05-Linux-x86_64.sh
conda create -n AIimpact python==3.9
conda activate AIimpact
```

Then you can use pip to install the packages
``` bash
pip install PackageName==Version
```

## Step2: Data Download
Please download the MAG data from https://www.aminer.cn/oag-2-1, which takes about 500GB disk space.

The downloaded file should looks like:
OAGdata
&emsp;|--affiliations
&emsp;&emsp;|--mag_affiliations.txt
&emsp;|--authors
&emsp;&emsp;|--mag_authors_0.txt
&emsp;&emsp;|--...
&emsp;&emsp;|--mag_authors_4.txt
&emsp;|--papers
&emsp;&emsp;|--mag_papers_0.txt
&emsp;&emsp;|--...
&emsp;&emsp;|--mag_papers_50.txt
&emsp;|--venues
&emsp;&emsp;|--mag_venues.txt

## Step3: Data Pre-process
Please use python code provided in /process_data.

```bash
python select_paper_venue.py
python select_paper_title_abstract.py
python select_paper_year.py

python fos_index.py
python get_paper_root_fos.py
python get_paper_root_fos_multi.py

python select_author_fos.py
# You may adjust MAX_THREADS=xx in the code according to the number of CPUs on your server
```

## Step4：Data Process
Please use python code provided in /process_data.

```bash
python get_paper_year.py
python get_citation_reference.py
python paper_citation_year.py
python get_author_citation_year.py
python get_author_paper_year.py

python get_author_career.py
python get_paper_team_last.py

python get_paper_fos_level1.py
python get_vocabulary.py

python get_paper_venue.py
# You may adjust MAX_THREADS=xx in the code according to the number of CPUs on your server
```

## Step6: Result Analysis
You can simply run the Jupyter Notebooks (.ipynb) to analyse the results and obtain the figures in the paper.