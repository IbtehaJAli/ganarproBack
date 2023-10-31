from django.db import models

# Create your models here.


class EmailTemplate(models.Model):
    name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=500)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    GENERAL_CONTRACTOR = 'GC'
    PROJECT_BOARD = 'PB'
    TEMPLATE_TYPE = (
        (GENERAL_CONTRACTOR, 'General Contractor'),
        (PROJECT_BOARD, 'Project Board')
    )
    type = models.CharField(max_length=2, choices=TEMPLATE_TYPE, blank=False, null=True, default=PROJECT_BOARD)
    ordering = models.IntegerField(choices=list(zip(range(1, 20), range(1, 20))), null=True)

    is_active = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordering']