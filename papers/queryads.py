import ads
import os

# ADS API token (use a GitHub secret!)
ads.config.token = 'nn83fQwsJBVIqknjUkyckgY1vaZxDmVnkx7kbd7U'

# Retrieve ADS API token from environment variable
ads_token = os.getenv("ADS_API_TOKEN")

if not ads_token:
    raise ValueError("ADS_API_TOKEN is not set!")

# Configure ADS with the token
ads.config.token = ads_token


def print_citation_entry(f,titlestring,varname,citation_count,countername='FirstAuthorCitations'):
    print('%{0}'.format(titlestring),file=f)
    print('\\newcount\{}'.format(varname),file=f)
    print('\{0}={1}'.format(varname, citation_count),file=f)
    print('\\advance\{0} by \{1}\n'.format(countername,varname),file=f)


f = open('papers/publications.tex','w')
print('\\newcount\FirstAuthorCitations',file=f)
print('\FirstAuthorCitations=0\n',file=f)

# First author bibcodes
bibcodes = [
    "2016MNRAS.463.1952P",
    "2016PhRvD..94l3013P",
    "2019MNRAS.488.1462P",
    "2019MNRAS.490.3616P",
    "2020MNRAS.494L..11P",
    "2021MNRAS.500..838P",
    "2021NatAs...5..251P",
    "2022MNRAS.510.6201P",
    "2022MNRAS.514.1266P",
    "2024MNRAS.530.4378P",
    "2024MNRAS.531..751P",
    "exp: a Python/C++ package for basis function expansion methods in galactic dynamics"
]

varnames = []
nfirstauthor = len(bibcodes)
letters = [chr(i) for i in range(65, 65+nfirstauthor)]

# Query ADS for citation counts
for bibcode in bibcodes:
    varnames.append('FirstAuthor'+letters.pop(0))
    papers = list(ads.SearchQuery(bibcode=bibcode, fl=["citation_count", "title"]))
    if papers:
        paper = papers[0]
        print(f"Title: {paper.title[0]}")
        print(f"Citations: {paper.citation_count}")
        print(varnames[-1], '=', paper.citation_count)
        print_citation_entry(f,{paper.title[0]},varnames[-1],paper.citation_count)
    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0)

f.close()


f = open('papers/publications.tex','a')
print('\n',file=f)
print('\\newcount\StudentAuthorCitations',file=f)
print('\StudentAuthorCitations=0\n',file=f)

# List of Bibcodes for the papers you want to query
# You can find these bibcodes in ADS for each paper
bibcodes = [
    "2022MNRAS.512..160R",
    "2022MNRAS.513L..46D",
    "2023MNRAS.518..774L",
    "2023MNRAS.521.1757J",
    "2024MNRAS.531.3524Y",
    "{\tt commensurability}: a Python package for classifying astronomical orbits based on their toroid volume",
    "2024arXiv241111972G"
]

varnames = []
nfirstauthor = len(bibcodes)
letters = [chr(i) for i in range(65, 65+nfirstauthor)]

# Query ADS for citation counts
for bibcode in bibcodes:
    varnames.append('StudentAuthor'+letters.pop(0))
    papers = list(ads.SearchQuery(bibcode=bibcode, fl=["citation_count", "title"]))
    if papers:
        paper = papers[0]
        print(f"Title: {paper.title[0]}")
        print(f"Citations: {paper.citation_count}")
        print(varnames[-1], '=', paper.citation_count)
        print_citation_entry(f,{paper.title[0]},varnames[-1],paper.citation_count,'StudentAuthorCitations')
    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0,'StudentAuthorCitations')

f.close()


f = open('papers/publications.tex','a')
print('\n',file=f)
print('\\newcount\CoauthorCitations',file=f)
print('\CoauthorCitations=0\n',file=f)

# List of Bibcodes for the papers you want to query
# You can find these bibcodes in ADS for each paper
bibcodes = [
    "2014ApJ...792...64B",
    "2021MNRAS.501.5408W",
    "2021MNRAS.508L..26P",
    "2024arXiv240207986H",
    "2024JOSS....9.6906N"
]

varnames = []
nfirstauthor = len(bibcodes)
letters = [chr(i) for i in range(65, 65+nfirstauthor)]

# Query ADS for citation counts
for bibcode in bibcodes:
    varnames.append('Coauthor'+letters.pop(0))
    papers = list(ads.SearchQuery(bibcode=bibcode, fl=["citation_count", "title"]))
    if papers:
        paper = papers[0]
        print(f"Title: {paper.title[0]}")
        print(f"Citations: {paper.citation_count}")
        print(varnames[-1], '=', paper.citation_count)
        print_citation_entry(f,{paper.title[0]},varnames[-1],paper.citation_count,'CoauthorCitations')
    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0,'CoauthorCitations')

f.close()


f = open('papers/publications.tex','a')
print('\n',file=f)
print('\\newcount\CollaboratorCitations',file=f)
print('\CollaboratorCitations=0\n',file=f)

# List of Bibcodes for the papers you want to query
# You can find these bibcodes in ADS for each paper
bibcodes = [
    "2009ApJ...701..306E",
    "2023ApJ...942...18C",
    "2023MNRAS.518.4138E",
    "2023ApJ...946...10P",
    "2023MNRAS.520.4779L",
    "2024MNRAS.532.2657B"
]

varnames = []
nfirstauthor = len(bibcodes)
letters = [chr(i) for i in range(65, 65+nfirstauthor)]

# Query ADS for citation counts
for bibcode in bibcodes:
    varnames.append('Collaborator'+letters.pop(0))
    papers = list(ads.SearchQuery(bibcode=bibcode, fl=["citation_count", "title"]))
    if papers:
        paper = papers[0]
        print(f"Title: {paper.title[0]}")
        print(f"Citations: {paper.citation_count}")
        print(varnames[-1], '=', paper.citation_count)
        print_citation_entry(f,{paper.title[0]},varnames[-1],paper.citation_count,'CollaboratorCitations')
    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0,'CollaboratorCitations')

f.close()