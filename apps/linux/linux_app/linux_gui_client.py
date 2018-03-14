#!/usr/bin/env python
#
# Copyright (c) DELL EMC, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong


from lib.singleton import Singleton
from apps.linux.linux_app.command import activate, download, start, unlink, state, backupset, account, history, continuous
from apps.linux.linux_app.command import stop, addbackupdirs, removebackupdirs, filecount, lastbackup
from apps.linux.linux_app.command import listbackupdir, clearbackupdirs, account, info, throttle, decrypt

class LinuxGUIClient(object):

    __metaclass__ = Singleton

    activate_cmd = activate.ActivateCmd()
    unlink_cmd = unlink.UnlinkCmd()
    download_cmd = download.DownloadCmd()
    start_cmd = start.StartCmd()
    state_cmd = state.StateCmd()
    backupset_cmd = backupset.BackupsetCmd()
    account_cmd = account.AccountCmd()
    history_cmd =  history.HistoryCmd()
    continuous_cmd = continuous.ContinuousCmd()
    stop_cmd = stop.StopCmd()
    addbackupdirs_cmd = addbackupdirs.AddBackupDirsCmd()
    removebackupdirs_cmd = removebackupdirs.RemovebackupdirsCmd()
    filecount_cmd = filecount.FilecountCmd()
    lastbackup_cmd = lastbackup.LastBackupCmd()
    listbackupdir_cmd = listbackupdir.ListBackupDirsCmd()
    clearbackupdirs_cmd = clearbackupdirs.ClearbackupdirsCmd()
    account_cmd = account.AccountCmd()
    info_cmd = info.InfoCmd()
    throttle_cmd = throttle.ThrottleCmd()
    decrypt_cmd = decrypt.DecryptCmd()



