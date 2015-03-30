# -*- coding: utf-8 -*-
#
# We map sidebar links for various views. I presume that sidebars will vary
# depending on the module but in each module we will have the same set of links
# for each sub-view (edition, deletion etc.).
#
LINKS_MAP = {
    'summary': (
        'invite',
    ),
    'news': (
        'new_discussion',
        'new_poll',
        'new_idea',
        'add_news',
        'invite',
        'news_category',
    ),
    'discussions': (
        'new_discussion',
        'new_poll',
        'new_location',
        'new_idea',
        'upload',
        'invite',
        'discussion_category',
    ),
    'ideas': (
        'new_discussion',
        'new_poll',
        'new_idea',
        'add_news',
        'invite',
        'idea_category',
    ),
    'polls': (
        'new_discussion',
        'new_poll',
        'new_idea',
        'add_news',
        'invite',
    ),
    'gallery': (
        'new_discussion',
        'new_poll',
        'new_idea',
        'add_news',
        'invite',
    ),
    'followers': (
        'invite',
    ),
    'sublocations': (
        'invite',
    ),
}
