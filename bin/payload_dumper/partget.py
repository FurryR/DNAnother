#!/usr/bin/env python
import struct
import argparse
import update_metadata_pb2 as um

def u32(x):
    return struct.unpack('>I', x)[0]

def u64(x):
    return struct.unpack('>Q', x)[0]




parser = argparse.ArgumentParser(description='OTA payload partition lister')
parser.add_argument('payloadfile', type=argparse.FileType('rb'),
                    help='payload file name')
args = parser.parse_args()

#Check for payload file exists

magic = args.payloadfile.read(4)
assert magic == b'CrAU'

file_format_version = u64(args.payloadfile.read(8))
assert file_format_version == 2

manifest_size = u64(args.payloadfile.read(8))

metadata_signature_size = 0

if file_format_version > 1:
    metadata_signature_size = u32(args.payloadfile.read(4))

manifest = args.payloadfile.read(manifest_size)
metadata_signature = args.payloadfile.read(metadata_signature_size)

data_offset = args.payloadfile.tell()

dam = um.DeltaArchiveManifest()
dam.ParseFromString(manifest)
block_size = dam.block_size

for part in dam.partitions:
    print(part.partition_name)

