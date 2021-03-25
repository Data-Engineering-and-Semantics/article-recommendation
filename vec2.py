from Bio import Entrez
import bs4
import urllib.request
import nltk
nltk.download('punkt')
nltk.download('stopwords')

Entrez.email = 'your.email@example.com'
handle = Entrez.esearch(db="pmc", term="(COVID-19) AND Review[Title]", retmax="100", sort="relevance" )
record = Entrez.read(handle)
idlist = record["IdList"]
print(idlist)
print(len(idlist))

article = ""
for ss in idlist:
    scrapped_data = urllib.request.urlopen("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="+ss+"&email=turkiabdelwaheb@hotmail.fr")
    article += str(scrapped_data.read())

parsed_article = bs4.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

processed_article = article_text.lower()
punc = '''!()[]{};:'"\,<>./?@#$%^&*_~='''

for ele in processed_article: 
    if ele in punc: 
        processed_article = processed_article.replace(ele, "") 
print(processed_article)

all_sentences = nltk.sent_tokenize(processed_article)
all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

from nltk.corpus import stopwords
for i in range(len(all_words)):
    all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
    all_words[i] = [w.encode('ascii', 'ignore') for w in all_words[i]]
    all_words[i] = [w.decode('ascii', 'ignore') for w in all_words[i]]
with open('vocabulary.txt', 'w') as filehandle:
    for listitem in all_words:
        for item in listitem:
            filehandle.write('%s\n' % item)