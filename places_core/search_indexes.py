import datetime
from haystack import indexes
from locations.models import Location


class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Wyszukiwarka dla lokalizacji.
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Location

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
