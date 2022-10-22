#!/usr/bin/python3

import datetime
import os
from re import sub
import subprocess
import sys
from time import sleep


def change_config(config, rate, batch_size, message_size):
    with open(config, 'r') as f:
        lines = f.readlines()

    flag = False

    for i in range(len(lines)):
        if lines[i].startswith("def remote(ctx):"):
            flag = True
        if flag:
            print(lines[i])
            if lines[i].startswith("        'rate':"):
                lines[i] = f"        'rate': [{rate}],\n"
            elif lines[i].startswith("        'tx_size': "):
                lines[i] = f"        'tx_size': {message_size},\n"
            elif "'batch_size':" in lines[i]:
                lines[i] = f"            'batch_size': {batch_size * message_size},\n"
    with open(config, 'w') as f:
        f.writelines(lines)


if __name__ == "__main__":
    
    message_sizes = [ 16, 32]
    batch_sizes = [200, 500, 1000, 10000, 20000, 50000, 80000, 100000]
    tgt_tp = [20000 , 30000, 50000, 100000, 200000, 450000]
    repeat = 5

    print("Starting benchmarking tool")
    for t in tgt_tp:
        for m in message_sizes:
            for b in batch_sizes:
                for i in range(repeat):
                    run = f"run_m{m}_b{b*m}_t{t}_repeat{i}"
                    now = datetime.datetime.now()

                    print("==============================================================")
                    print(str(now) + " Running test: " + run)

                    change_config("../fabfile.py", t, b, m)
                    subprocess.run(["fab", "remote"])

                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    sleep(1)

    print("Benchmarking finished")