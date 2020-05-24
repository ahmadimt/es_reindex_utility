#!/usr/bin/env python3

"""Elasticsearch Reindexing CLI: A simple Python script to re-index an Elasticsearch index and track it's progress.

Usage:
    reindex.py reindex <url> <source_index> <dest_index> [--username=<username>] [--password=<password>]
    reindex.py reindex -h|--help
    reindex.py reindex -v|--version
    
Options:
    url   Base Url of Elasticsearch including port. e.g 'http://localhost:9200'
    source_index  Source Index
    dest_index    Destination Index
    -h --help  Show this screen
    -v --version  Show version
"""


import requests
from requests.auth import HTTPBasicAuth
import time
from docopt import docopt


def reindex(url, source_index, dest_index, username=None, password=None):
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(username, password)
    response = requests.post(
        url + "/_reindex?slices=5&wait_for_completion=false",
        headers=headers,
        auth=auth,
        json={"source": {"index": source_index}, "dest": {"index": dest_index}},
    )
    taskId = response.json().get("task")
    print("Task Id for the request => " + response.json().get("task"))
    taskDetailsUrl = url + "/_tasks/" + taskId
    taskDetails = requests.get(taskDetailsUrl, auth=auth).json()
    while taskDetails.get("completed") == False:
        time.sleep(30)
        taskDetails = requests.get(taskDetailsUrl, auth=auth).json()
    print("Details of the task on completion =>\n", taskDetails)


if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1")
    if (
        arguments["<url>"],
        arguments["<source_index>"],
        arguments["<dest_index>"],
        arguments["--username"],
        arguments["--password"],
    ):
        reindex(
            arguments["<url>"],
            arguments["<source_index>"],
            arguments["<dest_index>"],
            arguments["--username"],
            arguments["--password"],
        )
    elif (arguments["<url>"], arguments["<source_index>"], arguments["<dest_index>"]):
        reindex(
            arguments["<url>"], arguments["<source_index>"], arguments["<dest_index>"]
        )
    else:
        print(arguments)
