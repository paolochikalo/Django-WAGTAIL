from os.path import join
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from bokeh.document import Document
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

def index(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "index.html", dict(script=script))

def sea_surface(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "base.html", dict(script=script))

def sea_surface_custom_uri(request: HttpRequest) -> HttpResponse:
    script = server_document(request._current_scheme_host + "/sea_surface")
    return render(request, "base.html", dict(script=script))

def ohlc(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "ohlc.html", dict(script=script))
