from trie_node import Node

import difflib


class Trie:
    def __init__(self):
        self.root = Node()

    def __getitem__(self, key):
        return self.root.children[key]

    def insert_word(self, wordObj):
        current_node = self.root
        word_finished = True

        for i in range(len(wordObj.word)):
            if wordObj.word[i] in current_node.children:
                current_node = current_node.children[wordObj.word[i]]
            else:
                word_finished = False
                break

        if not word_finished:
            while i < len(wordObj.word):
                current_node.addChild(wordObj.word[i])
                current_node = current_node.children[wordObj.word[i]]
                i += 1

        current_node.data = wordObj

    def has_word(self, word):
        if word == "":
            return False

        current_node = self.root
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break

        if exists:
            if current_node.data == None:
                exists = False

        return exists

    def start_with_prefix(self, prefix):
        words = []

        top_node = self.root
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else:
                return words

        if top_node == self.root:
            nodeList = [node for key, node in top_node.children.iteritems()]
        else:
            nodeList = [top_node]


        while len(nodeList) > 0:
            current_node = nodeList.pop()
            if current_node.data != None:
                words.append(current_node.data)

            nodeList += [node for key, node in current_node.children.iteritems()]

        return words

    def getData(self, word):
        if not self.has_word(word):
            raise ValueError(word + " not found.")

        current_node = self.root
        for letter in word:
            current_node = current_node[letter]

        return current_node.data

    def getSimilar(self, word):
        maxSimilatiry = 0
        maxWord = None

        wordlist = self.start_with_prefix(word[0])
        for possible_word in wordlist:
            similarity = difflib.SequenceMatcher(None, word, possible_word.word).ratio()
            if similarity >= maxSimilatiry:
                maxSimilatiry = similarity
                maxWord = possible_word.word

        return maxWord