import base64
import imghdr
import io
import os

from PIL import Image
from flask import Response
from library.Controller import Controller
from library.Net import Net


class Index(Controller):

    def _initialize(self, arrInput):
        """
        初始化方法
        :param arrInput:
        :return:
        """
        self._url = arrInput.get('url', default=None)
        self._w = arrInput.get('w', default=None)
        self._h = arrInput.get('h', default=None)
        self._x = arrInput.get('x', default='0:0').split(':')
        self._y = arrInput.get('y', default='0:0').split(':')
        len(self._x) < 2 and self._x.append(1)
        len(self._y) < 2 and self._y.append(1)

    def _execute(self):
        """
        执行方法
        :return:
        """
        try:
            result = io.BytesIO()
            resources = Net.scale(self._url)
            if "" == resources:
                raise Exception("")
            type = imghdr.what(resources)
            image = Image.open(resources)
            image = self.__crop(image)
            image = self.__resize(image)
            image.save(result, format=type)
            return Response(result.getvalue(), mimetype=self.__getmimetype(type))
        except (Exception, UnicodeDecodeError):
            result = io.BytesIO()
            Image.open('./static/images/default.png').save(result, format='png')
            return Response(result.getvalue(), mimetype=self.__getmimetype('png'))

    def __getmimetype(self, type):
        """
        返回类型转换
        :param type:
        :return:
        """
        if type == "png":
            return "image/png"
        elif type == "gif":
            return "image/gif"
        return "image/jpeg"

    def __getvalue(self, value, min, max):
        """
        获取边界值
        :param value:
        :param min:
        :param max:
        :return:
        """
        if value > max:
            return max
        elif value < min:
            return min
        return value

    def __crop(self, image):
        """
        图片剪切
        :param image:
        :return:
        """
        size = image.size
        x0 = self.__getvalue(int(self._x[0]), 0, size[0])
        x1 = self.__getvalue(int(self._x[1]), 0, size[0])
        y0 = self.__getvalue(int(self._y[0]), 0, size[1])
        y1 = self.__getvalue(int(self._y[1]), 0, size[1])
        if x0 + x1 > 0 and y0 + y1 > 0:
            return image.crop((x0, y0, x1, y1))
        return image

    def __resize(self, image):
        """
        图片缩放
        :param image:
        :return:
        """
        size = image.size
        rate = size[0] / size[1]
        if self._w and self._h:
            return image.resize((int(self._w), int(self._h)), Image.ANTIALIAS)
        elif self._w and not self._h:
            return image.resize((int(self._w), int(int(size[1]) / rate)), Image.ANTIALIAS)
        elif not self._w and self._h:
            return image.resize((int(int(size[0]) / rate), int(self._h)), Image.ANTIALIAS)
        return image