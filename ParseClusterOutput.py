#!/usr/bin/env python

import sys
import UclustParserNoConsensus
from roskinlib.utils import open_compressed
import argparse
from Bio import SeqIO
from pathlib import Path
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('directory_path', metavar='directory', help='the direcotry that has the putput of UCLUST')
    parser.add_argument('--cuttoff', metavar='N', type=int, default=5, help='minimum number of subjects in a cluster')
    
    
    args = parser.parse_args()
    cluster_file = args.directory_path + '/clusters.uc'

    with open_compressed(cluster_file, 'rt') as cluster_handle:
        for cluster in UclustParserNoConsensus.UclustIterator(cluster_handle):
            read_count = 0
            cluster_subjects = set()
            cluster_members = set()
            for member in cluster:
                cluster_members.add(member.name)
                for read in member.name.split(","):
                    read_count += 1
                    subject_id, clone_id, read_id = read.split(";")
                    cluster_subjects.add(subject_id)
            if len(cluster_subjects) >= args.cuttoff:
                print('Cluster'+str(cluster.name), *cluster_members, sep ='\t')
                shutil.copy(args.directory_path + '/cluster_aligns/align' + str(cluster.name), 'data/cluster_aligns/cluster_aligns' + str(cluster.name))

if __name__ == '__main__':
    sys.exit(main())
