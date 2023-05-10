# Cloze-Quality-Estimation
Offical code and data of Cloze Quality Estimation for Language Assessment (EACL 2023). ([Paper](https://aclanthology.org/2023.findings-eacl.39/))

## Data

Cloze tests and corresponded annotations are saved in 
`data/cloze_tests/*.json`
and
`data/cela.json`
.

The formats are as follows:
### Cloze Tests
Each cloze test is saved in a single json file, which looks like:

```json
*.json
{
    'source': (str) to indicate the source of article and option generation method
    'article': (str) an article with several blanks,
    'options': (list) list of options blanks,
    'answers': (list) list of answers, to indicate the correct answer for each blank
}
```

```json
options[i]: (list) four options for blank_i
options[i][j]: (str) an English word as option
```

```json
answers[i]: (str) "A", "B", "C", or "D"
```
### CELA
All annotation result is saved in cela.json file, which looks like:

```json
cela.json
{
    (str) source: (dict) annotation
}
```

```json
annotation
{
    'rel': (dict) annotation for reliability,
    'val': (val) annotation for validity
}
```

```json
annotation for reliability/validity
{
    (str) question_index: (str) annotation result
}
```
for `annotation for reliability`, `annotation result` is `T(rue)` or `F(alse)`; for `annotation for validity`, `annotation result` is `R(eading)`, `G(rammar)`, or `N(ot_valid)`.