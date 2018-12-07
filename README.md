# Projet Pagerank

## Dataset

Des données d'entrée sur lesquelles réaliser le pagerank sont disponibles dans le dossier [/data](/data).<br>Ce dossier contient un jeu de données nommé [example](data/example) très petit qui nous permet de nous assurer rapidement de la justesse de nos algorithmes. En voici la représentation sous forme de graphe:

[example]: images/example.png "example graph"
![alt text][example]

Le dossier contient également un jeu de données plus conséquent nommé [univnantes](data/univnantes) qui nous permet d'effectuer un pagerank sur l'ensemble des pages du site de l'université de Nantes. Il a été généré à partir du script [domain_graph.py](/scripts/domain_graph.py) à l'aide de la commande suivante:

> `python domain_graph.py https://www.univ-nantes.fr/`

## Pig

#### Execution

Le calcul du pagerank à l'aide de Pig se fait en exécutant le script [pig_pagerank.py](/Pig/pig_pagerank.py) via la commande suivante:

> `pig pig_pagerank.py inputData nbIter damping`
> - *inputData*: path of input data file</br>
> - *nbIter*: number of pagerank iterations</br>
> - *damping*: Pagerank damping value (between 0 and 1)

Exemple d'utilisation:

> `pig pig_pagerank.py ../data/univnantes 10 0.85`

#### Output

Les données de chaque itération du pagerank sont crées dans un dossier /Pig/output_nomDataset.

Une repréentation lisible du résultat de la dernière itéartion est est également crée: /Pig/pagerank_nomDataset

## Spark

#### Execution

Le calcul du pagerank à l'aide de Spark se fait en exécutant le script [spark_pagerank.py](/Spark/spark_pagerank.py) via la commande suivante:

> `spark-submit spark_pagerank.py inpuData nbIter damping`
> - *inputData*: path of input data file</br>
> - *nbIter*: number of pagerank iterations</br>
> - *damping*: Pagerank damping value (between 0 and 1)

Exemple d'utilisation:

> `spark-submit spark_pagerank.py ../data/univnantes 10 0.85`

#### Output

Les données du pagerank de la dernière itéartion sont écrite dans un fichier: /Spark/pagerank_nomDataset

## Statistiques

// TODO
