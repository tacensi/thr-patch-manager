#!/usr/bin/env python3
import argparse
from pathlib import Path
import binascii

parser = argparse.ArgumentParser()
parser.add_argument("patchfile", help="name of patch file in YDL format")
# parser.add_argument("-n", "--numpatches", type=int, default=100,
                    # help="number of patches to convert")
args = parser.parse_args()

# header of the single patch files
ydp_header = bytes(b'DTAP\x01\x02\x00\x02\x00')
# empty patch
emptypatch = bytearray(b'Empty\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

# path library opening
pf = open(args.patchfile, 'rb')

if pf:
    #create directory to store single patch files
    filename = Path(args.patchfile)
    dirname = filename.stem
    Path('./'+dirname).mkdir(parents=True, exist_ok=True)

    for i in range(0,100):
        # Calculate offset and set pointer on patchlib
        offset = 13 + (i * 261)
        pf.seek(offset)

        # Load current patch and its name
        currentpatch = bytearray(pf.read(256))
        patchname = currentpatch[0:32]

        # if patch is not empty
        if( patchname != emptypatch ):
            patchname = patchname.decode('utf-8')
            patchname = patchname.rstrip('\0')
            patchname = patchname.strip()
            patchname = patchname.replace('/', '-')

            print(i,patchname)
            patchdump = open("./" + dirname + "/" + str(i) + '.' + patchname + '.ydp', 'wb')
            patchdump.write(ydp_header)
            patchdump.write(currentpatch)
            patchdump.close
        else :
            print(i,'empty')


print("complete")
