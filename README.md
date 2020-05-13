# conjugate

- `python conjugate.py -h`
```
usage: conjugate.py [-h] language [verb] [mode] [tense] [person]

Conjugate verbs.

positional arguments:
  language    select the language [fr, pt, en, es, it]
  verb        optional or show list of tenses
  mode
  tense       use quotes if multiple words
  person      optional or show all persons

optional arguments:
  -h, --help  show this help message and exit
```
- `python conjugate.py fr`
```
indicatif présent
indicatif passé composé
indicatif imparfait
[..]
```
- `python conjugate.py pt`
```
indicativo presente
indicativo pretérito perfeito composto
indicativo pretérito imperfeito
[..]
```
- `python conjugate.py fr conjuguer indicatif present`
```
je conjugue
tu conjugues
il conjugue
nous conjuguons
vous conjuguez
ils conjuguent
```
- `python conjugate.py pt conjugar indicativo presente nos`
```
nós conjugamos
```
