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
            'node_num' : node_num,
            'run_id' : ([GeoLogParser.get_new_run_id()] * len(addresses))
            })
        return GeoLogParser._calculate_liveliness(votes_data)
    
    @staticmethod
    def _calculate_liveliness(data):
        total_props  = data['proposals'].sum()
        data['liveliness'] = ((data['votes']+ data['proposals'])/total_props) * 100
        data['liveliness_woprops'] = ((data['votes'])/total_props) * 100
        return data
    
    @staticmethod
    def get_new_run_id():
        # data = pd.read_csv('/home/ubuntu/results/geo-dec-metrics.csv')
        # id = data[data['node_num'] == 0].value_counts()
        # print(id)
        return 1