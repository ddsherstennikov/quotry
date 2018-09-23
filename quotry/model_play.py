"""
t1->q1
t2->q2

u1⊂up1 
    * t1
    <3 q1

u2⊂up2 
    * t2
    <3 q2
"""

# create 2 tags and 2 quotes
>>> from quotry.models import Tag, Quote, UserProfile
>>> t1 = Tag(name='Star Wars')
>>> t1.quote_set.all()
[]
>>> t1.save()
>>> q1 = Quote(tag=t1, text='Do or do not, there is no try.' )
>>> t1.quote_set.all()
[]
>>> q1.save()
>>> t1
<Tag: Star Wars>
>>> q1.author = 'Yoda'
>>> q1.title = 'Yoda saying'
>>> q1.save()
>>> q1
<Quote: Yoda saying>
>>> t1.quote_set.all()
[<Quote: Yoda saying
Do or do not, there is no try.
Yoda>]
>>> Tag.objects.all()
[<Tag: Star Wars>]
>>> Quote.objects.all()
[<Quote: Yoda saying
Do or do not, there is no try.
Yoda>]
>>> t2 = Tag(name='Hamlet')
>>> t2.save()
>>> q2 = Quote(tag=t2, text="To be or not to be?", author="W.Shakespear" )
>>> q2.save()

# create 2 users with 2 corresponding userprofiles
>>> from django.contrib.auth.models import User
>>> u1 = User(username='den', password='12den')
>>> u1.save()
>>> u2 = User(username='dima', password='12dima')
>>> u2.save()
>>> up1 = UserProfile(user=u1)
>>> up2 = UserProfile(user=u2)
>>> up1.save()
>>> up2.save()

# establish likes and favs relationships
>>> up1.favs.add(t1)
>>> Tag.objects.all()
[<Tag: Star Wars>, <Tag: Hamlet>]
>>> Tag.objects.all()[0]
<Tag: Star Wars>
>>> t1 = Tag.objects.all()[0]
>>> up1.favs.add(t1)
>>> up1.favs
<django.db.models.fields.related.ManyRelatedManager object at 0x7fe4b0659f10>
>>> up1.favs.all()
[<Tag: Star Wars>]
>>> up2.favs.add(t2)
>>> up1.likes.add(q1)
>>> Quote.objects.all()[0]
<Quote: Yoda saying
Do or do not, there is no try.
Yoda>
>>> q1 = Quote.objects.all()[0]
>>> up1.likes.add(q1)
>>> up2.likes.add(q2)
>>> up1.save()
>>> up2.save()


>>> up1.likes.all()
[<Quote: Yoda saying
Do or do not, there is no try.
Yoda>]
>>> up1.favs.all()
[<Tag: Star Wars>]
>>> up2.likes.all()
[<Quote: 
To be or not to be?
W.Shakespear>]
>>> up2.favs.all()
[<Tag: Hamlet>]
>>> q1.userprofile_set.all()
[<UserProfile: den>]
>>> q2.userprofile_set.all()
[<UserProfile: dima>]
>>> t1.userprofile_set.all()
[<UserProfile: den>]
>>> t2.userprofile_set.all()
[<UserProfile: dima>]
