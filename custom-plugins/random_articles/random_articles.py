# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random

from pelican import signals


def is_published(article):
    return getattr(article, 'status', 'published') == 'published'


def get_articles(generator):
    articles = generator.context['articles']
    published_articles = filter(is_published, articles)
    skip_articles = generator.settings.get('SKIP_ARTICLES', 0)
    return published_articles[skip_articles:]


class RandomArticles(object):
    "This class should inject a `random_articles` in a context."

    def __init__(self, generator, metadata=None):
        self.generator = generator
        self.metadata = metadata
        self.settings = generator.settings

    def inject_articles(self):
        """ Inject `random_articles` in generator context """
        self.generator.context['random_articles'] = self.get_random_articles()

    def get_random_articles(self):
        """ Get random articles following settings configuration """
        all_articles = get_articles(self.generator)
        random_articles_number = self.settings.get('RANDOM_ARTICLES', 3)

        articles_number = len(all_articles)

        # we should return only articles number that exists
        random_number = random_articles_number
        if articles_number < random_articles_number:
            random_number = articles_number

        return random.sample(all_articles, random_number)


def register_articles(generator, metadata):
    RandomArticles(generator, metadata).inject_articles()


def register():
    signals.page_generator_context.connect(register_articles)
