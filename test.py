#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Project ：python_rendering 
@File    ：test.py
@IDE     ：PyCharm 
@INFO     ： 
@Author  ：BGSPIDER
@Date    ：14/10/2024 下午5:12 
'''
from DrissionPage import ChromiumPage, ChromiumOptions
import base64
import requests
class SingleFile:
    def __init__(self, url, headless=True):
        """
        :param url: 要访问的url
        :param headless: 是否启用无头模式，默认为True
        """
        self.co = ChromiumOptions()
        self.co.set_user_data_path(f'temp')
        self.co.set_address(f'127.0.0.1:22010')
        self.page = ChromiumPage(self.co)
        self.url = url
        self.images = []
        self.javascripts = []
        self.stylelinks = []

    def _get_images(self):
        """
        处理图片img标签资源
        :return:
        """
        # 微信图片预处理
        temp_img_objs = self.page.eles('tag:img')
        for temp_img_obj in temp_img_objs:
            img_url = temp_img_obj.attr("src")
            if img_url:
                if img_url.startswith("data:image/svg+xml,") and "data-src" in temp_img_obj.attrs:
                    img_url = temp_img_obj.attr("data-src")
                    temp_img_obj.set.attr("src", img_url)

        # 遍历img标签
        img_objs = self.page.eles('tag:img')
        for img_obj in img_objs:
            img_url = img_obj.attr("src")

            if img_url:
                if img_url:
                    if img_url.startswith("http"):
                        try:
                            img_content_str = img_obj.src()
                            img_content_base64 = None
                            if img_content_str:
                                img_content_base64 = "data:image/png;base64," + base64.b64encode(img_content_str).decode()
                                img_obj.set.attr("src", img_content_base64)
                            else:
                                try:
                                    img_content_bytes = requests.get(self.url).content
                                    img_content_base64 = "data:image/png;base64," + base64.b64encode(img_content_bytes).decode()
                                    img_obj.set.attr("src", img_content_base64)
                                except:
                                    pass

                            image_dict = {
                                "url": img_url,
                                "content": img_content_str,
                                "data_uri": img_content_base64
                            }
                            self.images.append(image_dict)

                        except Exception as e:
                            print(e)

                    else:
                        print("img标签出现未知类型")
                        exit(-1)

    def _get_javascripts(self):
        """
        处理javascript标签资源
        :return:
        """
        script_objs = self.page.eles('tag:script')
        for script_obj in script_objs:
            script_url = script_obj.attr("src")
            if script_url:
                if script_url.startswith("http"):
                    try:
                        script_content_str = script_obj.src()
                        script_content_base64 = None

                        if not script_content_str:
                            try:
                                script_content_str = requests.get(self.url).text
                            except:
                                pass

                        if script_content_str:
                            script_content_base64 = "data:text/javascript;base64," + base64.b64encode(script_content_str.encode()).decode()
                            script_obj.set.attr("src", script_content_base64)

                        script_dict = {
                            "url": script_url,
                            "content": script_content_str,
                            "data_uri": script_content_base64
                        }
                        self.javascripts.append(script_dict)

                    except Exception as e:
                        print(e)

                else:
                    print("script标签出现未知类型")
                    exit(-1)

    def _get_stylelinks(self):
        """
        处理css link标签资源
        :return:
        """
        stylelink_objs = self.page.eles('tag:link@rel=stylesheet')
        for stylelink_obj in stylelink_objs:
            stylelink_url = stylelink_obj.attr("href")
            if stylelink_url:
                if stylelink_url.startswith("http"):
                    try:
                        stylelink_content_str = stylelink_obj.src()
                        stylelink_content_base64 = None

                        if not stylelink_content_str:
                            try:
                                stylelink_content_str = requests.get(self.url).text
                            except:
                                pass

                        if stylelink_content_str:
                            stylelink_content_base64 = "data:text/css;base64," + base64.b64encode(stylelink_content_str.encode()).decode()
                            stylelink_obj.set.attr("href", stylelink_content_base64)

                        stylelink_dict = {
                            "url": stylelink_url,
                            "content": stylelink_content_str,
                            "data_uri": stylelink_content_base64
                            }
                        self.stylelinks.append(stylelink_dict)

                    except Exception as e:
                        print(e)
                else:
                    print("stylelink标签出现未知类型")
                    exit(-1)

    def get_resource(self, delete_instance=True):
        """
        获取全部img、JavaScript、css资源。调用完此函数默认会删除实例，如需保留实例需要设置delete_instance参数。
        :param delete_instance: 调用完此函数是否删除实例，默认为True。
        :return:
        """
        self.page.get(self.url)
        self._get_images()
        self._get_javascripts()
        self._get_stylelinks()
        if delete_instance:
            self.__del__()

    def save(self, out_file_path=None, encodeing="utf8", delete_instance=True):
        """
        离线保存为文件。调用完此函数默认会删除实例，如需保留实例需要设置delete_instance参数。
        :param out_file_path: html保存路径
        :param encodeing: 文件编码
        :param delete_instance: 调用完此函数是否删除实例，默认为True。
        :return:
        """
        self.get_resource(delete_instance=False)
        # if not out_file_path:
        #     out_file_path = self.page.title + ".html"
        # if not out_file_path:
        out_file_path = "test.html"
        with open(out_file_path, "w", encoding=encodeing) as f:
            f.write(self.page.html)
        print(f"文件保存为：{out_file_path}")
        if delete_instance:
            self.__del__()

    def __del__(self):
        """
        销毁实例
        :return:
        """
        self.page.quit()


if __name__ == '__main__':
    u = '网址'
    sf = SingleFile(u, headless=True)
    sf.get_resource(delete_instance=False)
    sf.save()