from glob import glob
from os.path import join
from re import findall, search, match

import pandas as pd

from benchmark.utils import PathMaker

class GeoLogParser:
    @staticmethod
    def count_votes_props():
        directory = PathMaker.logs_path()
        addresses = []
        proposals = []
        for filename in sorted(glob(join(directory, 'node-*.log'))):
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
            'proposals': proposals
            })
        return votes_data