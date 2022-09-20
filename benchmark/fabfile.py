from fabric import task

from benchmark.local import LocalBench
from benchmark.logs import ParseError, LogParser
from benchmark.utils import Print
from benchmark.plot import Ploter, PlotError
from benchmark.instance import InstanceManager
from benchmark.remote import Bench, BenchError


@task
def test(ctx):
    import oci
    from oci.config import from_file, validate_config
    import os
    # config = from_file()
    # print(config)
    compartment_id = "ocid1.tenancy.oc1..aaaaaaaak5urycwdhjmdgdkfgu3q7wzamv63w6qa6pf4o5ry2dulte6aos4q"
    config = {
        "user": "ocid1.user.oc1..aaaaaaaakturkk3huvbnt6bk64cpi2ffr7t5emxoff2h4xai2unghk33tlra",
        "key_file": "/Users/alberto/.ssh/oci-2.pem",
        "fingerprint": "01:3f:f7:e0:ab:32:06:d8:74:2c:39:d0:bb:81:be:0f",
        "tenancy": compartment_id,
        "region": "us-sanjose-1"
    }
    validate_config(config)
    pool_id = "ocid1.instancepool.oc1.us-sanjose-1.aaaaaaaafmhldzoruib5q4fva5zzcsfk2hg7slggjuinuunt6ekapkolihnq"
    client = oci.core.ComputeManagementClient(config)
    result = client.list_instance_pools(compartment_id)
    # print(result.data)

    result = InstanceManager.make().private_hosts()
    print(result)


@task
def local(ctx):
    ''' Run benchmarks on localhost '''
    bench_params = {
        'faults': 0,
        'nodes': 4,
        'rate': 1_000,
        'tx_size': 512,
        'duration': 20,
    }
    node_params = {
        'consensus': {
            'timeout_delay': 1_000,
            'sync_retry_delay': 10_000,
        },
        'mempool': {
            'gc_depth': 50,
            'sync_retry_delay': 5_000,
            'sync_retry_nodes': 3,
            'batch_size': 15_000,
            'max_batch_delay': 10
        }
    }
    try:
        ret = LocalBench(bench_params, node_params).run(debug=False).result()
        print(ret)
    except BenchError as e:
        Print.error(e)


@task
def create(ctx, nodes=2):
    ''' Create a testbed'''
    try:
        InstanceManager.make().create_instances(nodes)
    except BenchError as e:
        Print.error(e)


@task
def destroy(ctx):
    ''' Destroy the testbed '''
    try:
        InstanceManager.make().terminate_instances()
    except BenchError as e:
        Print.error(e)


@task
def start(ctx, max=2):
    ''' Start at most `max` machines per data center '''
    try:
        InstanceManager.make().start_instances(max)
    except BenchError as e:
        Print.error(e)


@task
def stop(ctx):
    ''' Stop all machines '''
    try:
        InstanceManager.make().stop_instances()
    except BenchError as e:
        Print.error(e)


@task
def info(ctx):
    ''' Display connect information about all the available machines '''
    try:
        InstanceManager.make().print_info()
    except BenchError as e:
        Print.error(e)


@task
def install(ctx):
    ''' Install the codebase on all machines '''
    try:
        Bench(ctx).install()
    except BenchError as e:
        Print.error(e)


@task
def remote(ctx):
    ''' Run benchmarks on AWS '''
    bench_params = {
        'faults': 0,
        'nodes': [120],
        'rate': [400_000],
        'tx_size': 30,
        'duration': 60,
        'runs': 2,
    }
    node_params = {
        'consensus': {
            'timeout_delay': 5_000,
            'sync_retry_delay': 5_000,
        },
        'mempool': {
            'gc_depth': 50,
            'sync_retry_delay': 5_000,
            'sync_retry_nodes': 3,
            'batch_size': 500_000,
            'max_batch_delay': 100
        }
    }
    try:
        Bench(ctx).run(bench_params, node_params, debug=False)
    except BenchError as e:
        Print.error(e)


@task
def plot(ctx):
    ''' Plot performance using the logs generated by "fab remote" '''
    plot_params = {
        'faults': [0],
        'nodes': [16, 32, 64, 120],
        'tx_size': 30,
        'max_latency': [2_000, 5_000]
    }
    try:
        Ploter.plot(plot_params)
    except PlotError as e:
        Print.error(BenchError('Failed to plot performance', e))


@task
def kill(ctx):
    ''' Stop any HotStuff execution on all machines '''
    try:
        Bench(ctx).kill()
    except BenchError as e:
        Print.error(e)


@task
def logs(ctx):
    ''' Print a summary of the logs '''
    try:
        print(LogParser.process('./logs', faults='?').result())
    except ParseError as e:
        Print.error(BenchError('Failed to parse logs', e))
