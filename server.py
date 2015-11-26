#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import pandas as pd
import tornado.ioloop
import tornado.web

from geo import ItmToWGS84

coordinates_converter = ItmToWGS84()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class MarkersHandler(tornado.web.RequestHandler):
    def get(self):
        df_cities = pd.read_csv("static/data/cities.csv", encoding="cp1255")
        df_acc = pd.read_csv("static/data/lms/Accidents Type 3/H20141041/H20141041AccData.csv", encoding="cp1255")
        groups = df_acc[df_acc.SEMEL_YISHUV > 0].groupby("SEMEL_YISHUV", as_index=False)
        df_size = groups.size()
        df = groups.mean()
        df = pd.merge(df, df_cities, left_on="SEMEL_YISHUV", right_on="SEMEL")
        df = df[pd.notnull(df.X) & pd.notnull(df.Y)]
        markers = []
        for index, row in df.iterrows():
            lng, lat = coordinates_converter.convert(row.X, row.Y)
            markers.append({
                "lat": lat,
                "lng": lng,
                "title": row.NAME,
                "size": df_size[row.SEMEL_YISHUV],
            })
        data = {"markers": markers}
        output = json.dumps(data, ensure_ascii=False).encode("cp1255")
        self.write(output)


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/markers", MarkersHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()