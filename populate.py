import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qsite.settings')

import django
django.setup()

from quotry.models import Tag, Quote


def starwars():
    starwars = state_tag('Star Wars')                                                       # visits=128, favs=64
    state_quote(tag=starwars, author=u'Yoda', 
                text=u'Do or do not, there is no try.')                                     # likes=123
    state_quote(tag=starwars, author=u'Qui Gon Jinn',
                text=u'Your focus determines your reality.')                                # likes=14
    state_quote(tag=starwars, author=u'Luke Skywalker',
                text=u'I am a Jedi, like my father before me.')                             # likes=17
    state_quote(tag=starwars, author=u'Wookieepedia', url=u'http://starwars.wikia.com/wiki/Jedi',
                text=u'Originally formed as a philosophical study group situated'\
                ' on the planet Tython, the Jedi became revered as guardians of peace'\
                ' and justice in the galaxy. As mystical wielders of the Force and of'\
                ' their signature lightsabers, their powers inspired all citizens'\
                ' in the galaxy. The calm, considered demeanor of the Jedi made them'\
                ' ideal brokers of peace in times of conflict or dispute.')
    state_quote(tag=starwars, author=u'Qui-Gon Jinn', url=u'http://starwars.wikia.com/wiki/Jedi',
                text=u'Training to become a Jedi is not an easy challenge,'\
                'and even if you succeed, it\'s a hard life.')                              # likes=9001

def hamlet():
    hamlet = state_tag("Hamlet")                                                            # visits=64, favs=32
    state_quote(tag=hamlet, author=u'W.Shakespeare',
                text=u'To be or not to be?')                                                # likes=56
    state_quote(tag=hamlet, author=u'W.Shakespeare',
                text=u'There is nothing either good nor bad, but thinking makes it so')     # likes=73
    state_quote(tag=hamlet, author=u'W.Shakespeare',
                text=u'Words, words, words.')                                               # likes=184

def tennyson():
    tennyson = state_tag("Alfred Lord Tennyson")                                            # visits=32, favs=16
    state_quote(tag=tennyson, author=u'Alfred Lord Tennyson',
                text=u'To strive, to seek, to find, and not to yield.')                     # likes=42
    state_quote(tag=tennyson, author=u'Alfred Lord Tennyson',
                text=u'Ring in the valiant man and free')                                   # likes=12

def rw_emerson():
    rw_emerson = state_tag("Ralph Waldo Emerson")                                           # visits=16, favs=8
    state_quote(tag=rw_emerson, author=u'Ralph Waldo Emerson',
                text=u'Every book is a quotation; and every house is a quotation out of all'\
                    ' forests and mines and stone quarries;'\
                    ' and every man is a quotation from all his ancestors.')                # likes=22
    state_quote(tag=rw_emerson, author=u'Ralph Waldo Emerson',
                text=u'The profoundest thought or passion sleeps as in a mine,'\
                    ' until an equal mind and heart finds and publishes it.')               # likes=18
    state_quote(tag=rw_emerson, author=u'Ralph Waldo Emerson',
                text=u'...whether your jewel was got from the mine or from an auctioneer.') # likes=9

def nietzsche():
    nietzsche = state_tag("Friedrich Nietzsche")                                             # visits=8, favs=4
    state_quote(tag=nietzsche, author=u'Friedrich Nietzsche',
                text=u'In the mountains the shortest route is from peak'\
                'to peak but for that you must have long legs. '\
                'Aphorisms should be peaks, and those to whom'\
                ' they are spoken should be big and tall of stature.')                       # likes=22
    state_quote(tag=nietzsche, author=u'Friedrich Nietzsche',
                text=u'A good aphorism is too hard for the tooth of time, '\
                    'and is not worn away by all the centuries, although '\
                    'it serves as food for every epoch. Hence it is the '\
                    'greatest paradox in literature, the imperishable in '\
                    'the midst of change, the nourishment which always '\
                    'remains highly valued, as salt does, and never '\
                    'becomes stupid like salt.')                                             # likes=65

def proverbs():
    proverbs = state_tag("Proverbs")                                                         # visits=4, favs=2
    state_quote(tag=proverbs, author=u'Proverbs',
                text=u'The maxims of men disclose their hearts.')                            # likes=1

def seneca():
    seneca = state_tag("Seneca")                                                             # visits=4, favs=2
    state_quote(tag=seneca, author=u'Seneca',
                text=u'Precepts or maxims are of great weight; and a few useful ones'\
                    ' at hand do more toward a happy life than whole volumes '\
                    'that we know not where to find.')                                       # likes=13

def g_kabore():
    g_kabore = state_tag("Gaston Kabore")                                                             # visits=4, favs=2
    state_quote(tag=g_kabore, author=u'Gaston Kabore',
                text=u'A proverb is an exploding atom of wisdom.')                                       # likes=13




def populate():

    starwars()
    hamlet()
    tennyson()
    rw_emerson()
    nietzsche()
    proverbs()
    seneca()
    g_kabore()
    
    # Print out what we have added to the user.
    for t in Tag.objects.all():
        for q in Quote.objects.filter(tag=t):
            print "- {0} - {1}".format(str(t), str(q))


# create new or update existing tag, save to db
def state_tag(name, visits=0, favs=0):
    # payload - get or crt by name
    c = Tag.objects.get_or_create(name=name)[0]

    # ranging - fill or upd (if not null)
    if visits:
        c.visits = visits
    if favs:
        c.favs = favs

    # tech - slugify occures at model's overrided save() meth
    # c.slug

    c.save()
    return c


# create new or update existing tag, save to db
def state_quote(tag, author, text, title="", url="", likes=0):
    # org, payload required - get or crt by tag+author+text
    q = Quote.objects.get_or_create(tag=tag, author=author, text=text)[0]

    # payload addon - fill or upd (if not null)
    if title: 
        q.title = title
    if url:
        q.url = url

    # ranging - fill or upd (if not null)
    if likes:
        q.likes = likes

    q.save()
    return q


# Start execution here!
if __name__ == '__main__':
    print "Starting quotrY population script..."
    populate()