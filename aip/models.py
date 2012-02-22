from django.db import models
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

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
    #if height is -1, that means unlimited height
    #if height is 0, then height_unit and height_ref doesn't make sense, we're
    #always talking about the ground and up
    height = models.IntegerField()
    height_unit = models.CharField(max_length=2, choices=LENGTH_UNITS,
            blank=True)
    height_ref = models.CharField(max_length=4, choices=HEIGHT_REFS, blank=True)
    class Meta:
        unique_together = (("height", "height_unit", "height_ref"),)

    def clean(self):
        #check that height from GND and UNL make sense
        if self.height == 0 and ((self.height_unit!='') or
                (self.height_ref!='')):
            raise ValidationError('When height=GND, height ref and height unit should not be defined')
        if self.height == -1 and ((self.height_unit!='') or
                (self.height_ref!='')):
            raise ValidationError('When height=UNL, height ref and height unit should not be defined')
        if self.height < -1:
            raise ValidationError("Height can not be a negative number")

    def __unicode__(self):
        if (self.height == -1):
            return "UNL"
        if (self.height == 0):
            return "GND"
        else:
            return "%d %s %s" % (self.height, self.height_unit, self.height_ref)

class HeightBounds(models.Model):
    # related_name='+' means that django won't create a two way relation
    # https://docs.djangoproject.com/en/1.3/ref/models/fields/#django.db.models.ForeignKey.related_name
    lower = models.ForeignKey(Height, related_name='+')
    upper = models.ForeignKey(Height, related_name='+')
    class Meta:
        unique_together = (("lower", "upper"),)
    def clean(self):
        # check for obvious errors in the bounds definition, we can't have a
        # bound starting over the end
        if unicode(self.lower)=='UNL':
            raise ValidationError('Lower height can not be UNL')
        if unicode(self.upper)=='GND':
            raise ValidationError('Upper height can not be GND')
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
