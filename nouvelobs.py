import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from tabulate import tabulate
import re
import argparse
import unidecode
import sys

parser = argparse.ArgumentParser(description='Conjugate verbs.')
parser.add_argument('language', help='select the language [fr, pt]')
parser.add_argument('verb', nargs='?', default=None, help='optional or show list of tenses')
parser.add_argument('mode', nargs='?', default=None)
parser.add_argument('tense', nargs='?', default=None, help='use quotes if multiple words')
parser.add_argument('person', nargs='?', default=None, help='optional or show all persons')
args = parser.parse_args()

if args.verb:
  for arg in ['mode', 'tense']:
    if not args.__dict__[arg]:
      sys.exit('missing %s' % arg)

Tense = namedtuple('Tense', ['mode', 'tense', 'conjugations'])
Conjugation = namedtuple('Conjugation', ['person', 'form'])

class French:
  def __init__(self, verb):
    if verb is None:
      verb = 'avoir'

    url = 'https://la-conjugaison.nouvelobs.com/du/verbe/%s.php' % verb
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    self.tenses = [self.create_tense(t) for t in soup.find_all("div", attrs={"class": "tempstab"})]

  def person(self, mode, index, prefix):
    if re.search("^(je|j'|que je|que j')", prefix):
      return "je"
    if re.search("^(tu|que tu)", prefix):
      return "tu"
    if re.search("^(il|qu'il)\\s", prefix):
      return "il/elle"
    if re.search("^(nous|que nous)", prefix):
      return "nous"
    if re.search("^(vous|que vous)", prefix):
      return "vous"
    if re.search("^(ils|qu'ils)", prefix):
      return "ils/elles"
    if mode == 'impératif':
      return ['tu', 'nous', 'vous'][index]
    return None

  def prefix(self, conjugation):
    return str(conjugation.previous_element) if type(conjugation.previous_element).__name__ == 'NavigableString' else ''

  def create_tense(self, t):
    mode = t.find_previous_sibling("h2", attrs={"class": "mode"}).text.lower().strip()
    return Tense(
      mode = mode,
      tense = t.find("h3").text.lower().strip(),
      conjugations = [Conjugation(
        person = self.person(mode, i, self.prefix(c)),
        form = (self.prefix(c) + c.text).strip()
      ) for i, c in enumerate(t.find("div", attrs={"class": "tempscorps"}).find_all("b"))]
    )

class Portuguese:
  def __init__(self, verb):
    if verb is None:
      verb = 'haver'

    url = 'https://la-conjugaison.nouvelobs.com/portugais/verbe/%s.php' % verb
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    self.tenses = [self.create_tense(t) for t in soup.find_all("div", attrs={"class": "tempstab"})]

  def person(self, mode, index, prefix):
    if re.search("^(eu|se eu|quando je)", prefix):
      return "eu"
    if re.search("^(tu|se tu|quando tu)", prefix):
      return "tu"
    if re.search("^(ele|se ele|quando ele)\\s", prefix):
      return "ele/ela"
    if re.search("^(nós|se nós|quando nós)", prefix):
      return "nós"
    if re.search("^(vós|se vós|quando vós)", prefix):
      return "vós"
    if re.search("^(eles|se eles|quando eles)", prefix):
      return "eles/elas"
    if mode == 'imperativo':
      return ['tu', 'ele/ela', 'nós', 'vós', 'eles/elas'][index]
    return None

  def prefix(self, conjugation):
    return str(conjugation.previous_element) if type(conjugation.previous_element).__name__ == 'NavigableString' else ''

  def create_tense(self, t):
    mode = re.sub('\\s\\(.*?\\)', '', t.find_previous_sibling("h2", attrs={"class": "mode"}).text.lower().strip())
    return Tense(
      mode = mode,
      tense = re.sub('\\s\\(.*?\\)', '', t.find("h3").text.lower().strip()),
      conjugations = [Conjugation(
        person = self.person(mode, i, self.prefix(c)),
        form = (self.prefix(c) + c.text).strip()
      ) for i, c in enumerate(t.find("div", attrs={"class": "tempscorps"}).find_all("b"))]
    )

language = None
if args.language == 'fr':
  language = French(args.verb)
elif args.language == 'pt':
  language = Portuguese(args.verb)
else:
  sys.exit('unknown language %s' % args.language)

if args.verb is None:
  [print(t.mode, t.tense) for t in language.tenses]
else:
  query = [t for t in language.tenses if unidecode.unidecode(t.mode).lower() == unidecode.unidecode(args.mode).lower() and unidecode.unidecode(t.tense).lower() == unidecode.unidecode(args.tense).lower()]
  if query:
    tense = query[0]
    forms = [c.form for c in tense.conjugations if args.person == None or unidecode.unidecode(c.person).lower() == unidecode.unidecode(args.person).lower()]
    print('\n'.join(forms))
