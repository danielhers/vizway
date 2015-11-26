#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import pandas as pd
import numpy as np
import tornado.ioloop
import tornado.web

from geo import ItmToWGS84

coordinates_converter = ItmToWGS84()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class MarkersHandler(tornado.web.RequestHandler):
    def get(self):
        data = {"markers": app.markers}
        output = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.write(output)
        print "Sent %d markers" % len(app.markers)


def load_markers():
    df_cities = pd.read_csv("static/data/cities.csv", encoding="cp1255")
    df_acc = pd.read_csv("static/data/lms/Accidents Type 3/H20141041/H20141041AccData.csv", encoding="cp1255")
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
        size = 50 * np.log(1.1 + df_size_total[row.SEMEL_YISHUV] / float(max_size))
        size_per_severity = df_size[row.SEMEL_YISHUV]
        color = max(0, 200 - 200 * (size_per_severity.get(1, 0) +
                                    size_per_severity.get(2, 0)) /
                    size_per_severity.get(3, 1))
        print size
        app.markers.append({
            "lat": lat,
            "lng": lng,
            "title": row.NAME,
            "size": size,
            "color": color
        })


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/markers", MarkersHandler),
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