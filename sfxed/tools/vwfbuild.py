#!/usr/bin/env python
from __future__ import with_statement
from PIL import Image
import array

def ca65_bytearray(s):
    s = ['  .byt ' + ','.join("%3d" % ord(ch) for ch in s[i:i + 16])
         for i in xrange(0, len(s), 16)]
    return '\n'.join(s)

def vwfcvt(filename, tileHt=8):
    im = Image.open(filename)
    pixels = im.load()
    (w, h) = im.size
    (xparentColor, sepColor) = im.getextrema()
    widths = array.array('B')
    tiledata = array.array('B')
    for yt in xrange(0, h, tileHt):
        for xt in xrange(0, w, 8):
            tilew = 8
            for x in xrange(8):
                if pixels[x + xt, yt] == sepColor:
                    tilew = x
                    break
            widths.append(tilew)
            for y in xrange(tileHt):
                rowdata = 0
                for x in xrange(8):
                    pxhere = pixels[x + xt, y + yt]
                    pxhere = 0 if pxhere in (xparentColor, sepColor) else 1
                    rowdata = (rowdata << 1) | pxhere
                tiledata.append(rowdata)
    return (widths, tiledata)

def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv
    if len(argv) > 1 and argv[1] == '--help':
        print "usage: %s font.png font.s" % argv[0]
        return
    if len(argv) != 3:
        print >>sys.stderr, "wrong number of options; try %s --help" % argv[0]
        sys.exit(1)
        
    (widths, tiledata) = vwfcvt(argv[1])
    out = ["; Generated by vwfbuild",
           ".export chrWidths, chrData",
           '.segment "RODATA"',
           '.align 256',
           'chrData:',
           ca65_bytearray(tiledata.tostring()),
           "chrWidths:",
           ca65_bytearray(widths.tostring()),
           '']
    with open(argv[2], 'wb') as outfp:
        outfp.write('\n'.join(out))

if __name__ == '__main__':
##    main(['vwfbuild', '../tilesets/vwf7.png', '../obj/vwf7.s'])
    main()