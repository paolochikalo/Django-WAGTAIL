
#from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

import bokeh
from bokeh.server.django import autoload, directory, document, static_extensions

from bokeh_apps import sea_surface as sea_surface_app
from bokeh_apps import ohlc

from . import views


bokeh_app_config = apps.get_app_config('bokeh.server.django')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("ohlc/", views.ohlc),
    path("sea_surface/", views.sea_surface),
    path("my_sea_surface/", views.sea_surface_custom_uri),
]

base_path = settings.BASE_PATH

bokeh_apps = [
    autoload("sea_surface", sea_surface_app.sea_surface_handler),
    autoload("ohlc", ohlc.ohlc_stream),
#     document("sea_surface_with_template", sea_surface_app.sea_surface_handler_with_template),
#     document("bokeh_apps/sea_surface", base_path / "bokeh_apps" / "sea_surface.py"),
#     document("shape_viewer", sea_surface_app.shape_viewer_handler),
]

#apps_path = Path(bokeh.__file__).parent.parent / "examples" / "app"
#bokeh_apps += directory(apps_path)

urlpatterns += static_extensions() # needed for panel js to work
urlpatterns += staticfiles_urlpatterns()
