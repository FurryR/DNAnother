#!/bin/bash
# This program was under the LGPLv2.1 license.
# Copyright (c) 2021 awathefox.
echo "正在安装需要的组件，请稍等。"
sudo apt update
sudo apt upgrade
sudo apt install python3 git brotli android-sdk-libsparse-utils zip unzip -y
sudo pip3 install common protobuf six bsdiff4 lzma
echo "正在下载组件..."
git clone https://github.com/awathefox/DNAnother.git
cd DNAnother
sudo python3 DNAnother.py
