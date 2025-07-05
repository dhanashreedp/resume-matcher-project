from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.TextField()  # comma-separated skills

    def __str__(self):
        return self.title
