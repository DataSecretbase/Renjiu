from django.db import models
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime, date
from django.urls import reverse

import base.models as base


# use Django-tagging for tags. If Django-tagging cannot be found, create our own
# I did not author this little snippet, I found it somewhere on the web,
# and cannot remember where exactly it was.
#try:
#    from tagging.fields import TagField
#    tagfield_help_text = 'Separate tags with spaces, put quotes around multiple-word tags.'
#except ImportError:
#    class TagField(models.CharField):
#        def __init__(self, **kwargs):
#            default_kwargs = {'max_length': 255, 'blank': True}
#            default_kwargs.update(kwargs)
#            super(TagField, self).__init__(**default_kwargs)
#        def get_internal_type(self):
#            return 'CharField'
#    tagfield_help_text = 'Django-tagging was not found, tags will be treated as plain text.'

# End tagging snippet



class Audio(models.Model):
    """
    This is our Base Audio Class, with fields that will be available
    to all other Audio models.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,
        help_text="A url friendly slug for the audio clip.")
    description = models.TextField(null=True, blank=True)

#    tags = TagField(help_text=tagfield_help_text)
    categories = models.ManyToManyField('AudioCategory', null = True, blank = True)
    allow_comments = models.BooleanField(default=False)

    ## TODO:
    ## In future we may want to allow for more control over publication
    is_public = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(base.User, on_delete = models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ('-publish_date', '-created_date')
        get_latest_by = 'publish_date'

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        return reverse('audiostream_audio_detail', (), { 
            'year': self.publish_date.strftime("%Y"),
            'month': self.publish_date.strftime("%b"),
            'day': self.publish_date.strftime("%d"), 
            'slug': self.slug 
        })

    def save(self, *args, **kwargs):
        self.modified_date = datetime.now()
        if self.publish_date == None and self.is_public:
            self.publish_date = datetime.now()
        super(Audio, self).save(*args, **kwargs)


class BasicAudio(Audio):
    """
    This is our basic HTML5 Audio type. BasicAudio can have more than
    one HTML5 Audio as a 'audio type'. This allows us to create different
    audio formats, one for each type format.
    """
    pass


class HTML5Audio(models.Model):
    MPEG = 0
    MP3 = 1
    WMA = 2
    FLAC = 3
    AUDIO_TYPE = (
        (MPEG, 'audio/mpeg'),
        (MP3, 'audio/mp3'),
        (WMA, 'audio/wma'),
        (FLAC, 'audio/flac'),
    )

    audio_type = models.IntegerField(
        choices=AUDIO_TYPE,
        default=MP3,
        help_text="The Audio type"
    )
    audio_file = models.FileField(
        upload_to="Audio/html5/",
        help_text="The file you wish to upload. Make sure that it's the correct format.",
    )

    # Allow for multiple audio types for a single audio
    basic_audio = models.ForeignKey(Audio, on_delete = models.SET_NULL, null = True, blank = True)

    class Meta:
        verbose_name = "Html 5 Audio"
        verbose_name_plural = "Html 5 Audio"


class AudioCategory(models.Model):
    """ A model to help categorize audios """
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        help_text="A url friendly slug for the category",
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Audio Categories"

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        return reverse('audiostream_category_detail', [self.slug])
