import os.path
import pickle

from graph import Graph
from vertex import Vertex
from word_wrapper import Word
from trie import Trie
from parsers.parser import Parser
from time import time


class Indexer():

    __slots__ = "root", "data", "trie"

    def __init__(self, root):
        self.root = root
        self.words = {}
        self.data = {'WORDS': Trie(),
                     'LINKS': Graph(),
                     'FILES': set()}

    def get_file_data(self, filepath, parser):
        links, words = parser.parse(filepath)
        for word in words:
            if word in self.words:
                self.words[word].add(filepath)
            else:
                self.words[word] = set([filepath])
        for link in links:
            newVertex = self.data['LINKS'].add_vertex(Vertex(link))
            self.data['LINKS'][filepath].addEdge(newVertex)

    def get_all_files(self, dir, parser):
        for item in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, item)):
                filename, filetype = os.path.splitext(os.path.join(dir, item))
                if filetype == ".html":
                    self.data['FILES'].add(os.path.join(dir, item))
                    self.data['LINKS'].add_vertex(Vertex(os.path.join(dir, item)))
                    self.get_file_data(os.path.join(dir, item), parser)
            elif os.path.isdir(os.path.join(dir, item)):
                self.get_all_files(os.path.join(dir, item), parser)
        for key, value in self.words.iteritems():
            self.data['WORDS'].insert_word(Word(key, value))

    def index_data(self):
        start = time()
        parser = Parser()
        self.get_all_files(self.root, parser)
        end = time()
        print (end - start)

    def save_data(self):
        self.index_data()
        pickle.dump(self.data, open(os.path.join(self.root, ".index"), 'wb'))

    def load_data(self):
        if os.path.exists(os.path.join(self.root, ".index")):
            try:
                self.data = pickle.load(open(os.path.join(self.root, ".index"), 'rb'))
            except ValueError:
                self.save_data()
        else:
            self.save_data()