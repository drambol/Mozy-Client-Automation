#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong

import json
import os

from apps.linux.linux_app.controller.lynx_controller import LynxCtrl
from lib.filehelper import FileHelper

class Backupset(object):

    def __init__(self, name, **kwargs):
        self.config = {}
        self.config["name"] = name
        self.__set_path(kwargs)
        self.__set_exclude(kwargs)
        self.__set_exclusionary(kwargs)
        self.__set_rules(kwargs)

    def to_json(self,):
        content = {}
        content['backupsets'] = []
        content['backupsets'].append(self.config)
        return json.dumps(content, indent=4, separators=(',', ': '), sort_keys=True)

    def __set_exclude(self, args):
        self.config["excludes"] = []
        if "excludes" in args.keys():
            if type(args["excludes"]) == list:
                self.config["excludes"] = args["excludes"]
            else:
                self.config["excludes"].push(args["excludes"])

        return self.config["excludes"]

    def __set_path(self, args):
        self.config["paths"] = []
        if "paths" in args.keys():
            if type(args["paths"]) == list :
                self.config["paths"] = args["paths"]
            else:
                self.config["paths"].append(args["paths"])

        return self.config["paths"]

    def __set_exclude(self, args):
        if args.get('excludes'):
            self.config["excludes"] = []
            if type(args["excludes"]) == list:
                self.config["excludes"] = args["excludes"]
            else:
                self.config["excludes"].append(args["excludes"])

    def __set_exclusionary(self, args):
        is_exclusionary = args.get('exclusionary') or None
        if is_exclusionary.upper() == 'TRUE':
            self.config['exclusionary'] = True
        else:
            self.config['exclusionary'] = False

    def __set_rules(self, args):
        self.config["rules"] = {}
        have_filenames_rules = args.get('filenames')
        have_exclude_filenames_rules = args.get('exclude_filenames')
        have_filetypes_rules = args.get('filetypes')
        have_exclude_filetypes_rules = args.get('exclude_filetypes')

        if have_filenames_rules:
            self.config["rules"]['filenames'] = have_filenames_rules

        if have_exclude_filenames_rules:
            self.config["rules"]['exclude_filenames'] = have_exclude_filenames_rules

        if have_filetypes_rules:
            self.config['rules']['filetypes'] = have_filetypes_rules

        if have_exclude_filetypes_rules:
            self.config['rules']['exclude_filetypes'] = have_exclude_filetypes_rules

    def generate_json_file(self, filename ="backupset.json", conf_dir=None):
        if not conf_dir:
            conf_dir = LynxCtrl.conf_dir

        if not filename.endswith(".json"):
            filename += ".json"

        full_path = os.path.join(conf_dir, filename)
        with open(full_path, "w+") as f:
            f.write(self.to_json())

        return full_path
