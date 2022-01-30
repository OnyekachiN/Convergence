#!/usr/bin/env python
import pprint
from Bio import SeqIO
#from roskinlib.utils import open_compressed
#import gzip


class SeqCluster(object):
    """A cluster of sequence based objects.

    Class to store a cluster of sequence objects, the cluster members, and the
    cluster representative.
    """
    def __init__(self, name, representative, members):
        self.name = name
        self.representative = representative
        self.members = members

    def __iter__(self):
        """
        Iterating over a cluster is to iterate over its members.
        """
        return self.members.__iter__()

class SeqClusterMember(object):
    """A member of a sequence based cluster.

    Only the name is stored in the cluster member. No sequence is store. That must be
    stored elsewhere.
    """
    def __init__(self, name):
        self.name = name

def UclustIterator(handle):
    clusters = {}
    for line in handle:
        record_label,cluster_number, seq_length,_,_,_,_,_,member_label,rep2 = line.strip().split('\t')
        cluster_number = int(cluster_number)
        seq_length = int(seq_length)
        #elif check and nested if to check for new cluster
        if record_label == 'C':
            pass
        elif record_label == 'S':
            assert cluster_number not in clusters, 'found more than 1 S line for the same cluster ' + cluster_number
            new_member = SeqClusterMember(member_label)
            new_member.sequence_length = seq_length
            clusters[cluster_number] = [new_member]
        elif record_label == 'H':
            assert cluster_number in clusters, 'found H line for cluster before seeing it\'s S line'
            new_member = SeqClusterMember(member_label)
            new_member.sequence_length = seq_length
            clusters[cluster_number].append(new_member)
           
    for cluster_number, cluster_members in clusters.items():
        cluster = SeqCluster(cluster_number, cluster_members[0], cluster_members)
        yield cluster



