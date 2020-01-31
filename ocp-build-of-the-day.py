# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 IBM Corporation
Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
    Contributors:
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""

import os
import json
import urllib
import collections
from datetime import date

def get_date():
    """ Get todays' date """
    today=date.today()
    return today.strftime("%Y-%m-%d")

def get_file_name(current_date):
    """ Create a file name with today's date" """
    return "./graph-"+current_date

def get_ocp_builds_info(file_name):
    """ Download the JSON file with all build information """
    urllib.urlretrieve("https://openshift-release-ppc64le.svc.ci.openshift.org/graph", filename=file_name)
    return file_name

def process_file(file_name):
    """ Process the JSON file """
    fp = open(file_name, "r")
    obj = json.load(fp)
    fp.close()
    return obj

def structure_data(raw_data):
    """ Create a dictionary with the raw values and sort it """
    builds = {}
    for node in raw_data["nodes"]:
        version = node["version"]
        payload = node["payload"]
        builds[version]=payload
    od = collections.OrderedDict(sorted(builds.items()))
    return od

def find_builds(current_date, structured_data):
    """ Look for today's build and print its information """
    for key in structured_data:
        if current_date in key:
            print ("--------------------------------------------------------------------------------------------")
            print (key + " | " + current_date + " | " + str(key.split("-")[-1:][0]))
            print ("quay.io/openshift-release-dev/ocp-release-nightly:" + key)
            print ("registry.svc.ci.openshift.org/ocp-ppc64le/release-ppc64le:" + key)
            print ("https://mirror.openshift.com/pub/openshift-v4/ppc64le/clients/ocp-dev-preview/" + key)
            print (structured_data[key])

def cleanup(file):
    """ Detele the JSON file """
    os.remove(file)

def main():
    """ Do the magic """
    today = get_date()
    file_name=get_file_name(today)
    find_builds(today, structure_data(process_file(get_ocp_builds_info(file_name))))
    cleanup(file_name)

if __name__== "__main__":
    main()
