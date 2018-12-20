from __future__ import print_function

import os
import re
import sys
from operator import add
from datetime import datetime
import numpy as np

from pyspark.sql import SparkSession


def computeContribs(id, urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    yield(id, 0.0) # Prevent empty values
    for url in urls:
        yield (url, rank / num_urls)

def parseLinks(line):
    parts = line.split(" ")
    links = map(lambda l : l[1:-1], parts[2][1:-1].split(","))
    links = filter(lambda l : l != "", links)
    return [(parts[0], links) ,(parts[0], float(parts[1]))]

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: spark-submit spark_pagerank.py <file> <iterations> <damping>", file=sys.stderr)
        sys.exit(-1)

    dataFile = sys.argv[1]
    name = os.path.splitext(os.path.basename(dataFile))[0]
    damping = float(sys.argv[3])

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    lines = lines.map(lambda urls: parseLinks(urls))
    links = lines.map(lambda urls: urls[0])
    ranks = lines.map(lambda urls: urls[1])


    # Calculates and updates URL ranks continuously using PageRank algorithm.
    startTime = datetime.now()
    for iteration in range(int(sys.argv[2])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(
            lambda url_urls_rank: computeContribs(url_urls_rank[0], url_urls_rank[1][0], url_urls_rank[1][1]))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * damping + (1-damping))

    durationTime = datetime.now()-startTime
    print("Time: "+str(durationTime.total_seconds()*1000.0)+"ms")

    # Collects all URL ranks and dump them to console.
    ordered = []
    for (link, rank) in ranks.collect():
        ordered.append({"url":link,"rank":str(format(rank, '1.16f'))})
        #print("%s has rank: %s." % (link, rank))

    spark.stop()

    file = open("pagerank_"+name,"w")
    for d in sorted(ordered, key=lambda k: k['rank'], reverse=True):
        file.write(d["rank"]+"\t"+d["url"]+"\n")
    file.close()
