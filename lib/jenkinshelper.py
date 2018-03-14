#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


import urllib2
import base64
import ast
import os
import re
from lib import filehelper


class JenkinsHelper(object):

    """
    jenkins helper: that abstract functions interact with Jenkins
    """

    def __init__(self, url, user, api_key):
        self.url = url
        self.user = user
        self.api_key = api_key

    def get_packages(self, job, build, pattern=None):
        """
        usage: get all packages full path
        :param job: jobname
        :param build: build number
        :return: packages name list
        """
        packages = []
        if build == -1:
            build = self.get_last_successful_build_number(job)
        #get_build_run is used for matrix configuration job
        runs = self._get_build_run(job, build)
        if runs is not None:
            for run in runs:
                package_names = self._get_packages_from_url(run['url'])
                for package_name in package_names:
                    if pattern:
                        if JenkinsHelper._is_package_include(package_name, pattern):
                            packages.append(package_name)
                    else:
                        packages.append(package_name)

        else:
            url = "%s/job/%s/%s/" %(self.url, job, build)
            package_names = self._get_packages_from_url(url)
            for package_name in package_names:
                if pattern:
                     if JenkinsHelper._is_package_include(package_name, pattern):
                        packages.append(package_name)
                else:
                    packages.append(package_name)
        return packages

    def download_package(self, download_url, dest):
        """
        :param download_url:
        :param dest:
        :return: local destination of download package
        """
        package = download_url.split('/')[-1]
        filehelper.FileHelper().create_directory(dest)
        dest_full_path = os.path.join(dest,package)
        req = urllib2.Request(download_url)
        req.add_header('Authorization', self._auth_header())

        if filehelper.FileHelper().file_exist(dest_full_path):
            filehelper.FileHelper().delete_file(dest_full_path)

        with open(dest_full_path, 'wb') as output:
            output.write(urllib2.urlopen(req).read())

        return dest_full_path

    def download_packages(self,packages,dest):
        packages_downloaded = []
        for url in packages:
            packages_downloaded.append(self.download_package(url, dest))
        return packages_downloaded

    def get_last_successful_build_number(self, job):
        http_request = "%s/job/%s/lastStableBuild/buildNumber" %(self.url, job)
        number = self._jenkins_api_call(http_request)
        return number


    @staticmethod
    def _is_package_include(url, pattern=None):
        result = False
        package_name = url.split("/")[-1]
        if re.compile(pattern).match(package_name):
            result = True

        return result

    def _get_packages_from_url(self, url):
        packages = []
        api_url = "%sapi/python?pretty=true" % (url)
        artifacts = []
        try:
            result = self._jenkins_api_call(api_url)
            if result:
                artifacts = result["artifacts"]
            # artifacts = self._jenkins_api_call(api_url)["artifacts"]
        except urllib2.URLError as e:
            print e
        if artifacts:
            for artifact in artifacts:
                packages.append(url + "artifact/" + artifact['relativePath'])
        return packages

    def _get_build_run(self, job, build):
        result = None
        data = self._get_build_info(job, build)
        if not data:
            # LogHelper.error("Fail to get build info from Jenkins.")
            print("Fail to get build info from Jenkins.")
        else:
            if data.has_key("runs"):
                result = data["runs"]
        return result

    def _get_build_info(self, job, build):
        url = "%s/job/%s/%d/api/python?pretty=true" % (self.url, job, build)
        return self._jenkins_api_call(url)

    def _auth_header(self):
        return "Basic " + base64.encodestring("%s:%s" % (self.user, self.api_key)).strip()

    def _jenkins_api_call(self, url):
        try:
            req = urllib2.Request(url)
            req.add_header('Authorization', self._auth_header())
            data = urllib2.urlopen(req).read()
            result = ast.literal_eval(data)
        except urllib2.URLError as e:
            result = None
        return result


