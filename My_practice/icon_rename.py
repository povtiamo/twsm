#!/bin/python
#coding=utf8



#这个是用来改icon 图片名字的...
#复制脚本到图标目录下    在命令行中直接运行  python   icon_rename.py
import os
from PIL import Image

ios_size_name = {
	"57_57" : ["Icon.png", "Default~iphone.png", "Icon-57.png"],
	"72_72"	: "Icon-72.png",
	"114_114" : ["Icon@2x.png", "Icon-114.png"],
	"152_152" : "Icon-152.png",
	"120_120" : "Icon-120.png",
	"76_76"   : "Icon-76.png",
	"29_29"   : "Icon-29.png",
	"40_40"   : "Icon-40.png",
	"50_50"   : "Icon-50.png",
	"58_58"   : "Icon-58.png",
	"76_76"   : "Icon-76.png",
	"80_80"   : "Icon-80.png",
	"100_100" : "Icon-100.png",
	"144_144" : "Icon-144.png"
}

android_size_name = {
	"72_72" : "drawable-hdpi",
	"36_36" : "drawable-ldpi",
	"48_48" : "drawable-mdpi",
	"96_96" : "drawable-xhdpi",
	"144_144" : "drawable-xxhdpi"
}

if __name__ == "__main__":
	script_path = "/".join(__file__.split("/")[:-1])
	os.chdir(script_path)

	image_list = os.popen("ls | grep '.png' ").read().split("\n")
	size_map = {}
	for name in image_list:
		if "" == name:
			continue
		img = Image.open(name)
		size_key = "%s_%s" % (img.size[0], img.size[1])
		size_map[size_key] = name

	os.system("mkdir IOS")
	for size_key in ios_size_name:
		img_name = size_map[size_key]

		save_name = ios_size_name[size_key]
		if type(save_name) != list:
			save_name = [save_name]

		for _name in save_name:
			os.system("cp -rf %s IOS/%s" % (img_name, _name) )

	# os.system("mkdir Android")
	# for size_key in android_size_name:
	# 	img_name = size_map[size_key]
	# 	save_folder = android_size_name[size_key]

	# 	if type(save_folder) != list:
	# 		save_folder = [save_folder]

	# 	for _folder in save_folder:
	# 		os.system("cd Android; mkdir %s" % _folder)
	# 		os.system("cp -rf %s Android/%s/icon.png" % (img_name, _folder) )


