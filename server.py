#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class MarkersHandler(tornado.web.RequestHandler):
    def get(self):
        data = {"markers":
            [
                {"lat": 32.0833, "lng": 34.8000, "title": "תל אביב"}
            ]
        }
        print data
        output = json.dumps(data)
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