#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import random

import re


class ExerciseOne:
    __file_prefix = 'reuters-00'
    __file_postfix = '.json'

    def __construct_file_path(self, index):
        string = str(index) if index > 9 else '0' + str(index)
        return 'data-files/reuters-0' + string + '.json'

    def __should_exclude_article(self, article):
        return 'body' not in article or 'topics' not in article or len(article['topics']) < 1

    # def load_files_construct_articles(self):
    #     articles = []
    #     article_topics = []
    #     format_string = lambda string: '' \
    #         .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:') \
    #         .lower()
    #
    #     for i in range(0, 22):
    #         with open(self.__construct_file_path(i)) as file:
    #             data = json.load(file)
    #             for article in data:
    #                 if not self.__should_exclude_article(article):
    #                     articles.append(format_string(article['body']))
    #                     article_topics.append(article['topics'])
    #     return articles, article_topics

    def load_files_construct_articles(self):
        articles_list = []
        article_topics_list = []
        format_string = lambda string: '' \
            .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:_') \
            .lower()

        with open('data-files/reuters-101.json') as file:
            data = json.load(file)
            for article in data:
                if not self.__should_exclude_article(article):
                    articles_list.append(format_string(article['body']))
                    article_topics_list.append(article['topics'])
        return articles_list, article_topics_list

    """
    Create a matrix, with width = the number of distinct words from all articles, and is a hashed BOW, in the format
     that if a word is present in the article, we put 1 under the index of that word, for the current row of the matrix,
     where each row corresponds to an article.
    """

    def encode_bow(self, articles_list):
        distinct_words = dict()
        dist_words = list()
        count = 0
        for article in articles_list:
            words_in_article = article.split()
            for word in words_in_article:
                # For each distinct word as key, put incremented integer as value
                if word not in distinct_words:
                    distinct_words[word] = count
                    dist_words.append(set())
                    count += 1

        bow = list()
        dist_words_count = len(distinct_words)
        for i_article, article in enumerate(articles_list):
            # Add a row of 0's for each new article, to the BOW matrix
            bow.append([0] * dist_words_count)

            words_in_article = article.split()
            # For each word in the article, get its value from the distinct words. That value is actually an index in
            # the current row of the BOW matrix. Put a 1 as a value to that index.
            for word in words_in_article:
                bow[i_article][distinct_words[word]] = 1

        return bow, dist_words

    """
    Generate a list (permutation/hash function) of numbers from 0 to the length of the BOW matrix, shuffled randomly
    """

    def generate_permutation(self, bow):
        bow_matrix_len = len(bow)
        permutation = random.sample(xrange(0, bow_matrix_len), bow_matrix_len)
        return permutation

    """
    According to the permutation, generate a new matrix, from the BOW matrix.
    Then calculate the MinHash algorithm
    """

    def permute_bow_matrix(self, bow, permutation, dist_words):
        shuffled_bow = list()
        # permuted_bow = copy.copy(dist_words)

        # Shuffle and re-arrange the BOW according to the permutation. F.e. if the permutation is:
        # [6, 1, 7, 5, 4, 0, 3, 2, 8)], then the element on index 6 from the BOW will go on index 0 in the shuffled BOW,
        # the element on index 1 from the BOW will go index 1 in the shuffled, then el. on index 7 will go on index 2
        # in the shuffled BOW and so on.
        for i_p, number in enumerate(permutation):
            shuffled_bow.append(bow[permutation[i_p]])

        # Loop through the `dist_words` (a list of indices of the words in the BOW, with value set()) - so, basically,
        # iterate for each distinct word, and then inner-iterate through the shuffled BOW matrix (permuted BOW), and
        # take the word of the current BOW by the current index of the `dist_words`, because each row of the BOW matrix
        # is identical to the `dist_words` list. Then check if the flag (the value) of the word in that row is 1.
        # If yes, add the index of that row from the BOW matrix, to the set of the current word in the `dist_words` and
        # break the loop (because we want to get the index of only the first occurrence of the word in the matrix).
        # If no, then go to the next row of the BOW matrix, and this way until we find a place where the flag is 1.
        for i_word, set_w in enumerate(dist_words):
            for i_word_list, word_list in enumerate(shuffled_bow):
                word_flag = word_list[i_word]
                if word_flag == 1:
                    set_w.add(i_word_list)
                    break

        return dist_words


# ----------------------------------------------------------------------------------------------------------------------
instance = ExerciseOne()
articles, article_topics = instance.load_files_construct_articles()
bow_matrix, dist_words_list = instance.encode_bow(articles)

permutation_hash_1 = instance.generate_permutation(bow_matrix)
dist_words_list = instance.permute_bow_matrix(bow_matrix, permutation_hash_1, dist_words_list)
for index, row in enumerate(dist_words_list):
    if len(row) > 0:
        print (index, row)

print '-----------'

permutation_hash_2 = instance.generate_permutation(bow_matrix)
dist_words_list = instance.permute_bow_matrix(bow_matrix, permutation_hash_2, dist_words_list)
for index, row in enumerate(dist_words_list):
    if len(row) > 0:
        print (index, row)

print '-----------'

permutation_hash_3 = instance.generate_permutation(bow_matrix)
dist_words_list = instance.permute_bow_matrix(bow_matrix, permutation_hash_3, dist_words_list)
for index, row in enumerate(dist_words_list):
    if len(row) > 0:
        print (index, row)

print '-----------'

print 'articles x features => ' + str(len(bow_matrix)) + ' x ' + str(len(bow_matrix[0]))
