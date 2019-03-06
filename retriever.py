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

    def __init__(self):
        self.load_documents()


    def load_documents(self):
        print("Loading document map...")
        with open("WEBPAGES_RAW/bookkeeping.json", 'r') as f:
            self.doc_map = json.loads(f.read())

    def load_index(self, index_file):
        # Load index file according to the input
        print("Loading index... ")
        with open(index_file, 'r') as f:
            str = f.read()
            self.index = json.loads(str)




    def retrieve(self, terms):
        doc_dict = defaultdict(int)

        # Gather all docs which contain at least one term
        for t in terms:
            filename = t[0 : 3]
            index_file = "index_folder\\" + filename + ".json"
            self.load_index(index_file)
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
        print("To use: python retriever.py <term>")
        exit()

    retrieve(sys.argv[1:])
