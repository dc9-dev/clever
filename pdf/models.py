from django.db import models


class State(models.Model):

    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=30, blank=True, null=True)
    #country = models.ForeignKey(Country, related_name="country", on_delete=models.CASCADE,null=True)
    is_deleted = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'states'
