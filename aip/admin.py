from django.contrib.gis import admin
from models import *

admin.site.register(Height, admin.ModelAdmin)
admin.site.register(HeightBounds, admin.ModelAdmin)
admin.site.register(Airspace, admin.GeoModelAdmin)
