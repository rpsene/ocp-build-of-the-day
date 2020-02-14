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
import sys
import json
import datetime
import collections
import urllib.request

def get_date():
    """ Get todays' date """
    today=datetime.date.today()
    return today.strftime("%Y-%m-%d")

def get_file_name(x):
    """ Create a file name with today's date" """
    return "./graph-"+x

def get_ocp_builds_info(file_name):
    """ Download the JSON file with all build information """
    urllib.request.urlretrieve("https://openshift-release-ppc64le.svc.ci.openshift.org/graph", filename=file_name)
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

def find_builds(x, structured_data):
    """ Look for today's build and print its information """
    print ("--------------------------------------------------------------------------------------------")
    print ("Summary")
    # This source can be improved, 1 loop is enough for everything.
    for key in structured_data:
        if x in key:    
            print ("https://mirror.openshift.com/pub/openshift-v4/ppc64le/clients/ocp-dev-preview/" + key)
    for key in structured_data:
        if x in key:
            print ("--------------------------------------------------------------------------------------------")
            print (key + " | " + x + " | " + str(key.split("-")[-1:][0]))
            print ("quay.io/openshift-release-dev/ocp-release-nightly:" + key)
            print ("registry.svc.ci.openshift.org/ocp-ppc64le/release-ppc64le:" + key)
            print ("https://mirror.openshift.com/pub/openshift-v4/ppc64le/clients/ocp-dev-preview/" + key)
            print ("oc adm release extract --tools registry.svc.ci.openshift.org/ocp-ppc64le/release-ppc64le:"+key)
            print ("wget https://mirror.openshift.com/pub/openshift-v4/ppc64le/clients/ocp-dev-preview/" + key + "/openshift-install-linux-" + key + ".tar.gz")
            print ("wget https://mirror.openshift.com/pub/openshift-v4/ppc64le/clients/ocp-dev-preview/" + key + "/openshift-client-linux-" + key + ".tar.gz")
            print (structured_data[key])

def cleanup(file):
    """ Delete the JSON file """
    os.remove(file)

def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        raise ValueError("ERROR: date format should be YYYY-MM-DD")
        
def validate_version(version):
    version_list = ["4.3.0","4.4.0"]
    if version in version_list:
        return True
    else:
        print ("Invalid Version")

def run(x):
    """ Run the search for builds """
    file_name=get_file_name(x)
    find_builds(x, structure_data(process_file(get_ocp_builds_info(file_name))))
    cleanup(file_name)

def help():
    """ Help """
    print
    print ("You can use one of the following options:")
    print ("    python3 ./ocp-build-of-the-day.py")
    print ("    python3 ./ocp-build-of-the-day.py YYYY-MM-DD")
    print ("    python3 ./ocp-build-of-the-day.py -v VERSION")
    print

def main(argv):
    """ Do the magic """
    if len(argv) == 0:
        today = get_date()
        run(today)
    elif len(argv) == 1:
        input = argv[0]
        if "-h" in input or "--help" in input:
            help()
        elif validate_date(input):
            today = input
            run(today)
    elif len(argv) == 2:
        input = argv[0]
        if "-v" in input or "--version" in input:
            version = argv[1]
            validate_version(version)
            run(version)
    else:
        help()

if __name__== "__main__":
    main(sys.argv[1:])
