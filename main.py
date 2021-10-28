import cv2
import numpy as np
import psutil
import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header
from urllib import parse
import ssl
import urllib.request
import io

port = 12345


class HttpRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse.parse_qsl(
                self.rfile.read(length),
                encoding='utf-8',
                errors='replace',
                keep_blank_values=1)
        else:
            postvars = []

        postvars = dict(postvars)

        url = postvars.get(b'url', "").decode()
        id = postvars.get(b'id', 0).decode()

        res_json = wall(id, url)

        self.wfile.write(res_json.encode())


def memory_usage(message: str = 'debug'):
    # current process RAM usage
    p = psutil.Process()
    rss = p.memory_info().rss / 2 ** 20 # Bytes to MB
    print(f"[{message}] memory usage: {rss: 10.5f} MB")


def url_to_image(url):
    context = ssl._create_unverified_context()

    resp = urllib.request.urlopen(url, context=context)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


def wall(id, url):
    image = url_to_image(url)
    image1 = np.zeros(image.shape, np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    outer_ret, outer_wall = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY_INV)

    mask1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    mask2 = cv2.getStructuringElement(cv2.MORPH_RECT, (200, 200))

    outer_wall = cv2.erode(outer_wall, mask1, iterations=2)
    outer_wall = cv2.dilate(outer_wall, mask1, iterations=2)

    outer_wall = cv2.dilate(outer_wall, mask2, iterations=1)
    outer_wall = cv2.erode(outer_wall, mask2, iterations=1)

    outer_wall = cv2.erode(outer_wall, mask1, iterations=1)
    outer_wall = cv2.dilate(outer_wall, mask1, iterations=1)

    ret, wall_obj = cv2.threshold(image, 45, 255, cv2.THRESH_BINARY_INV)

    mask3 = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))

    wall_obj = cv2.erode(wall_obj, mask3, iterations=2)
    wall_obj = cv2.dilate(wall_obj, mask3, iterations=3)

    inner_wall = outer_wall - wall_obj
    inner_wall = cv2.erode(inner_wall, mask3, iterations=1)

    contours, hierarchy = cv2.findContours(inner_wall, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = {}

    for i in range(len(contours)):
        epsilon = 0.001*cv2.arcLength(contours[i], True)
        approx = cv2.approxPolyDP(contours[i], epsilon, True)
        points[i] = approx.reshape(approx.shape[0], 2)
        points[i] = points[i].tolist()

        cv2.drawContours(image1, [approx], 0, (0, 255, 0), 3)

    json_obj = {"id": id, "points": points}
    json_string = json.dumps(json_obj, sort_keys=True, indent=4)

    return json_string


server = HTTPServer(('', port), HttpRequestHandler)
server.serve_forever()

