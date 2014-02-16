#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------
# 打包程序

from distutils.core import setup
import py2exe,glob

setup(windows=[{
            "script": 'calc.py',}],
      data_files=[
        #因为客户机可能缺少部分开发文件造成无法运行程序，需要打包一些文件
        (".",glob.glob("dlls/*.*")),
        ],
      options={"py2exe":{"includes":["sip"],
                         "optimize":2,
                         #打包成一个文件，加快读取速度
                         "compressed":1,
                         "bundle_files":2,
                         #文件放在哪里
                         "dist_dir":"temp/dist",
                         #少了个文件,不管它
                         "dll_excludes":["MSVCP90.dll"],
                         },
          
               },
      zipfile=None,)#一个文件


import shutil
shutil.rmtree('build')