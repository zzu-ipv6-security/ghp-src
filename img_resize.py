#!/usr/bin/env python3

import argparse
import os

from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=float, default=10)
parser.add_argument('image')
args = parser.parse_args()

prefix, ext = os.path.splitext(args.image)
nimage = prefix + '_resized' + ext

img = Image.open(args.image)
sz = img.size
nsz = (int(sz[0] / args.n), int(sz[1] / args.n))
img_resized = img.resize(nsz)
img_resized.save(nimage)
