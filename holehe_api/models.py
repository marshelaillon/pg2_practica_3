from django.db import models

class EmailLookup(models.Model):
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.email


class ServiceResult(models.Model):
  lookup = models.ForeignKey(EmailLookup, related_name='results', on_delete=models.CASCADE)
  service = models.CharField(max_length=100)
  result_data = models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"{self.service} -> {self.lookup.email}"
