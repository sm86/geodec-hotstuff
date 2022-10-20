from glob import glob
from os.path import join
from re import findall, split

import pandas as pd

from benchmark.utils import PathMaker

#########################################################################################
#########################################################################################
#### GeoDec emulator to study impacts of geospatial diversity on blockchain networks ####
############# Created by Shashank Motepalli, Arno Jacobsen ##############################
#########################################################################################
#########################################################################################
class GeoLogParser:
    @staticmethod
    def count_votes_props():
        directory = PathMaker.logs_path()
        addresses = []
        proposals = []
        node_num = []
        for filename in sorted(glob(join(directory, 'node-*.log'))):
            node_num.append(int(filename.split('-')[1].split('.')[0]))
            with open(filename, 'r') as f:
                data = f.read()
                addr_line = findall(r'Node .* successfully booted', data)
                addr = split(' ', addr_line[0])[1]
                addresses.append(addr)
                prop = findall(r'\[(.*Z) .* Created B\d+ -> ([^ ]+=)', data)
                proposals.append(len(prop))
                    
        votes = [0] * len(addresses)
        with open(join(directory, 'node-0.log'), 'r') as f:
            logs = f.read()
            qc_lines = findall(r'QC for block: Round:\d.*', logs)
            for n in range(len(qc_lines)):
                line = qc_lines[n]
                for i in range(len(addresses)):
                    if addresses[i] in line:
                        votes[i] = votes[i] + 1
        votes_data = pd.DataFrame(
            {'address': addresses,
            'votes': votes,
            'proposals': proposals,
            'node_num' : node_num
            })
        return votes_data