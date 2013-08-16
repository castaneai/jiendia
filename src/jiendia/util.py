# -*- coding: utf-8 -*-
import os

def get_latale_dir():
    u"""Windowsの環境変数からラ・セーヌがインストールされているディレクトリのパスを返す
    標準以外の場所にインストールされている場合は取得できないのでNoneを返す"""
    pf_dir = None
    if 'ProgramFiles(x86)' in os.environ:
        pf_dir = os.environ['ProgramFiles(x86)']
    elif 'ProgramFiles' in os.environ:
        pf_dir = os.environ['ProgramFiles']
    else:
        return None

    latale_dir = '{0}/Gamepot/LaTale'.format(pf_dir)
    if os.path.exists(latale_dir):
        return latale_dir
    else:
        return None
