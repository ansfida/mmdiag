#!/usr/bin/python
from mobile_insight.monitor import OfflineReplayer
from mobilitymisconfiggsmcdma_analyzer import MobilityMisconfigGsmCdmaAnalyzer
import collections
import numpy as np
import os
import pickle
import re
import sys
import json

def get_sorted_logs(fileMi2logText):
    content = []
    with open(fileMi2logText) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def parse_qmdl(plainTextFile):
    # Initialize an OfflineReplayer as monitor
    src = OfflineReplayer()
    m = MobilityMisconfigGsmCdmaAnalyzer()

    for f in get_sorted_logs(plainTextFile):
        m.reset()
        m.set_source(src)
        src.set_input_path(f)

        # Start the monitoring
        src.run()

        gsm_mobility_misconfig_serving_cell_dict = m.get_gsm_mobility_misconfig_serving_cell_dict()
        cdma_mobility_misconfig_serving_cell_dict = m.get_cdma_mobility_misconfig_serving_cell_dict()
        evdo_mobility_misconfig_serving_cell_dict = m.get_evdo_mobility_misconfig_serving_cell_dict()

        filename = str(f)
        print filename
        carrier = "Unknown"
        try:
            carrier = (filename.split('.mi2log')[0]).split('_')[-1]
        except:
            carrier = "Unknown"

        for CellIdentityCombine, CellInfo in gsm_mobility_misconfig_serving_cell_dict.iteritems():
            CellIdentityCombine = (carrier,) + CellIdentityCombine
            print CellIdentityCombine
            InfoKey = "gsm_cell_information"
            if InfoKey in CellInfo:
                print InfoKey
                for InfoValueItem in CellInfo[InfoKey]:
                    print InfoValueItem
            InfoKey = "gsm_reselection_parameters"
            if InfoKey in CellInfo:
                print InfoKey
                for InfoValueItem in CellInfo[InfoKey]:
                    print InfoValueItem

            print "-----------------------------------------------------------"

        for CellIdentityCombine, CellInfo in cdma_mobility_misconfig_serving_cell_dict.iteritems():
            CellIdentityCombine = (carrier,) + CellIdentityCombine
            print CellIdentityCombine
            InfoKey = "cdma_paging"
            if InfoKey in CellInfo:
                print InfoKey
                for InfoValueItem in CellInfo[InfoKey]:
                    print InfoValueItem

            print "-----------------------------------------------------------"

        for CellIdentityCombine, CellInfo in evdo_mobility_misconfig_serving_cell_dict.iteritems():
            CellIdentityCombine = (carrier,) + CellIdentityCombine
            print CellIdentityCombine
            InfoKey = "evdo_sector_parameters"
            if InfoKey in CellInfo:
                print InfoKey
                for InfoValueItem in CellInfo[InfoKey]:
                    print InfoValueItem
            InfoKey = "evdo_other_rat"
            if InfoKey in CellInfo:
                print InfoKey
                for InfoValueItem in CellInfo[InfoKey]:
                    print InfoValueItem

            print "-----------------------------------------------------------"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage python main_gsmcdma.py [plain text file containing path to mi2log files]"
        exit()
    parse_qmdl(sys.argv[1])
