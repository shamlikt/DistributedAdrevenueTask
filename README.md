
# DistributedAdrevenueTask

![admarketplace](https://github.com/shamlikt/DistributedAdrevenueTask/assets/2134692/9c9d29cc-de5d-4167-91e0-0363ff51a915)
This is a scalable solution to the given problem. I have used a distributed data computing library called Dask instead of Pandas.
The user can easily shuffle through local running as well as distributed running based on a simple make command.

## Architecture
There is an application docker, a Dask head node docker, and a Dask worker docker, all created using a docker-compose file.

## Usage
Please note that all the data should be in the `DistributedAdrevenueTask/data` folder for ease of docker execution.

```bash
git clone https://github.com/shamlikt/DistributedAdrevenueTask.git
cd DistributedAdrevenueTask
```

### To initialize the cluster
```bash
make cluster_up
```
Check `http://localhost:8787/status` to verify the status of the cluster.

### To run a sample job locally
```bash
make run_local ads=ads.csv publisher=pubs.csv date=2021-06-02 output=goo.csv
```

### To run a job in cluster mode
```bash
make run_cluster ads=ads.csv publisher=pubs.csv date=2021-06-02 output=goo.csv
```

### To shut down the cluster
```bash
make cluster_down
```
