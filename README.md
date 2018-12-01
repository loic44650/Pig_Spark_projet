# Projet Pagerank

## Dataset

Des données d'entrée sur lesquelles réaliser le page rank sont disponibles dans le dossier [/data](/data).

Les tests ci-dessous sont réalisés sur le jeu de donné [univnantes](/data/univnantes) qui a été généré à partir du script [domain_graph.py](/scripts/domain_graph.py) à l'aide de la commande suivante:

> `python domain_graph.py https://www.univ-nantes.fr/`

## Pig

### Execution

Le calcul du pagerank à l'aide de Pig se fait en exécutant le script [pig_pagerank.py](/Pig/pig_pagerank.py) via la commande suivante:

> `pig pig_pagerank.py inputData nbIter damping`

> - *inputData*: path of input data file</br>
> - *nbIter*: number of pagerank iterations</br>
> - *damping*: Pagerank damping value (between 0 and 1)

exemple d'utilisation:

> `pig pig_pagerank.py ../data/univnantes 10 0.85`

### Output

Les données de chaque itération du pagerank sont crées dans un dossier /Pig/output_nomDataset.

Une repréentation lisible du résultat de la dernière itéartion est est également crée: /Pig/pagerank_nomDataset
