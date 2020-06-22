from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple
from django.shortcuts import redirect, render
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from .snippets import BlogAuthor, BlogCategory

from pytils.translit import slugify
from streams import blocks


class BlogListingPage(RoutablePageMixin, Page):

    max_count = 1
    template = "blog/blog_listing_page.html"
    subpage_types = ['blog.BlogDetailPage']

    custom_title = models.CharField(max_length=150, blank=False, null=False, help_text="Наші статті")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Grab all the posts from detail page that are Live and Public
        # Returns a list that named QuerySet
        #context['posts'] = BlogDetailPage.objects.live().public()
        # -first_published_at --> Wagtail field added automatically to each post, draft pages doesn't have it
        # republishing doesn't influence that field
        #all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at') 
        all_posts = BlogDetailPage.objects.live().public().order_by('-publication_date')

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])
        
        paginator = Paginator(object_list=all_posts, per_page=4)
        # Get page number we're currently at
        page = request.GET.get("p")
        try: # Trying to get that page
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage: # if someone will go to page 99999999
            # return last page
            print("WARNING: Page not found, redirrecting to the last one")
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()
        return context

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        context = self.get_context(request)
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            return redirect('/blog/')

        context['category'] = category
        context['posts'] = BlogDetailPage.objects.live().public().filter(category__in=[category])
        return render(request, "blog/latest_posts.html", context)

    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title')
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogDetailPage(Page):

    template = "blog/blog_detail_page.html"
    
    parent_page_types=['blog.BlogListingPage']

    publication_date = models.DateTimeField(
        verbose_name='Дата публікації',
        default=timezone.now
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    custom_title = models.CharField(max_length=150, blank=False, null=False, verbose_name="Підзаголовок. Скорочений опис", 
    help_text="Додайте скорочений опис статті. Максимум 150 символів.")

    category = ParentalManyToManyField("blog.BlogCategory", blank=True)
    
    
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
    [
        ("title_and_text", blocks.TitleAndTextBlock()),
        ("rich_text", blocks.RichTextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock())
    ],
    null=True,
    blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('publication_date'),
        FieldPanel('tags'),
        ImageChooserPanel('blog_image'),
        MultiFieldPanel([   
            FieldPanel('category', heading='Оберіть категорію', widget=forms.CheckboxSelectMultiple)
        ], heading='Категорія'),
        StreamFieldPanel('content')
    ]

    def full_clean(self, *args, **kwargs):
        super(BlogDetailPage, self).full_clean(*args, **kwargs)

        self.slug = slugify(self.slug)


BlogDetailPage._meta.get_field("title").verbose_name = "Вкажіть Заголовок Статті"
BlogDetailPage._meta.get_field("title").help_text = "Вкажіть заголовок, який відображатиметься на головній стрічці сайту"
