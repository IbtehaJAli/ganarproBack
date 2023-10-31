from ckeditor.fields import RichTextField
from django.db import models
from django.template.defaultfilters import slugify

from app.api.models import TimestampedModel


# Create your models here.
class ProjectType(TimestampedModel):
    """Proposal table"""
    name = models.CharField(max_length=100, blank=True, null=False)
    slug = models.CharField(max_length=50, blank=False, null=False, unique=True)
    template = RichTextField(null=True, blank=True)
    template_a = models.FileField(upload_to="project_type_upload/", null=True, blank=True, max_length=300)
    template_b = models.FileField(upload_to="project_type_upload/", null=True, blank=True, max_length=300)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(ProjectType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
