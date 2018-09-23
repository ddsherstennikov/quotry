from django.contrib import admin

from quotry.models import Tag, Quote, UserProfile


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 1


class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'slug']}),
        ('ranging', {'fields': ['visits', 'favs'],'classes': ['collapse'],}),
    ]

    prepopulated_fields = {'slug':('name',)}

    inlines = [QuoteInline]
    list_display = ('name', 'visits', 'favs')
    list_filter = ['visits', 'favs']
    search_fields = ['name']


class QuoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'tag']}),
        (None, {'fields': ['text', 'author', 'url']}),
        ('ranging', {'fields': ['likes'],'classes': ['collapse'],}),
    ]
    list_display = ('title', 'tag', 'text', 'author', 'url', 'likes')
    list_filter = ['likes']
    search_fields = ['tag__name', 'title', 'text', 'author']


admin.site.register(Tag, TagAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(UserProfile)