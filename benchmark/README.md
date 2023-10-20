# BigQuery Benchmark
This directory contains benchmark scripts for BigQuery client. It is created primarily for project
maintainers to measure library performance.

## Usage
`python benchmark.py`


### Flags
Run `python benchmark.py -h` for detailed information on available flags.

`--reruns` can be used to override the default number of times a query is rerun. Must be a positive
integer. Default value is 3.

`--projectid` can be used to run benchmarks in a different project.  If unset, the GOOGLE_CLOUD_PROJECT
 environment variable is used.

`--queryfile` can be used to override the default file which contains queries to be instrumented.

`--table` can be used to specify a table to which benchmarking results should be streamed.  The format
for this string is in BigQuery standard SQL notation without escapes, e.g. `projectid.datasetid.tableid`

`--create_table` can be used to have the benchmarking tool create the destination table prior to streaming.

`--tag` allows arbitrary key:value pairs to be set.  This flag can be specified multiple times.

When `--create_table` flag is set, must specify the name of the new table using `--table`.

### Example invocations

Setting all the flags
```
python benchmark.py \
  --reruns 5 \
  --projectid test_project_id \
  --table logging_project_id.querybenchmarks.measurements \
  --create_table \
  --tag source:myhostname \
  --tag somekeywithnovalue \
  --tag experiment:special_environment_thing
```

Or, a more realistic invocation using shell substitions:
```
python benchmark.py \
  --reruns 5 \
  --table $BENCHMARK_TABLE \
  --tag origin:$(hostname) \
  --tag branch:$(git branch --show-current) \
  --tag latestcommit:$(git log --pretty=format:'%H' -n 1)
```

## BigQuery Benchmarks In Other Languages
* Go: https://github.com/googleapis/google-cloud-go/tree/main/bigquery/benchmarks
* JAVA: https://github.com/googleapis/java-bigquery/tree/main/benchmark
