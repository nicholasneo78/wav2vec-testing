#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Helper script to pre-compute embeddings for a flashlight (previously called wav2letter++) dataset
"""

import argparse
import os
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--output-name", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    transcriptions = {}

    with open(args.tsv, "r") as tsv, open(
        os.path.join(args.output_dir, args.output_name + ".ltr"), "w"
    ) as ltr_out, open(
        os.path.join(args.output_dir, args.output_name + ".wrd"), "w"
    ) as wrd_out:
        root = next(tsv).strip()
        print()
        print(f'root: {root}')
        for line in tsv:
            line = line.strip()
            print(f'line info: {line}')
            #dir = os.path.dirname(line)

            # hardcode dir first
            #parts = ['84', '121123', '0023', 'trans', 'txt']

            # finding and breaking the string line using regex
            parts = re.split('-|\.', line)

            dir = f'{parts[0]}-{parts[1]}'

            #print(f'transcriptions: {transcriptions}')
            if dir not in transcriptions:
                #parts = dir.split(os.path.sep)
                #debug - hardcode
                #parts = ['84', '121123', '0023', 'trans', 'txt']
                #print(f'Parts 1: {parts[0]}')
                #print(f'Parts 2: {parts[1]}')
                # get the trascription path, concatenate from dir
                trans_path = f"{dir}.trans.txt"
                
                #path = os.path.join(root, dir, trans_path)
                path = os.path.join(root, trans_path)

                print(f'path: {path}')
                assert os.path.exists(path)
                texts = {}
                with open(path, "r") as trans_f:
                    for tline in trans_f:
                        items = tline.strip().split()
                        texts[items[0]] = " ".join(items[1:])
                
                # redefined dir (hardcode first)
                #dir = '84-121123'
                transcriptions[dir] = texts
                # hardcode
                #transcriptions['84-121123'] = texts
            part = os.path.basename(line).split(".")[0]
            assert part in transcriptions[dir]
           
            print(transcriptions[dir][part], file=wrd_out)
            print(
                " ".join(list(transcriptions[dir][part].replace(" ", "|"))) + " |",
                file=ltr_out,
            )
            print()
        print(f'final transcriptions: {transcriptions}')

if __name__ == "__main__":
    main()
