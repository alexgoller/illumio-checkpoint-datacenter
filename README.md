# Illumio PCE Workload Export Script

Checkpoint has introduced a way to dynamically read and add objects to policy from a generic data structure that
is available as a file retrieved via http(s) or locally. The file structure is explained here:

https://support.checkpoint.com/results/sk/sk167210


This script is used to connect to an Illumio Policy Compute Engine (PCE), retrieve information about workloads, and export this information in a JSON format compatible with Check Point firewalls.

## Requirements

- Python 3
- `illumio` Python library

## Usage

You can run the script using the following command:

```
python illumio-checkpoint-datacenter.py --pce_host <host> --pce_port <port> --pce_org <org> --pce_api_user <api_user> --pce_api_secret <api_secret> --labels <label1,label2,label3> --limit <limit> --output <output_file>
```

Replace `<host>`, `<port>`, `<org>`, `<api_user>`, `<api_secret>`, `<label1,label2,label3>`, `<limit>` and `<output_file>` with the appropriate values.

## Arguments

- `--pce_host` (required): The host address of the PCE.
- `--pce_port`: The port of the PCE. Default is `443`.
- `--pce_org`: The organization ID for the PCE. Default is `1`.
- `--pce_api_user` (required): The API user for the PCE.
- `--pce_api_secret` (required): The API secret for the PCE.
- `--labels`: A comma-separated list of labels to retrieve. Default is `role`, `app`, `env`, `loc`. There should be no spaces in between the labels.
- `--limit`: The maximum number of workloads to retrieve. Default is `500`.
- `--output`: The output file to write the JSON data to. Default is `illumio-checkpoint.json`.

## Output

The script outputs a JSON file containing information about each workload. The JSON data is in a format compatible with Check Point firewalls. If an output file is not specified, the JSON data is printed to the console.

## Example

To run the script with default settings, you can use the following command:

```
python illumio-checkpoint-datacenter.py --pce_host myhost.com --pce_api_user myuser --pce_api_secret mysecret
```

This will connect to the PCE at `myhost.com` using the specified API user and secret, retrieve information about up to 500 workloads, and write the information to `illumio-checkpoint.json`.
