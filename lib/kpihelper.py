import re
import time, datetime
from copy import deepcopy

from lib.platformhelper import PlatformHelper
from lib.filehelper import FileHelper
from lib.loghelper import LogHelper
from lib.kpi import KPI


class KPIHelper(object):
    extracted_kpis = dict()
    testcase = ""
    hostname = None
    ip = None
    thost = None
    client = None
    env = None
    currentkpi = None

    @staticmethod
    def extract_kpi(logfile, starttime=None, hostname=None, ip=None, env="QA12"):
        if logfile:
            if hostname:
                KPIHelper.hostname = hostname
            if ip:
                KPIHelper.ip = ip
            if env:
                KPIHelper.env = env

            KPIHelper.get_kpis(logfile, starttime)

            print starttime
            print len(KPIHelper.extracted_kpis)

        else:
            LogHelper.info("WARNING: There is no log file found.")

    @staticmethod
    def get_started(file, start):
        """
        Get the started line number from log.
        :param file: file
        :param start: time after start
        :return: int(line number)
        """
        if PlatformHelper.is_win():
            search_pattern = re.compile("^(.*\s.*)\s.*\.exe.*$", re.IGNORECASE)
        elif PlatformHelper.is_Linux():
            search_pattern = re.compile("^(.*)\.\d{6}.*$", re.IGNORECASE)
        indices = FileHelper.find_text_indices(file, search_pattern)
        return indices[0]

    @staticmethod
    def get_backup_start(file):
        search_pattern = "start backup"
        if PlatformHelper.is_win():
            search_pattern = "Starting backup:"
        elif PlatformHelper.is_Linux():
            search_pattern = "Executing : start"
        elif PlatformHelper.is_mac():
            search_pattern = "Starting backup:"
        else:
            pass

        indices = FileHelper.find_text_indices(file, search_pattern)
        if indices:
            return indices[-1]

    @staticmethod
    def get_win_apicode(kpi, line):
        """
        line = "26Sep2017 09:37:34 mozyprobackup.exe: DEBUG 23080 0000000001D54AA0 mordor:http:client http\client.cpp:485 127-1 HTTP/1.1 304 Not Modified"
        result:
                26Sep2017 09:37:34
                mozyprobackup.exe
                304
                Not Modified
        """
        apicodepattern = re.compile(
            "^(.*)\s(.*\.exe).*\s+HTTP/1.1\s(\d+)\s(.*)$", re.IGNORECASE)
        apicodeinfo = re.match(apicodepattern, line)
        if apicodeinfo is not None and apicodeinfo.groups():
            print line
            groups = apicodeinfo.groups()
            kpi.set_apicode(groups)

        return kpi

    @staticmethod
    def get_linux_apicode(kpi, line):
        """
        line = "2017-09-25T23:21:40.185991 534263 DEBUG 30042 0x7fa9c00014d0 mordor:http:client client.cpp:485 16-11 HTTP/1.1 200 OK"
        result:
                2017-09-25T23:21:40
                185991
                16-11
                200
                OK
        """
        apicodepattern = re.compile(
            "^(.*)\.(\d{6}).*\s(\d+\-\d+)\sHTTP/1.1\s(\d+)\s(.*)$", re.IGNORECASE)
        apicodeinfo = re.match(apicodepattern, line)
        if apicodeinfo is not None and apicodeinfo.groups():
            print line
            groups = apicodeinfo.groups()
            kpi.set_apicode(groups)

            KPIHelper.extracted_kpis[groups[2]] = kpi
        return kpi

    @staticmethod
    def get_windows_kpi(kpi, line, starttime):
        """
        line = "26Sep2017 11:45:30 mozyprobackup.exe: DEBUG 16016 0000000001E25780 mordor:http:client http\client.cpp:476 27-13 GET /client/get_config?arch=x64&codename=mozypro&country=CN&machineid=f00f0896217f80c72aedcedabd64db5b0daffa61&os1=6&os2=1&os3=7601&os4=1&os5=0&os6=4&platform=win&product_key=Q86QZTBVER3WRS2G4FBF&user=4b6d60ab12e6cd983f2990cff853a972a475d8d9&ver=2.34.0.600 HTTP/1.1"
        result:
                26Sep2017 11:45:30
                mozyprobackup.exe
                27-13
                GET
                /client/get_config?arch=x64&codename=mozypro&coun...

        """
        # skip /dev/null api
        apipattern = re.compile(
            "^(.*)\s(.*\.exe).*\s(\d+-\d+)\s(GET|HEAD|PUT|DELETE|POST)\s(.*[^/dev/null])\sHTTP/1.1$", re.IGNORECASE)
        clientpattern = re.compile(
            "^(.*)\s(.*\.exe).*\s+(Starting (backup|restore)).*$", re.IGNORECASE)
        """
        line = "26Sep2017 09:37:34 mozyprobackup.exe: DEBUG 23080 0000000001D54AA0 mordor:http:client http\client.cpp:485 127-1 HTTP/1.1 304 Not Modified"
        result:
                26Sep2017 09:37:34
                mozyprobackup.exe
                127-1
                304
                Not Modified
        """
        apicodepattern = re.compile(
            "^(.*)\s(.*\.exe).*\s(\d+-\d+)\sHTTP/1.1\s(\d+)\s(.*)$", re.IGNORECASE)

        """
        line="26Sep2017 14:48:49 mozyprobackup.exe: Finished backup with code: 0x00000000 0 1 1"
        result:
            26Sep2017 14:48:49
            mozyprobackup.exe
            Finished backup
            backup
            0x00000000
        """
        backupresultpattern = re.compile(
            "(.*)\s(.*\.exe).*\s(Finished (backup|restore))\s.*:\s(0x\w+)[\s\d]+$",
            re.IGNORECASE)

        """
        line="11Oct2017 17:55:48 mozyprobackup.exe: Error: Restore failed with code 0xfff00003"
        result:
            11Oct2017 17:55:48
            mozyprobackup.exe
            Restore
            0xfff00003
        """

        restoreresultpattern = re.compile("(.*)\s(.*\.exe).*\sError:\s(Restore) failed.*(0x\w+)$", re.IGNORECASE)

        """
        16Nov2017 17:00:00 MozyEnterpriseconf.exe: Error: ErrorDialog - ConnectionError9 : Unable to connect to MozyEnterprise servers
        """
        # clienterrorpattern = re.compile("(.*)\s(.*\.exe).*\sError:\sErrorDialog\s-\s(.*Error\d+)\s:\s(.*)$", re.IGNORECASE)
        clienterrorpattern = re.compile("(.*)\s(.*\.exe).*\sError:\sErrorDialog\s-\s(.*Error.*)$", re.IGNORECASE)
        """
        X-Extended-Error-Code: 507
        """
        apiextenderrorpattern = re.compile("^X-Extended-Error-Code: (\d+)", re.IGNORECASE)

        hostpattern = re.compile("^host:\s(.*.com)", re.IGNORECASE)
        testclientpattern = re.compile("^User-Agent: (.*)", re.IGNORECASE)

        apiinfo = re.match(apipattern, line)
        apicodeinfo = re.match(apicodepattern, line)
        clientinfo = re.match(clientpattern, line)
        backupresult = re.match(backupresultpattern, line)
        restoreresult = re.match(restoreresultpattern, line)
        clienterrorinfo = re.match(clienterrorpattern, line)
        hostinfo = re.match(hostpattern, line)
        testclientinfo = re.match(testclientpattern, line)
        extenderrorinfo = re.match(apiextenderrorpattern, line)    # API response with extend error code for easier analyse

        if apiinfo is not None:
            apigroups = apiinfo.groups()
            if apigroups and datetime.datetime.strptime(apigroups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ') > starttime:
                # print line
                # print datetime.datetime.strptime(groups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
                # print time.strptime(groups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                name = apigroups[4].split("?")[0]
                kpi = KPI(testcase=KPIHelper.testcase, category="Service",
                          start_time=datetime.datetime.strptime(apigroups[0], '%d%b%Y %H:%M:%S').strftime(
                              '%Y-%m-%dT%H:%M:%SZ'),
                          apimethod=apigroups[3], name=name, message=line, hostname=KPIHelper.hostname, ip=KPIHelper.ip,
                          client=KPIHelper.client, env=KPIHelper.env)

                if "log_transfer" in name:
                    match_result = re.match(r"^.*(data_transfered_rate_avg)=(\d+)\&.*", apigroups[4])
                    if KPIHelper.extracted_kpis.has_key(apigroups[1]) and KPIHelper.extracted_kpis[apigroups[1]].apicode is None:
                        KPIHelper.extracted_kpis[apigroups[1]].end_time = None
                        KPIHelper.extracted_kpis[apigroups[1]].result = "TIMEOUT"
                        KPIHelper.extracted_kpis[apigroups[1]].write_to_elasticsearch()
                        # Remove the key as this means API timeout without response.
                        KPIHelper.extracted_kpis.pop(apigroups[1], None)

                    if match_result:
                        KPIHelper.extracted_kpis["backup"].throughput = round(int(match_result.groups()[1]) / 1000/8)
                        KPIHelper.extracted_kpis["backup"].thost = KPIHelper.thost
                        KPIHelper.extracted_kpis["backup"].client = KPIHelper.client
                        if KPIHelper.extracted_kpis["backup"].throughput > 0:
                            """
                            Known client issue, restore status is sent in next backup. Skip this log transfer.
                            """
                            KPIHelper.extracted_kpis["backup"].write_to_elasticsearch()

                        # kpi.throughput = round(int(match_result.groups()[1]) / 1000/8)     # kilo byte per sec
                else:
                    kpi.thost = KPIHelper.thost
                    kpi.client = KPIHelper.client
                    KPIHelper.extracted_kpis[apigroups[2]] = kpi
                    KPIHelper.currentkpi = kpi
                # kpi.message = line


        # if kpi and apicodeinfo is not None and apicodeinfo.groups() and apicodeinfo.groups()[0] > starttime:
        elif apicodeinfo is not None:
            apicodeinfogroups = apicodeinfo.groups()
            if apicodeinfogroups and datetime.datetime.strptime(apicodeinfogroups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ') > starttime:
                # print line
                if KPIHelper.extracted_kpis.has_key(apicodeinfogroups[2]):
                    kpi = KPIHelper.extracted_kpis[apicodeinfogroups[2]]
                    kpi.set_apicode(apicodeinfogroups)
                    kpi.thost = KPIHelper.thost
                    kpi.client = KPIHelper.client

                    print "Set KPI {0} {1} {2} {3} {4} {5} {6}".format(kpi.name,
                                                                   kpi.apimethod,
                                                                   kpi.apicode,
                                                                   kpi.result,
                                                                   kpi.start_time,
                                                                   kpi.end_time,
                                                                   kpi.thost)

                    KPIHelper.extracted_kpis[apicodeinfogroups[2]] = deepcopy(kpi)
                    KPIHelper.currentkpi = kpi

                    if not re.match(r"(5\d{2})$", str(kpi.apicode)) or not re.match(r"/(namedobjects|manifest|object|batch)", str(kpi.name)):
                        kpi.write_to_elasticsearch()
                        KPIHelper.currentkpi = None

        elif clientinfo is not None:
            clientinfogroups = clientinfo.groups()
            if clientinfogroups and datetime.datetime.strptime(clientinfogroups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ') > starttime:
                # print line
                kpi = KPI(testcase=KPIHelper.testcase, category="Windows",
                          start_time=datetime.datetime.strptime(clientinfogroups[0], '%d%b%Y %H:%M:%S').strftime(
                              '%Y-%m-%dT%H:%M:%SZ'),
                          name=clientinfogroups[3], result="SUCCESS", message=line, hostname=KPIHelper.hostname,
                          ip=KPIHelper.ip, client=KPIHelper.client, env=KPIHelper.env)

                KPIHelper.extracted_kpis[clientinfogroups[3]] = kpi

                # kpi.write_to_elasticsearch()

        elif backupresult is not None:
            backupresultgroups = backupresult.groups()
            if backupresultgroups and datetime.datetime.strptime(backupresultgroups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ') > starttime:
                # print line
                if KPIHelper.extracted_kpis.has_key(backupresultgroups[3]):
                    kpi = KPIHelper.extracted_kpis[backupresultgroups[3]]
                    kpi.set_backupstatus(backupresultgroups)

                    KPIHelper.extracted_kpis[backupresultgroups[3]] = deepcopy(kpi)


                    # kpi.write_to_elasticsearch()

        elif restoreresult is not None:
            restoreresultgroups = restoreresult.groups()
            if restoreresultgroups and datetime.datetime.strptime(restoreresultgroups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')> starttime:
                # print line
                if KPIHelper.extracted_kpis.has_key(restoreresultgroups[2].lower()):
                    kpi = KPIHelper.extracted_kpis[restoreresultgroups[2].lower()]
                    kpi.set_restorestatus(restoreresultgroups)

                    KPIHelper.extracted_kpis[restoreresultgroups[2].lower()] = deepcopy(kpi)

                    kpi.thost = KPIHelper.thost
                    kpi.client = KPIHelper.client
                    kpi.write_to_elasticsearch()

        elif hostinfo is not None:
            KPIHelper.thost = hostinfo.groups()[0]
        elif testclientinfo is not None:
            KPIHelper.client = testclientinfo.groups()[0]

        elif KPIHelper.currentkpi and KPIHelper.currentkpi.apicode and extenderrorinfo is not None:
            KPIHelper.currentkpi.exterrorcode = extenderrorinfo.groups()[0]
            KPIHelper.currentkpi.write_to_elasticsearch(False)
            KPIHelper.currentkpi = None

        elif clienterrorinfo is not None:
            clienterrorgroups = clienterrorinfo.groups()
            if clienterrorgroups and datetime.datetime.strptime(clienterrorgroups[0], '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ') > starttime:
                # print line
                kpi = KPI(testcase=KPIHelper.testcase, category="Windows",
                          start_time=datetime.datetime.strptime(clienterrorgroups[0], '%d%b%Y %H:%M:%S').strftime(
                              '%Y-%m-%dT%H:%M:%SZ'),
                          name="backup", result="Fail", message=clienterrorgroups[2], hostname=KPIHelper.hostname,
                          ip=KPIHelper.ip, client=KPIHelper.client, env=KPIHelper.env)

                kpi.write_to_elasticsearch()
                kpi = None

                # kpi.write_to_elasticsearch()
        else:
            # print "No Valid KPI."
            pass
        # if kpi and kpi.result:
        #     kpi = None
        return kpi

    @staticmethod
    def get_windows_backup_status(kpi, line):
        """
        line = "26Sep2017 09:39:46 mozyprobackup.exe: Finished backup with code: 0xfffffff7 0 1 1"
        result:
                26Sep2017 09:39:46
                mozyprobackup.exe
                Finished backup
                backup
                0xfffffff7
        """
        clientresultpattern = re.compile(
            "^(.*)\s(.*\.exe).*\s+(Finished (backup|restore)).*:\s(0x.*)(\s\d){3}$",
            re.IGNORECASE)
        clientresult = re.match(clientresultpattern, line)
        if clientresult is not None and clientresult.groups():
            print line
            groups = clientresult.groups()
            kpi.set_backupstatus(groups)

        return kpi

    @staticmethod
    def get_windows_restore_status(kpi, line):
        """
        line = "25Sep2017 10:37:52 mozyprobackup.exe: Restore completed."
        result:
                26Sep2017 09:39:46
                mozyprobackup.exe
                Finished backup
                backup
                0xfffffff7
        """
        clientresultpattern = re.compile(
            "^(.*)\s(.*\.exe).*\s+(Restore (complete))", re.IGNORECASE)
        clientresult = re.match(clientresultpattern, line)
        if clientresult is not None and clientresult.groups():
            print line
            groups = clientresult.groups()
            kpi.set_restorestatus(groups)

        return kpi

    @staticmethod
    def get_linux_kpi(kpi, line, starttime):
        if kpi:
            KPIHelper.currentkpi = kpi
            print "Initial KPI {0} {1} {2} {3} {4}".format(kpi.name, kpi.apimethod, kpi.apicode, kpi.start_time, kpi.end_time)
        """
        line = "2017-09-25T21:35:31.785582 17584676 DEBUG 26312 0x7fd7140043f0 mordor:http:client client.cpp:476 7-1 PUT /namedObjects/9479567/%2Flinux%2Fbackup%2Flin-int%2Flin-int_testdata_0.dat?type=baseline HTTP/1.1"
        result:
                2017-09-25T21:35:31
                7-1
                PUT
                /namedObjects/9479567/%2Flinux%2Fbackup%2Flin-int%2Flin-int_testdata_0.dat?type=baseline
        """
        apipattern = re.compile("^(.*\.\d{6})\s.*\s(\d+\-\d+)\s(GET|HEAD|PUT|DELETE|POST)\s+(.*)\s+HTTP/1.1$", re.IGNORECASE)
        """
        line = "2017-09-25T23:21:40.185991 534263 DEBUG 30042 0x7fa9c00014d0 mordor:http:client client.cpp:485 16-11 HTTP/1.1 200 OK"
        result:
                2017-09-25T23:21:40
                185991
                16-11
                200
                OK
        """
        apicodepattern = re.compile("^(.*\.(\d{6})).*\s(\d+\-\d+)\sHTTP/1.1\s(\d+)\s(.*)$", re.IGNORECASE)
        clientpattern = re.compile("^(.*\.\d{6})\s.*\s+Executing : (.*)", re.IGNORECASE)
        hostpattern = re.compile("^host:\s(.*.com)", re.IGNORECASE)
        testclientpattern = re.compile("^User-Agent: (.*)", re.IGNORECASE)
        """
        X-Extended-Error-Code: 507
        """
        apiextenderrorpattern = re.compile("^X-Extended-Error-Code: (\d+)", re.IGNORECASE)
        """
        2017-11-23T21:52:37.706284 7843289 ERROR 15301 0x368db70 msync:main linuxclient.cpp:241 Backup is stopped because of account error: Invalid credentials.  Re-enter your account information.
It may be necessary to use the "activate" command to resolve the issue
        """
        clienterrorpattern = re.compile("^(.*\.\d{6})\s.*(ERROR).*Backup is stopped because of account error:(.*)", re.IGNORECASE)

        apiinfo = re.match(apipattern, line)
        apicodeinfo = re.match(apicodepattern, line)
        clientinfo = re.match(clientpattern, line)
        hostinfo = re.match(hostpattern, line)
        testclientinfo = re.match(testclientpattern, line)
        clienterrorinfo = re.match(clienterrorpattern, line)
        extenderrorinfo = re.match(apiextenderrorpattern, line)    # API response with extend error code for easier analyse


        # if apiinfo is not None and apiinfo.groups() and apiinfo.groups()[0] > starttime:
        if apiinfo is not None:
            apigroups = apiinfo.groups()
            if apigroups and apigroups[0] > starttime:
                name = apigroups[3].split("?")[0]
                kpi = KPI(testcase=KPIHelper.testcase, category="Service",
                          start_time=apigroups[0], apimethod=apigroups[2], name=name, message=line,
                          hostname=KPIHelper.hostname, ip=KPIHelper.ip, client=KPIHelper.client, env=KPIHelper.env)

                if "log_transfer?arch=" in apigroups[3]:
                    match_result = re.match(r"^.*(data_transfered_rate_avg)=(\d+)\&.*(duration)=(\d+)\&.*(type)=(\d+)\&.*", apigroups[3])
                    """
                    data_transfered_rate_avg
                    1074866
                    duration
                    112
                    type
                    4
                    """
                    if KPIHelper.extracted_kpis.has_key(apigroups[1]) and KPIHelper.extracted_kpis[apigroups[1]].apicode is None:
                        KPIHelper.extracted_kpis[apigroups[1]].end_time = None
                        KPIHelper.extracted_kpis[apigroups[1]].result = "TIMEOUT"
                        KPIHelper.extracted_kpis[apigroups[1]].write_to_elasticsearch()
                        # Remove the key as this means API timeout without response.
                        KPIHelper.extracted_kpis.pop(apigroups[1], None)
                    if match_result:
                        if int(match_result.groups()[5]) == 1:
                            # Backup throughput and duration
                            if KPIHelper.extracted_kpis.has_key("start") and round(int(match_result.groups()[1]) / 1000 / 8) > 0:
                                KPIHelper.extracted_kpis["start"].throughput = round(int(match_result.groups()[1]) / 1000 / 8)  # kilo byte per sec
                                KPIHelper.extracted_kpis["start"].duration = int(match_result.groups()[3])
                                KPIHelper.extracted_kpis["start"].end_time = apigroups[0]
                                KPIHelper.extracted_kpis["start"].message = line
                                KPIHelper.extracted_kpis["start"].thost = KPIHelper.thost
                                KPIHelper.extracted_kpis["start"].client = KPIHelper.client
                                """
                                Known client issue, restore status is sent in next backup. Skip this log transfer.
                                """
                                KPIHelper.extracted_kpis["start"].write_to_elasticsearch()
                        elif int(match_result.groups()[5]) == 4:
                            # Restore throughput and duration
                            if KPIHelper.extracted_kpis.has_key("restore") and round(int(match_result.groups()[1]) / 1000 / 8) > 0:
                                KPIHelper.extracted_kpis["restore"].throughput = round(int(match_result.groups()[1]) / 1000 / 8)  # kilo byte per sec
                                KPIHelper.extracted_kpis["restore"].duration = int(match_result.groups()[3])
                                KPIHelper.extracted_kpis["restore"].end_time = apigroups[0]
                                KPIHelper.extracted_kpis["restore"].message = line
                                KPIHelper.extracted_kpis["restore"].thost = KPIHelper.thost
                                KPIHelper.extracted_kpis["restore"].client = KPIHelper.client
                                """
                                From log, Linux can't distinguish MZD restore and Archive restore.
                                """
                                KPIHelper.extracted_kpis["restore"].write_to_elasticsearch()

                else:
                    kpi.thost = KPIHelper.thost
                    kpi.client = KPIHelper.client
                    KPIHelper.extracted_kpis[apigroups[1]] = kpi
                    KPIHelper.currentkpi = kpi
                    # kpi.write_to_elasticsearch()

        # if kpi and apicodeinfo is not None and apicodeinfo.groups() and apicodeinfo.groups()[0] > starttime:
        elif apicodeinfo is not None:
            apicodeinfogroups = apicodeinfo.groups()
            if apicodeinfogroups and apicodeinfogroups[0] > starttime:
                # print line
                if KPIHelper.extracted_kpis.has_key(apicodeinfogroups[2]):
                    kpi = KPIHelper.extracted_kpis[apicodeinfogroups[2]]
                    kpi.set_apicode(apicodeinfogroups)
                    kpi.thost = KPIHelper.thost
                    kpi.client = KPIHelper.client

                    # print "Set Linux KPI {0} {1} {2} {3} {4} {5}".format(kpi.name,
                    #                                                kpi.apimethod,
                    #                                                kpi.apicode,
                    #                                                kpi.result,
                    #                                                kpi.start_time,
                    #                                                kpi.end_time)

                    KPIHelper.extracted_kpis[apicodeinfogroups[2]] = deepcopy(kpi)
                    KPIHelper.currentkpi = kpi

                    if not re.match(r"(5\d{2})$", str(kpi.apicode)):
                        kpi.write_to_elasticsearch()
                        KPIHelper.currentkpi = None

        # if clientinfo is not None and clientinfo.groups() and clientinfo.groups()[0] > starttime:
        elif clientinfo is not None:
            clientinfogroups = clientinfo.groups()
            if clientinfogroups and clientinfogroups[0] > starttime:
                # print line
                name = clientinfogroups[1]
                if "DOWNLOAD --PATH" in name.upper():
                    name = "restore"
                kpi = KPI(testcase=KPIHelper.testcase, category="Linux",
                          start_time=clientinfogroups[0], name=name, result="SUCCESS", message=line,
                          hostname=KPIHelper.hostname, ip=KPIHelper.ip, env=KPIHelper.env)


                if name.upper() == "START":
                    # Don't send to ES until throughput is generated.
                    KPIHelper.extracted_kpis["start"] = kpi
                elif name.upper() == "RESTORE":
                    # --path for inclient restore, --mzd for mzd download
                    KPIHelper.extracted_kpis["restore"] = kpi
                else:
                    KPIHelper.extracted_kpis[clientinfogroups[1]] = kpi
                    KPIHelper.extracted_kpis[clientinfogroups[1]].thost = KPIHelper.thost
                    KPIHelper.extracted_kpis[clientinfogroups[1]].client = KPIHelper.client

                    kpi.write_to_elasticsearch()
                    # kpi = None


        elif hostinfo is not None:
            KPIHelper.thost = hostinfo.groups()[0]
        elif testclientinfo is not None:
            KPIHelper.client = testclientinfo.groups()[0]

        elif KPIHelper.currentkpi and KPIHelper.currentkpi.apicode and extenderrorinfo is not None:
            KPIHelper.currentkpi.exterrorcode = extenderrorinfo.groups()[0]
            KPIHelper.currentkpi.write_to_elasticsearch(False)
            KPIHelper.currentkpi = None

        elif clienterrorinfo is not None:
            clienterrorgroups = clienterrorinfo.groups()
            if clienterrorgroups and clienterrorgroups[0] > starttime:
                # print line

                kpi = KPI(testcase=KPIHelper.testcase, category="Linux", start_time=clienterrorgroups[0],
                          name="start", result="Fail", message=clienterrorgroups[2], hostname=KPIHelper.hostname,

                          ip=KPIHelper.ip, client=KPIHelper.client, env=KPIHelper.env)

                kpi.write_to_elasticsearch()
                kpi = None

        else:
            pass
            # print "No Valid KPI."
        # if kpi and kpi.result:
        #     kpi = None
        return kpi

    @staticmethod
    def get_kpis(file, starttime=0):
        """
        Get service KPIs
        :param file: Mozy backup log
        :param starttime: Only analyse latest log
        :return: Key Service KPI.  e.g.["/client/sync": response time, "/batch": response time]
        """
        kpi = None

        with open(file, "r") as f:
            for line_no, line in enumerate(f.readlines()):
                if PlatformHelper.is_win():
                    KPIHelper.get_windows_kpi(kpi, line, starttime)  #datetime.datetime.strptime(starttime, '%d%b%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ'))

                elif PlatformHelper.is_Linux():
                    KPIHelper.get_linux_kpi(kpi, line.strip(), starttime)

                elif PlatformHelper.is_mac():
                    KPIHelper.get_mac_kpis(file, line.strip())

    @staticmethod
    def log_error(category="Web", kpiname="Unknown", result="Fail", message=None):
        kpi = KPI(category=category, name=kpiname, result=result, message=message, hostname=KPIHelper.hostname,
                          ip=KPIHelper.ip, client=KPIHelper.client, env=KPIHelper.env)
        kpi.write_to_elasticsearch()


if __name__ == '__main__':
    # file = "C:\Program Files\MozyPro\Data\mozypro.log"
    # starttime = "2017-10-20T16:58:20"
    file = "C:\Program Files\MozyPro\Data\mozy.log"
    starttime = "2017-10-20T22:21:40"
    KPIHelper.extract_kpi(file, starttime)
