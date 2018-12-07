#!/usr/bin/python
from org.apache.pig.scripting import *
import sys
import os

dataFile = sys.argv[1]
name = os.path.splitext(os.path.basename(dataFile))[0]
nbIter = int(sys.argv[2])
damping = float(sys.argv[3])

P = Pig.compile("""
-- PR(A) = (1-d) + d (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))
previous_pagerank =
    LOAD '$docs_in'
    USING PigStorage(' ')
    AS ( url: chararray, pagerank: float, links:{ link: ( url: chararray ) } );
outbound_pagerank =
    FOREACH previous_pagerank
    GENERATE
        ( pagerank / COUNT ( links ) ) AS pagerank,
        FLATTEN ( links ) AS to_url;
new_pagerank =
    FOREACH
        ( COGROUP outbound_pagerank BY to_url, previous_pagerank BY url INNER )
    GENERATE
        group AS url,
        ( 1 - $d ) + $d * ( (IsEmpty(outbound_pagerank.pagerank)) ? 0.0 : SUM(outbound_pagerank.pagerank) )  AS pagerank,
        FLATTEN ( previous_pagerank.links ) AS links;

STORE new_pagerank
    INTO '$docs_out'
    USING PigStorage(' ');
""")

params = { 'd': damping, 'docs_in': dataFile } #data.txt

for i in range(nbIter):
	out = "out_"+name+"/pagerank_iter_" + str(i + 1)
	params["docs_out"] = out
	Pig.fs("rmr " + out)
	stats = P.bind(params).runSingle()
	if not stats.isSuccessful():
		raise 'failed'
	params["docs_in"] = out

nbi = str(nbIter)
file = open("out_"+name+"/pagerank_iter_"+nbi+"/part-r-00000","r")
lines = file.read().split("\n")
lines.pop()
clean = [{"url":i.split(" ")[0],"rank":format(float(i.split(" ")[1]), '1.16f')} for i in lines]
orderedclean = sorted(clean, key=lambda k: k['rank'], reverse=True)
file.close()

file = open("pagerank_"+name,"w")
for d in orderedclean:
    file.write(str(d["rank"])+"\t"+d["url"]+"\n")
file.close()
