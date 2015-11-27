#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from glob import glob

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

import tornado.ioloop
import tornado.web

from geo import ItmToWGS84

coordinates_converter = ItmToWGS84()
CHART_SCALE = 10
AGE_BINS = [1, 4, 14, 99]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class MarkersHandler(tornado.web.RequestHandler):
    def get(self):
        data = {"markers": app.markers}
        output = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.write(output)


class TimelineHandler(tornado.web.RequestHandler):
    def get(self):
        city1 = self.get_argument("city1")
        city2 = self.get_argument("city2")
        image = create_plot(city1, city2)
        self.set_header('Content-type', 'image/png')
        self.set_header('Content-length', len(image))
        self.write(image)


def create_plot(city1, city2):
    plt.figure()
    years1 = create_plot_one_city(city1, "#FC5200")
    years2 = create_plot_one_city(city2, "#FEB700")
    plt.axvline(0)
    years = np.concatenate((years1, years2))
    plt.xticks([int(np.nanmin(years)), int(np.nanmax(years))])
    plt.xlabel("")
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().ticklabel_format(useOffset=False)
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    memdata = io.BytesIO()
    plt.savefig(memdata, format='png')
    image = memdata.getvalue()
    return image


def create_plot_one_city(city, color):
    df = app.df_acc
    df = df[df.SEMEL_YISHUV == int(city)]
    if df.empty:
        return [np.nan]
    years = df.SHNAT_TEUNA
    df = df.groupby("SHNAT_TEUNA").size()
    df.plot(color=color)
    return years


def load_markers():
    print "Creating markers...",
    df_cities = pd.read_csv("static/data/cities.csv", encoding="cp1255")
    app.df_acc = pd.concat(pd.read_csv(filename, encoding="cp1255") for filename in
                           glob("static/data/lms/Accidents Type 3/*/*AccData.csv"))
    df_inv = pd.concat(pd.read_csv(filename, encoding="cp1255") for filename in
                           glob("static/data/lms/Accidents Type 3/*/*InvData.csv"))
    app.df_acc = app.df_acc[app.df_acc.SEMEL_YISHUV > 0]

    # Severity counts per city
    groups = app.df_acc.groupby(["SEMEL_YISHUV", "HUMRAT_TEUNA"], as_index=False)
    df_size = groups.size()
    df_size_total = app.df_acc.groupby("SEMEL_YISHUV", as_index=False).size()
    max_size = df_size_total.max()
    df_markers = groups.mean()
    df_markers = pd.merge(df_markers, df_cities, left_on="SEMEL_YISHUV", right_on="SEMEL")
    df_markers = df_markers[pd.notnull(df_markers.X) & pd.notnull(df_markers.Y) & (df_size_total > 1)]

    # Involved individuals counts
    df_involved = pd.merge(app.df_acc, df_inv,
                           left_on=["pk_teuna_fikt", "sug_tik"],
                           right_on=["pk_teuna_fikt", "SUG_TIK"])
    df_involved = df_involved.groupby(["SEMEL_YISHUV",
                                       np.digitize(df_involved.KVUZA_GIL, bins=AGE_BINS)],
                                      as_index=False).size()

    app.markers = []
    for index, row in df_markers.iterrows():
        lng, lat = coordinates_converter.convert(row.X, row.Y)
        size = count_to_size(df_size_total[row.SEMEL_YISHUV], max_size)

        severity_count = df_size[row.SEMEL_YISHUV]
        light = severity_count.get(3, 1)
        severe = severity_count.get(1, 0) + severity_count.get(2, 0)
        normalizer = max(light, severe)
        color = max(0, int(200 - 2000 * float(severe) / light))

        age_count = df_involved[row.SEMEL_YISHUV]
        involved = age_count.sum()
        young = age_count.get(1, 0)
        middle = age_count.get(2, 0)
        old = age_count.get(3, 0)
        # 4 (that is 99 before binning) is unknown age

        app.markers.append({
            "lat": lat,
            "lng": lng,
            "title": row.NAME,
            "size": size,
            "color": color,
            "total": df_size_total[row.SEMEL_YISHUV],
            "light": light,
            "severe": severe,
            "light_size": CHART_SCALE * count_to_size(light, normalizer),
            "severe_size": CHART_SCALE * count_to_size(severe, normalizer),
            "involved_count": involved,
            "young_count": young,
            "middle_count": middle,
            "old_count": old,
            "id": row.SEMEL_YISHUV,
        })
    app.markers.sort(key=lambda marker: marker["title"])
    print "%d done" % len(app.markers)


def count_to_size(count, max_size):
    return 30 * np.log(1.25 + count / float(max_size)) if count else 0


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/markers", MarkersHandler),
            (r"/timeline.png", TimelineHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )


if __name__ == "__main__":
    app = make_app()
    load_markers()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
