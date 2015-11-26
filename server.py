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
    t = np.linspace(0, 10, 500)
    y = np.sin(t * 2 * 3.141)
    plt.plot(t, y)
    plt.axis('off')
    memdata = io.BytesIO()
    plt.savefig(memdata, format='png')
    image = memdata.getvalue()
    return image


def load_markers():
    df_cities = pd.read_csv("static/data/cities.csv", encoding="cp1255")
    df_acc = pd.concat(pd.read_csv(filename, encoding="cp1255") for filename in
                       glob("static/data/lms/Accidents Type */*/*AccData.csv"))
    df_acc = df_acc[df_acc.SEMEL_YISHUV > 0]
    groups = df_acc.groupby(["SEMEL_YISHUV", "HUMRAT_TEUNA"], as_index=False)
    df_size = groups.size()
    df_size_total = df_acc.groupby("SEMEL_YISHUV", as_index=False).size()
    max_size = df_size_total.max()
    df = groups.mean()
    df = pd.merge(df, df_cities, left_on="SEMEL_YISHUV", right_on="SEMEL")
    df = df[pd.notnull(df.X) & pd.notnull(df.Y) & (df_size_total > 1)]
    app.markers = []
    for index, row in df.iterrows():
        lng, lat = coordinates_converter.convert(row.X, row.Y)
        size = count_to_size(df_size_total[row.SEMEL_YISHUV], max_size)
        size_per_severity = df_size[row.SEMEL_YISHUV]
        light = size_per_severity.get(3, 1)
        severe = size_per_severity.get(1, 0) + size_per_severity.get(2, 0)
        normalizer = max(light, severe)
        color = max(0, 200 - 200 * severe / light)
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
            "involved_count": 300,
            "young_count": 200,
            "middle_count": 70,
            "old_count": 30,
        })
    print "Created %d markers" % len(app.markers)


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