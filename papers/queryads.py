import ads
import os
from datetime import datetime

import bibcodes as biblog

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

# Get the current date and time
current_time = datetime.now()

# Format the date and time as a string
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print('%Updated: {0}\n'.format(formatted_time),file=f)
formatted_time = current_time.strftime("%Y-%m-%d")
print('\\newcommand{\publicationdatecheck}{%s}\n' % formatted_time,file=f)


total_citations = 0
print('\\newcount\FirstAuthorCitations',file=f)
print('\FirstAuthorCitations=0\n',file=f)

bibcodes = biblog.get_first_author_bibcodes()

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
        total_citations += paper.citation_count
    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0)

f.close()


f = open('papers/publications.tex','a')
print('\n',file=f)
print('\\newcount\StudentAuthorCitations',file=f)
print('\StudentAuthorCitations=0\n',file=f)

# get student-led bibcodes
bibcodes = biblog.get_student_led_bibcodes()

varnames = []
nstudentauthor = len(bibcodes)
letters = [chr(i) for i in range(65, 65+nstudentauthor)]

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
        total_citations += paper.citation_count

    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0,'StudentAuthorCitations')

f.close()


f = open('papers/publications.tex','a')
print('\n',file=f)
print('\\newcount\CoauthorCitations',file=f)
print('\CoauthorCitations=0\n',file=f)

# get coauthor bibcodes
bibcodes = biblog.get_coauthor_bibcodes()

varnames = []
ncoauthor = len(bibcodes)
letters = [chr(i) for i in range(65, 65+ncoauthor)]

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
        total_citations += paper.citation_count

    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0,'CoauthorCitations')

f.close()


f = open('papers/publications.tex','a')
print('\n',file=f)
print('\\newcount\CollaboratorCitations',file=f)
print('\CollaboratorCitations=0\n',file=f)


bibcodes = biblog.get_collaborative_bibcodes()

varnames = []
ncollaborator = len(bibcodes)
letters = [chr(i) for i in range(65, 65+ncollaborator)]

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
        total_citations += paper.citation_count

    else:
        print(f"No data found for bibcode {bibcode}")
        print_citation_entry(f,{bibcode},varnames[-1],0,'CollaboratorCitations')

f.close()


f = open('papers/publications.tex','a')

# count the total citations
print('\n',file=f)
print('\\newcount\TotalCitations',file=f)
print('\TotalCitations=0\n',file=f)
print('\\advance\TotalCitations by \FirstAuthorCitations',file=f)
print('\\advance\TotalCitations by \StudentAuthorCitations',file=f)
print('\\advance\TotalCitations by \CoauthorCitations',file=f)
print('\\advance\TotalCitations by \CollaboratorCitations',file=f)

# count the total papers
print('\n',file=f)
print('\\newcount\FirstAuthorPublications',file=f)
print('\FirstAuthorPublications={0}\n'.format(nfirstauthor),file=f)

print('\\newcount\StudentPublications',file=f)
print('\StudentPublications={0}\n'.format(nstudentauthor),file=f)

print('\\newcount\CoauthorPublications',file=f)
print('\CoauthorPublications={0}\n'.format(ncoauthor),file=f)

print('\\newcount\CollaborativePublications',file=f)
print('\CollaborativePublications={0}\n'.format(ncollaborator),file=f)

print('\\newcount\AllPublications',file=f)
print('\AllPublications=\FirstAuthorPublications',file=f)
print('\\advance\AllPublications by \StudentPublications',file=f)
print('\\advance\AllPublications by \CoauthorPublications',file=f)
print('\\advance\AllPublications by \CollaborativePublications\n',file=f)

print('\\newcount\AllCollaborativePublications',file=f)
print('\AllCollaborativePublications=\CoauthorPublications',file=f)
print('\\advance\AllCollaborativePublications by \CollaborativePublications',file=f)


print('% {0} Total Citations'.format(total_citations),file=f)

f.close()

