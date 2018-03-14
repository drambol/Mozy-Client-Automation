#!/usr/bin/python
# coding: utf-8
"""
#
# https://confluence.dpc.lab.emc.com/display/MC/Kalypso+Error+Codes
# {
#     0x00000000     None    TRITON_ERROR_NONE    No error
#     0x00000001     ServerError0    TRITON_ERROR_INVALID_COMMAND    Backend server error
#     0x00000002     AccountError0    TRITON_ERROR_USER_EXISTS    User account already exists
#     0x00000003     AccountError1    TRITON_ERROR_USER_UNKNOWN    Invalid username and/or password
#     0x00000004     AccountError2    TRITON_ERROR_AUTH_FAILED    Invalid username and/or password
#     0x00000005     ServerError1    TRITON_ERROR_INVALID_MANIFEST    Backend server error
#     0x00000006     ServerError2    TRITON_ERROR_PROTOCOL    Backend server error
#     0x00000007     ServerError3    TRITON_ERROR_NOT_EXIST    Requested file not found
#     0x00000008     ServerError4    TRITON_ERROR_NUM_BLOCKS    Backend server error
#     0x00000009     ServerError5    TRITON_ERROR_STORE_FAILED    Backend server error
#     0x0000000a     AccountError3    TRITON_ERROR_QUOTA_EXCEEDED    Backup size exceeds quota
#     0x0000000b     ServerError6    TRITON_ERROR_LOCK_FAILED    User account in use
#     0x0000000c     ServerError7    TRITON_ERROR_DELETE_FAILED    Backend server error
#     0x0000000d     AccountError4    TRITON_ERROR_MACHINE_UNKNOWN    Machine not recognized
#     0x0000000e     ServerError8    TRITON_ERROR_BAD_PATCH    Invalid file patch
#     0x0000000f     UpdateRequired0    TRITON_ERROR_OLD_CLIENT    Client update required
#     0x00000010     ServerError16    TRITON_ERROR_INVALID_STATE    Backend server error
#     0x00000011     ServerError17    TRITON_ERROR_GO_AWAY    Server busy
#     0x00000012     EncryptionError5    TRITON_ERROR_ENCRYPT_NOT_SET    Encryption not set
#     0x00000013     ServerError19    TRITON_ERROR_INCORRECT_SITE    Backend server error
#     0x00000014     AccountError10    TRITON_ERROR_ACCOUNT_INACTIVE    Your account has expired
#     0x00000015     ServerError20    TRITON_ERROR_REPLICATION_FAILED    Backend server error
#     0x00000016     ServerError17    TRITON_ERROR_ACCOUNT_DATA_UNAVAIL    Server busy
#     0x00000017     ServerError17    TRITON_ERROR_STORAGE_SYSTEM_UNAVAIL    Server busy
#     0x00000018     ServerError17    TRITON_ERROR_CONTAINER_DATA_UNAVAIL    Server busy
#     0x00000019     ServerError17    TRITON_ERROR_AUTHENTICIATE_SERVICE_UNAVAIL    Server busy
#     0x00000064     ServerError16    TRITON_ERROR_NOT_MDB_MACHINE    Backend server error
#     0x00000065     ServerError2    TRITON_ERROR_BAD_LIST_PARAMS    Backend server error
#     0x00000066     ServerError16    TRITON_ERROR_CANT_CRYPT    Backend server error
#     0x00000067     ServerError2    TRITON_ERROR_INVALID_METADATA    Backend server error
#     0x00000068     ServerError2    TRITON_ERROR_NEED_PREVIOUS_OBJECTID    Backend server error
#     0x00000069     ServerError2    TRITON_ERROR_OBJECTID_MISMATCH    Backend server error
#     0x0000006a     ServerError8    TRITON_ERROR_INVALID_PATCH_HEADERS    Invalid file patch
#     0x0000006b     ServerError2    TRITON_ERROR_HASH_VERIFICATION_FAILED    Backend server error
#     0x0000006c     ServerError16    TRITON_ERROR_UPDATE_CONFLICT    Backend server error
#     0x0000006d     ServerError17    TRITON_ERROR_INVALID_CONTAINER    Server busy
#     0x0000006e     ServerError2    TRITON_ERROR_RESUMABLE_TOKEN_EXPIRED    Backend server error
#
#     0x80000000     ConnectionError0    TRITON_ERROR_CONNECTION_FAILED    Unable to connect to %1 servers
#     0x80000001     ConnectionError1    TRITON_ERROR_CONNECT_FAILED    Unable to connect to %1 servers
#     0x80000002     ConnectionError2    TRITON_ERROR_SEND_FAILED    Connection lost
#     0x80000003     ConnectionError3    TRITON_ERROR_RECV_FAILED    Connection lost
#     0x80000004     ConnectionError4    TRITON_ERROR_SENDFILE_FAILED    Connection lost
#     0x80000005     ConnectionError5    TRITON_ERROR_RECVRESULT_FAILED    Connection lost
#     0x80000006     MaintenanceError0    TRITON_ERROR_MAINTENANCE    Servers are unavailable due to maintenance
#     0x80000016     ConnectionError6    TRITON_ERROR_HTTPS_PROXY_FAILED    Unable to negotiate proxy connection
#     0x80000007     ConnectionError7    TRITON_ERROR_NO_INTERNET    No Internet access detected
#     0x80000008     ConnectionError8    TRITON_ERROR_CONNECT_TIMEOUT    Connection to %1 timed out
#     0x80000009     ConnectionError9    TRITON_ERROR_HOST_CONNECT_FAILED    Unable to connect to %1 servers
#     0x8000000a     ServerError11    TRITON_ERROR_REQUEST_TIMEOUT    Backend server error
#     0x8000000f     AccountError5    TRITON_ERROR_MACHINE_CREATE_FAILED    Unable to create machine account
#     0x80000010     InvalidKeyError0    TRITON_ERROR_INVALID_PRODUCT_KEY    Invalid product key
#     0x80000011     ServerError9    TRITON_ERROR_DATABASE_ERROR    Backend server error
#     0x80000012     ServerError10    TRITON_ERROR_MACHINE_TRANSFER_FAILED    Backend server error
#     0x80000013     AccountError6    TRITON_ERROR_USER_UNDER_WRONG_ADMIN    Can not create %1 account
#     0x80000014     ActivationError0    TRITON_ERROR_INVALID_DOMAIN    Unrecognized %1 corporate domain
#     0x80000015     ActivationError1    TRITON_ERROR_KEYS_EXHAUSTED    No available license keys
#     0x80000017     ActivationError2    TRITON_ERROR_KEY_IN_USE    License key already activated
#     0x80000018     EncryptionError6    TRITON_ERROR_MISMATCHED_KEY    Incorrect encryption key
#     0x80000019     AccountError7    TRITON_ERROR_PASSWORD_NOT_COMPLEX_ENOUGH    Password does not meet complexity requirements
#     0x8000001a     AccountError8    TRITON_ERROR_PASSWORD_CHANGE_REQUIRED    Password change required
#     0x8000001b     AccountError9    TRITON_ERROR_INVALID_REGION    Unrecognized region
#     0x8000001c     AuthenticationError0    TRITON_ERROR_TOO_MANY_AUTH_FAILURES    Account locked out
#     0x8000001e     ActivationError3    TRITON_ERROR_WRONG_CLIENT    Using incorrect product to activate
#
#     0xf0000001     LogRotationError0    HANDLER_ERROR_EMPTY_LOG_PATH    Unable to update log
#     0xf0000002     LogRotationError1    HANDLER_ERROR_AVAILABLE_LOG    Unable to update log
#     0xf0000003     LogRotationError2    HANDLER_ERROR_DRIVER    Unable to update log
#     0xf0000004     LogRotationError3    HANDLER_ERROR_OPEN_FILE    Unable to update log
#     0xf0000005     LogRotationError4    HANDLER_ERROR_BLIND    Unable to update log
#     0xf0000006     LogRotationError5    HANDLER_ERROR_BADLINE    Unable to update log
#     0xf0000007     LogRotationError6    HANDLER_ERROR_OVERLOAD    Unable to update log
#     0xf0000008     LogRotationError7    HANDLER_ERROR_DB    Unable to update log
#
#     0xff000000     ClientError6    KALYPSO_ERROR_NOT_CONFIGURED    has not been set up
#     0xff000001     ClientError7    KALYPSO_ERROR_NO_SERVICE    service not set up correctly
#     0xff000002     ClientError8    KALYPSO_ERROR_NO_AUTOLOGIN    Autologin not set
#     0xff000003     ClientError9    KALYPSO_ERROR_SERVICE_NOT_STARTED    service not started
#     0xff000004     DBError3    KALYPSO_ERROR_CACHEDB_LOCKED    Unable to update backup set cache.
#     0xff000005     DBError4    KALYPSO_ERROR_STATEDB_LOCKED    Unable to update file state cache.
#     0xff000006     LocalBackupError0    KALYPSO_ERROR_LOCALDISK_MISSING_AT_START    Local backup drive is missing
#     0xff000007     LocalBackupError1    KALYPSO_ERROR_LOCALDISK_UNAVAILABLE    Local backup drive not available
#     0xff000008     LocalBackupError2    KALYPSO_ERROR_LOCALDISK_ERROR    Local backup drive disk error
#     0xff000009     LocalBackupError4    KALYPSO_ERROR_LOCALHISTORY_FULL    Version history is full. Contact your administrator to allocate more space to your version history.
#     0xff000010     ExtDrive404    KALYPSO_ERROR_EXTERNAL_DRIVE_UNAVAILABLE    External drive is unavailable
#     0xff000014     EncryptionWarning0    KALYPSO_ERROR_ENCRYPTION_TYPE_WARNING    Current encryption type is no longer allowed.
#
#
#     0xffffff01     ClientError0    TRITON_ERROR_CALCULATE    Unable to prepare server message
#     0xffffff02     ClientError1    TRITON_ERROR_MEMORY    Out of memory
#     0xffffff03     ClientError2    TRITON_ERROR_INVALID_RESPONSE    Bad message from %1 servers
#     0xffffff04     ClientError3    TRITON_ERROR_UNKNOWN    Unknown error
#
#     0xffffffa0     DBError6    KALYPSO_ERROR_LOCAL_BACKUP_DB    Local backup database error
#     0xffffffa8     DBWarning0    KALYPSO_WARNING_RECREATE_STATEDB    Repaired Database. Backup was successful
#
#
#     0xffffffb0     AuthenticationError1    KALYPSO_ERROR_NOT_NETWORK_CRED    Authentication using network credentials is not enabled
#     0xffffffb1     AuthenticationError2    KALYPSO_ERROR_UNKNOWN_SUBDOMAIN    Invalid Subdomain
#     0xffffffb2     AuthenticationError3    KALYPSO_ERROR_INVALID_SAML    Invalid user
#     0xffffffb3     AuthenticationError4    KALYPSO_ERROR_TOKEN_AUTH_FAILURE    Access token has expired
#     0xffffffb5     AuthenticationError5    KALYPSO_ERROR_WEB_AUTH_FAILURE    Web Authentication failed
#     0xffffffb6     AuthenticationError6    KALYPSO_ERROR_AUTH_UNEXPECTED_RESPONSE    Unexpected response from Authentication Server
#
#     0xffffffca     ClientError16    KALYPSO_ERROR_NO_FILES_CHOSEN    No files have been selected for backup. Open Settings to select files for backup.
#     0xffffffcb     ConnectionError11    KALYPSO_ERROR_RESUME_FAILED    Unable to resume send for file
#     0xffffffcc     DataSeedingError6    KALYPSO_ERROR_NO_SEED_ORDER    Data Shuttle not enabled for this account
#     0xffffffcd     ConnectionError10    KALYPSO_ERROR_NETWORK_RESTRICTED    Restricted network list preventing backup
#     0xffffffce     SeedDeviceFull    KALYPSO_ERROR_SEED_DEVICE_FULL    Data Shuttle Device Full
#     0xffffffcf     MobileRestriction2    KALYPSO_ERROR_MOBILE_BACKUP_TOO_LARGE    Backup exceeds size limit for mobile network
#
#
#     0xffffffd0     MobileRestriction1    KALYPSO_ERROR_MOBILE_BACKUP_RESTRICTED    Mobile rule preventing backup
#     0xffffffd2     EncryptionError8    KALYPSO_ERROR_PERSONAL_KEY_MISSING    Encryption key missing
#     0xffffffd3     DataSeedingError5    KALYPSO_ERROR_SEED_DEVICE_PREP_FAILED    Failed to prepare device for data transfer
#     0xffffffd4     DataSeedingError2    KALYPSO_ERROR_SEED_DEVICE_NOT_FOUND    Data Shuttle device not found
#     0xffffffd5     NetworkShareError1    KALYPSO_ERROR_CONNECT_SHARE_FAILED    Failed to connect network share
#     0xffffffd6     DataSeedingError1    KALYPSO_ERROR_INVALID_SEED_STATE    Data Shuttle state mismatch
#     0xffffffd7     DataSeedingError4    KALYPSO_ERROR_INVALID_SEED_DEVICE    Data Shuttle device not registered to this machine
#     0xffffffd8     DataSeedingError3    KALYPSO_ERROR_BAD_CRYPTO_DATASEED    Invalid encryption for Data Shuttle
#     0xffffffda     FilesystemError4    KALYPSO_ERROR_IO    I/O Error
#     0xffffffdb     FilesystemError3    KALYPSO_ERROR_DISK_FULL    Disk full
#     0xffffffdc     RebootRequired1    KALYPSO_ERROR_REBOOT_REQUIRED    Reboot Required
#     0xffffffdd     SnapshotError5    KALYPSO_ERROR_VSS_RESTORE_FAILED    VSS Restore Failed
#     0xffffffde     SnapshotError4    KALYPSO_ERROR_VSS_WRITER    VSS Writer Error
#     0xffffffdf     LicenseError1    KALYPSO_ERROR_NO_SERVER_SUPPORT    Product license does not allow Windows Server
#
#     0xffffffe0     FilterError0    KALYPSO_ERROR_FILTER_DRIVER_NOT_RUNNING    change monitor is not running
#     0xffffffe1     FilesystemError1    KALYPSO_ERROR_EFS_NOT_SUPPORTED    EFS Encrypted File
#     0xffffffe2     CancelError1    KALYPSO_ERROR_SERVICE_STOPPING    The %1 Backup service was stopped
#     0xffffffe3     CancelError2    KALYPSO_ERROR_SYSTEM_SUSPEND    The computer was suspended
#     0xffffffe4     CancelError3    KALYPSO_ERROR_SYSTEM_SHUTDOWN    The computer was shut down
#     0xffffffe5     SnapshotError2    KALYPSO_ERROR_SNAPSHOT_DISABLED_NO_NTFS    No NTFS volume for open file support
#     0xffffffe6     SnapshotError3    KALYPSO_ERROR_SNAPSHOT_DISABLED_WIN2K    Open files not supported on Windows 2000
#     0xffffffe7     ClientError14    KALYPSO_ERROR_NO_BACKUP_PRIVILEGES    No backup privileges
#     0xffffffe8     ClientError13    KALYPSO_ERROR_UPDATE_DOWNLOAD_FAILED    Unable to download latest client version
#     0xffffffe9     EncryptionError4    KALYPSO_ERROR_FAILED_CRYPTO    Unable to generate a random password
#     0xffffffea     DBError5    KALYPSO_ERROR_BAD_MANIFEST    Corrupted manifest
#     0xffffffeb     DBError2    KALYPSO_ERROR_BAD_CONFIGDB    Corrupted configuration
#     0xffffffec     Error1    KALYPSO_ERROR_INVALID_CORP_CONFIG    Invalid %1 configuration downloaded
#     0xffffffed     EncryptionError7    KALYPSO_ERROR_FETCH_ENCRYPTION_KEY_FAILED    Unable to fetch private encryption key
#     0xffffffee     ReferrerFraud0    KALYPSO_ERROR_REFERER_FRAUD    Duplicate referral machine detected
#     0xffffffef     ClientError5    KALYPSO_ERROR_NOT_IMPLEMENTED    Unknown error
#
#     0xfffffff0     FilesystemError2    KALYPSO_ERROR_FILE_OPEN_FAILED    Unable to open a file for backup
#     0xfffffff1     SnapshotError1    KALYPSO_ERROR_SNAPSHOT_DISABLED    Open file support is disabled
#     0xfffffff2     ClientError12    KALYPSO_ERROR_BAD_EMAIL_ADDRESS    Invalid email address
#     0xfffffff3     ClientError11    KALYPSO_ERROR_LOST_TEMP_FILE    Unable to open prepared file
#     0xfffffff4     EncryptionError3    KALYPSO_ERROR_INSECURE_SSL    Insecure connection to %1 servers
#     0xfffffff5     SnapshotError0    KALYPSO_ERROR_SNAPSHOT_FAILED    Unable to snapshot drive
#     0xfffffff6     FilesystemError0    KALYPSO_ERROR_FILTER    Unable to determine changes
#     0xfffffff7     CancelError0    KALYPSO_ERROR_CANCELED    Paused by user
#     0xfffffff8     EncryptionError0    KALYPSO_ERROR_BAD_CRYPTO    Encryption settings do not match
#     0xfffffff9     ClientError4    KALYPSO_ERROR_PREPARE_FAILED    Unable to prepare files for backup
#     0xfffffffa     EncryptionError1    KALYPSO_ERROR_SET_ENCRYPTION    Unable to set encryption preference
#     0xfffffffb     EncryptionError2    KALYPSO_ERROR_GET_ENCRYPTION    Unable to determine encryption preference
#     0xfffffffc     DBError0    KALYPSO_ERROR_BAD_CACHEDB    Corrupted backup set cache
#     0xfffffffd     DBError1    KALYPSO_ERROR_BAD_STATEDB    Corrupted file state cache
#     0xfffffffe     ServerError12    TRITON_ERROR_UNEXPECTED    Backend server error
#     0xffffffff     ServerError11    TRITON_ERROR_TDN_TIMEOUT    Backend server error
#
#     0xfff00001     RestoreError0    RESTORE_ERROR_WRITE_FAILED    Unable to write to file
#     0xfff00002     RestoreError1    RESTORE_ERROR_DIRECTORY    Unable to create directory
#     0xfff00003     RestoreError2    RESTORE_ERROR_SAVE_FAILED    Unable to save file
#     0xfff00004     RestoreError3    RESTORE_ERROR_FILES_SKIPPED    File(s) temporarily unavailable
#     0xfff0000a     RestoreError4    RESTORE_MANAGER_DONE_WITH_ERRORS    Restore Manager error
#     0xfff00005     RestoreError5    RESTORE_MANAGER_ERROR_DISK_MISSING    Disk Missing
#     0xfff0000b     RestoreError6    RESTORE_MANAGER_ERROR_EXPANDER_PARSE    Parsing error during expansion
#     0xfff00006     RestoreError7    RESTORE_MANAGER_ERROR_PATH_TOO_LONG    Path too long
#     0xfff00007     RestoreError8    RESTORE_MANAGER_ERROR_ACCESS_DENIED    Access denied
#     0xfff00008     RestoreError9    RESTORE_MANAGER_ERROR_SSL_ERROR    SSL Error
#     0xfff0000c     RestoreError10    RESTORE_MANAGER_FORK_WITHOUT_PARENT_ERROR    Resource fork was restored without the parent file
#     0xfff0000d     RestoreError11    RESTORE_MANAGER_ERROR_DISK_REQUIREMENTS_NOT_MET    Insufficient disk space
# }
...
"""

