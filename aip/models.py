from django.db import models
from django.contrib.gis.db import models

LENGTH_UNITS = (
    ('m', 'meters'),
    ('ft', 'feet'),
    ('fl', 'flight level'),
)

HEIGHT_REFS = (
    ('amsl', 'Above Mean Sea Level'),
    ('agl', 'Above Ground Level'),
)

class Height(models.Model):
    height = models.IntegerField()
    height_unit = models.CharField(max_length=2, choices=LENGTH_UNITS, null=True)
    height_ref = models.CharField(max_length=4, choices=HEIGHT_REFS, null=True)
    def __unicode__(self):
        if (self.height == -1):
            return "UNL"
        else:
            return "%d %s %s" % (self.height, self.height_unit, self.height_ref)

class HeightBounds(models.Model):
    # related_name='+' means that django won't create a two way relation
    # https://docs.djangoproject.com/en/1.3/ref/models/fields/#django.db.models.ForeignKey.related_name
    lower = models.ForeignKey(Height, related_name='+')
    upper = models.ForeignKey(Height, related_name='+')
    def __unicode__(self):
        return "%s TO %s" % (self.lower.__unicode__(),self.upper.__unicode__())

class Airspace(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    icao_designator = models.CharField(max_length=5)
    height_bounds = models.ForeignKey(HeightBounds)

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom = models.PolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
