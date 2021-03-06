''' To be used with the module search. Can't run individually'''

import os
import re
import sys
import json
import time
import copy
import heapq
import string
from collections import defaultdict



class Retriever(object):

    def __init__(self, index_file="index.json"):

        self.load_index(index_file)


    def load_index(self, index_file):
        # Load index and document map
        print("Loading index... ")
        with open(index_file, 'r') as f:
            str = f.read()
            self.index = json.loads(str)

        print("Loading document map...")
        with open("WEBPAGES_RAW/bookkeeping.json", 'r') as f:
            self.doc_map = json.loads(f.read())


    def retrieve(self, terms):
        doc_dict = defaultdict(int)

        # Gather all docs which contain at least one term
        for t in terms:
            t = t.lower()
            if t in self.index.keys():
                for doc, info in self.index[t].items():
                    weight = info["tf-idf"]
                    doc_dict[doc] = -weight # Invert weight since heapq is min-heap

        # Convert dict to priority queue based on tf-idf weights

        pq = []
        for doc, weight in doc_dict.items():
            pq.append((weight, self.doc_map[doc]))

        heapq.heapify(pq)
        return pq




if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("To use: python retrieve.py <term>")
        exit()

    retrieve(sys.argv[1:])