class Error_Codes(object):


    def __init__(self):
        pass

    ERROR_CODE = {
    # '0xff000000':'ERROR_SOURCE_MASK',

    '0x00000000':'SUCCESS',
    '0x00000001':'TRITON_ERROR_INVALID_COMMAND',
    '0x00000002':'TRITON_ERROR_USER_EXISTS',  #AccountError0
    '0x00000003':'TRITON_ERROR_USER_UNKNOWN',  #
    '0x00000004':'TRITON_ERROR_AUTH_FAILED',
    '0x00000005':'TRITON_ERROR_INVALID_MANIFEST',
    '0x00000006':'TRITON_ERROR_PROTOCOL',
    '0x00000007':'TRITON_ERROR_NOT_EXIST',
    '0x00000008':'TRITON_ERROR_NUM_BLOCKS',
    '0x00000009':'TRITON_ERROR_STORE_FAILED',
    '0x0000000a':'TRITON_ERROR_QUOTA_EXCEEDED',
    '0x0000000b':'TRITON_ERROR_LOCK_FAILED',
    '0x0000000c':'TRITON_ERROR_DELETE_FAILED',
    '0x0000000d':'TRITON_ERROR_MACHINE_UNKNOWN',
    '0x0000000e':'TRITON_ERROR_BAD_PATCH',
    '0x0000000f':'TRITON_ERROR_OLD_CLIENT',
    '0x00000010':'TRITON_ERROR_INVALID_STATE',
    '0x00000011':'TRITON_ERROR_GO_AWAY',
    '0x00000012':'TRITON_ERROR_ENCRYPT_NOT_SET',
    '0x00000013':'TRITON_ERROR_INCORRECT_SITE',
    '0x00000014':'TRITON_ERROR_ACCOUNT_INACTIVE',
    '0x00000015':'TRITON_ERROR_REPLICATION_FAILED',
    '0x00000016':'TRITON_ERROR_ACCOUNT_DATA_UNAVAIL',
    '0x00000017':'TRITON_ERROR_STORAGE_SYSTEM_UNAVAIL',
    '0x00000018':'TRITON_ERROR_CONTAINER_DATA_UNAVAIL',
    '0x00000019':'TRITON_ERROR_AUTHENTICIATE_SERVICE_UNAVAIL',
    '0x00000064':'TRITON_ERROR_NOT_MDB_MACHINE',
    '0x00000065':'TRITON_ERROR_BAD_LIST_PARAMS',
    '0x00000066':'TRITON_ERROR_CANT_CRYPT',
    '0x00000067':'TRITON_ERROR_INVALID_METADATA',
    '0x00000068':'TRITON_ERROR_NEED_PREVIOUS_OBJECTID',
    '0x00000069':'TRITON_ERROR_OBJECTID_MISMATCH',
    '0x0000006a':'TRITON_ERROR_INVALID_PATCH_HEADERS',
    '0x0000006b':'TRITON_ERROR_HASH_VERIFICATION_FAILED',
    '0x0000006c':'TRITON_ERROR_UPDATE_CONFLICT',
    '0x0000006d':'TRITON_ERROR_INVALID_CONTAINER',
    '0x0000006e':'TRITON_ERROR_RESUMABLE_TOKEN_EXPIRED',

    ## REST-specific errors
    '100':'TRITON_ERROR_NOT_MDB_MACHINE',
    '101':'TRITON_ERROR_BAD_LIST_PARAMS',
    '102':'TRITON_ERROR_CANT_CRYPT',
    '103':'TRITON_ERROR_INVALID_METADATA',
    '104':'TRITON_ERROR_NEED_PREVIOUS_OBJECTID',
    '105':'TRITON_ERROR_OBJECTID_MISMATCH',
    '106':'TRITON_ERROR_INVALID_PATCH_HEADERS',
    '107':'TRITON_ERROR_HASH_VERIFICATION_FAILED',
    '108':'TRITON_ERROR_UPDATE_CONFLICT',
    '109':'TRITON_ERROR_INVALID_CONTAINER',
    '110':'TRITON_ERROR_RESUMABLE_TOKEN_EXPIRED',

    ## ERROR_SOURCE_TRITON = 0x00000000,

    ## errors that denote where the connection failed
    '0x80000000':'TRITON_ERROR_CONNECTION_FAILED',
    '0x80000001':'TRITON_ERROR_CONNECT_FAILED',  ## Deprecated. Replaced with NO_INTERNET, FIREWALL_BLOCK, HOST_CONNECT, and PROXY_CONNECT
    '0x80000002':'TRITON_ERROR_SEND_FAILED',
    '0x80000003':'TRITON_ERROR_RECV_FAILED',
    '0x80000004':'TRITON_ERROR_SENDFILE_FAILED',
    '0x80000005':'TRITON_ERROR_RECVRESULT_FAILED',
    '0x80000006':'TRITON_ERROR_MAINTENANCE',
    '0x80000007':'TRITON_ERROR_NO_INTERNET',
    '0x80000008':'TRITON_ERROR_CONNECT_TIMEOUT',
    '0x80000009':'TRITON_ERROR_HOST_CONNECT_FAILED',
    '0x8000000a':'TRITON_ERROR_REQUEST_TIMEOUT',
    # '0x80000000':'ERROR_SOURCE_CONNECTION',
    ## fake triton error code that makes client handling easier
    '0x8000000f':'TRITON_ERROR_MACHINE_CREATE_FAILED',
    '0x80000010':'TRITON_ERROR_INVALID_LICENSE_KEY',
    '0x80000011':'TRITON_ERROR_DATABASE_ERROR',
    '0x80000012':'TRITON_ERROR_MACHINE_TRANSFER_FAILED',
    '0x80000013':'TRITON_ERROR_USER_UNDER_WRONG_ADMIN',
    '0x80000014':'TRITON_ERROR_INVALID_DOMAIN',
    '0x80000015':'TRITON_ERROR_KEYS_EXHAUSTED',
    '0x80000016':'TRITON_ERROR_HTTPS_PROXY_FAILED',
    '0x80000017':'TRITON_ERROR_KEY_IN_USE',
    '0x80000018':'TRITON_ERROR_MISMATCHED_KEY',
    '0x80000019':'TRITON_ERROR_PASSWORD_NOT_COMPLEX_ENOUGH',
    '0x8000001a':'TRITON_ERROR_PASSWORD_CHANGE_REQUIRED',
    '0x8000001b':'TRITON_ERROR_INVALID_REGION',
    '0x8000001c':'TRITON_ERROR_TOO_MANY_AUTH_FAILURES',
    '0x8000001d':'TRITON_ERROR_PLATFORM_MISMATCH',
    '0x8000001e':'TRITON_ERROR_WRONG_CLIENT',

    ## log handling errors
    '0xf0000001':'HANDLER_ERROR_EMPTY_LOG_PATH',
    '0xf0000002':'HANDLER_ERROR_AVAILABLE_LOG',
    '0xf0000003':'HANDLER_ERROR_DRIVER',
    '0xf0000004':'HANDLER_ERROR_OPEN_FILE',
    '0xf0000005':'HANDLER_ERROR_BLIND',
    '0xf0000006':'HANDLER_ERROR_BADLINE',
    '0xf0000007':'HANDLER_ERROR_OVERLOAD',
    '0xf0000008':'HANDLER_ERROR_DB',

    '0xf0000000':'ERROR_SOURCE_HANDLER',


    ## other generic errors
    '0xff000000': 'KALYPSO_ERROR_NOT_CONFIGURED',
    '0xff000001': 'KALYPSO_ERROR_NO_SERVICE',
    '0xff000002': 'KALYPSO_ERROR_NO_AUTOLOGIN',
    '0xff000003': 'KALYPSO_ERROR_SERVICE_NOT_STARTED',
    '0xff000004': 'KALYPSO_ERROR_CACHEDB_LOCKED',
    '0xff000005': 'KALYPSO_ERROR_STATEDB_LOCKED',
    '0xff000006': 'KALYPSO_ERROR_LOCALDISK_MISSING_AT_START',  ## local backup drive not found
    '0xff000007': 'KALYPSO_ERROR_LOCALDISK_UNAVAILABLE',  ## local backup drive had been found, but not now
    '0xff000008': 'KALYPSO_ERROR_LOCALDISK_ERROR',  ## misc local backup disk error
    '0xff000009': 'KALYPSO_ERROR_LOCALHISTORY_FULL',
    '0xff000010': 'KALYPSO_ERROR_EXTERNAL_DRIVE_UNAVAILABLE',
    '0xff000011': 'KALYPSO_ERROR_PARTNERID_CONFLICT',
    '0xff000012': 'KALYPSO_ERROR_MERGING_CONFIG',
    '0xff000013': 'KALYPSO_ERROR_MERGING_CONFIG_FATAL',
    '0xff000014': 'KALYPSO_ERROR_ENCRYPTION_TYPE_WARNING',

    ## restore errors
    '0xfff00001': 'RESTORE_ERROR_WRITE_FAILED',
    '0xfff00002': 'RESTORE_ERROR_DIRECTORY',
    '0xfff00003': 'RESTORE_ERROR_SAVE_FAILED',
    '0xfff00004': 'RESTORE_ERROR_FILES_SKIPPED',
    '0xfff00005': 'RESTORE_MANAGER_ERROR_DISK_MISSING',
    '0xfff00006': 'RESTORE_MANAGER_ERROR_PATH_TOO_LONG',
    '0xfff00007': 'RESTORE_MANAGER_ERROR_ACCESS_DENIED',
    '0xfff00008': 'RESTORE_MANAGER_ERROR_SSL_ERROR',
    '0xfff0000a': 'RESTORE_MANAGER_DONE_WITH_ERRORS',
    '0xfff0000b': 'RESTORE_MANAGER_ERROR_EXPANDER_PARSE',
    '0xfff0000c': 'RESTORE_MANAGER_FORK_WITHOUT_PARENT_ERROR',
    '0xfff0000d': 'RESTORE_MANAGER_ERROR_DISK_REQUIREMENTS_NOT_MET',
    '0xfff0000e': 'RESTORE_BACKUP_CONFLICTED',

    '0xfff00000':'ERROR_SOURCE_RESTORE',


    ## Reserved Mac OS X error code block: 0xffff0000 - 0xffffefff
    '0xffff0000':'ERROR_SOURCE_MAC',

    ## the following errors are all client side errors
    '0xffffff01': 'TRITON_ERROR_CALCULATE',
    '0xffffff02': 'TRITON_ERROR_MEMORY',
    '0xffffff03': 'TRITON_ERROR_INVALID_RESPONSE',
    '0xffffff04': 'TRITON_ERROR_UNKNOWN',


    '0xffffffa0': 'KALYPSO_ERROR_LOCAL_BACKUP_DB',
    '0xffffffa8': 'KALYPSO_WARNING_RECREATE_STATEDB',

    '0xffffffb0': 'KALYPSO_ERROR_NOT_NETWORK_CRED',
    '0xffffffb1': 'KALYPSO_ERROR_UNKNOWN_SUBDOMAIN',
    '0xffffffb2': 'KALYPSO_ERROR_INVALID_SAML',
    '0xffffffb3': 'KALYPSO_ERROR_TOKEN_AUTH_FAILURE',
    '0xffffffb4': 'KALYPSO_ERROR_INVALID_SAML_TRY_WEBAUTH',
    '0xffffffb5': 'KALYPSO_ERROR_WEB_AUTH_FAILURE',
    '0xffffffb6': 'KALYPSO_ERROR_AUTH_UNEXPECTED_RESPONSE',

    ## these aren't really triton errors, but this is becoming
    ## the place to store errors we can report.

    '0xffffffca': 'KALYPSO_ERROR_NO_FILES_CHOSEN',
    '0xffffffcb':'KALYPSO_ERROR_RESUME_FAILED',
    '0xffffffcc':'KALYPSO_ERROR_NO_SEED_ORDER',
    '0xffffffcd':'KALYPSO_ERROR_NETWORK_RESTRICTED',
    '0xffffffcd':'KALYPSO_ERROR_SEED_DEVICE_FULL',
    '0xffffffcf':'KALYPSO_ERROR_MOBILE_BACKUP_TOO_LARGE',

    '0xffffffd0':'KALYPSO_ERROR_MOBILE_BACKUP_RESTRICTED',
    '0xffffffd1':'KALYPSO_ERROR_RESPONSE_PENDING',
    '0xffffffd2':'KALYPSO_ERROR_PERSONAL_KEY_MISSING',
    '0xffffffd3':'KALYPSO_ERROR_SEED_DEVICE_PREP_FAILED',
    '0xffffffd4':'KALYPSO_ERROR_SEED_DEVICE_NOT_FOUND',
    '0xffffffd5':'KALYPSO_ERROR_CONNECT_SHARE_FAILED',
    '0xffffffd6':'KALYPSO_ERROR_INVALID_SEED_STATE',
    '0xffffffd7':'KALYPSO_ERROR_INVALID_SEED_DEVICE',
    '0xffffffd8':'KALYPSO_ERROR_BAD_CRYPTO_DATASEED',
    '0xffffffd9':'KALYPSO_ERROR_SEED_FROZEN',
    '0xffffffda':'KALYPSO_ERROR_IO',
    '0xffffffdb':'KALYPSO_ERROR_DISK_FULL',
    '0xffffffdc':'KALYPSO_ERROR_REBOOT_REQUIRED',
    '0xffffffdd': 'KALYPSO_ERROR_VSS_RESTORE_FAILED',
    '0xffffffde': 'KALYPSO_ERROR_VSS_WRITER',
    '0xffffffdf':'KALYPSO_ERROR_NO_SERVER_SUPPORT',

    '0xffffffe0':'KALYPSO_ERROR_FILTER_DRIVER_NOT_RUNNING',
    '0xffffffe1': 'KALYPSO_ERROR_EFS_NOT_SUPPORTED',
    '0xffffffe2':'KALYPSO_ERROR_SERVICE_STOPPING',
    '0xffffffe3': 'KALYPSO_ERROR_SYSTEM_SUSPEND',
    '0xffffffe4':'KALYPSO_ERROR_SYSTEM_SHUTDOWN',
    '0xffffffe5':'KALYPSO_ERROR_SNAPSHOT_DISABLED_NO_NTFS',
    '0xffffffe6':'KALYPSO_ERROR_SNAPSHOT_DISABLED_WIN2K',
    '0xffffffe7': 'KALYPSO_ERROR_NO_BACKUP_PRIVILEGES',
    '0xffffffe8': 'KALYPSO_ERROR_UPDATE_DOWNLOAD_FAILED',
    '0xffffffe9':'KALYPSO_ERROR_FAILED_CRYPTO',
    '0xffffffea': 'KALYPSO_ERROR_BAD_MANIFEST',
    '0xffffffeb':'KALYPSO_ERROR_BAD_CONFIGDB',
    '0xffffffec':'KALYPSO_ERROR_INVALID_CORP_CONFIG',
    '0xffffffed':'KALYPSO_ERROR_FETCH_ENCRYPTION_KEY_FAILED',
    ## Dumb triton stole my error numbers (-1 and -2) without telling me,
    ## so I had to change these
    '0xffffffee': 'KALYPSO_ERROR_REFERER_FRAUD',
    '0xffffffef' :'KALYPSO_ERROR_NOT_IMPLEMENTED',

    ## warning 0xffffffe e-f are taken below, don't reuse them here

    '0xfffffff0':'KALYPSO_ERROR_FILE_OPEN_FAILED',
    '0xfffffff1': 'KALYPSO_ERROR_SNAPSHOT_DISABLED',
    '0xfffffff2':'KALYPSO_ERROR_BAD_EMAIL_ADDRESS',
    '0xfffffff3':'KALYPSO_ERROR_LOST_TEMP_FILE',
    '0xfffffff4':'KALYPSO_ERROR_INSECURE_SSL',
    '0xfffffff5' : 'KALYPSO_ERROR_SNAPSHOT_FAILED',
    '0xfffffff6':'KALYPSO_ERROR_FILTER',
    '0xfffffff7': 'KALYPSO_ERROR_CANCELED',
    '0xfffffff8':'KALYPSO_ERROR_BAD_CRYPTO',
    '0xfffffff9':'KALYPSO_ERROR_PREPARE_FAILED',
    '0xfffffffa' : 'KALYPSO_ERROR_SET_ENCRYPTION',
    '0xfffffffb' :'KALYPSO_ERROR_GET_ENCRYPTION',
    '0xfffffffc':'KALYPSO_ERROR_BAD_CACHEDB',
    '0xfffffffd':'KALYPSO_ERROR_BAD_STATEDB',
    '0xfffffffe':'TRITON_ERROR_UNEXPECTED',
    '0xffffffff':'TRITON_ERROR_TDN_TIMEOUT',

    # '0xff000000':'ERROR_SOURCE_CLIENT'
    }

if __name__ == '__main__':
    if Error_Codes.ERROR_CODE.has_key("0xfffffff7"):
        print Error_Codes.ERROR_CODE.get("0xfffffff7")