
"""
{
    0xff000000 => 'ERROR_SOURCE_MASK',

    0x00000000 => 'TRITON_ERROR_NONE',
    0x00000001 => 'TRITON_ERROR_INVALID_COMMAND',
    0x00000002 => 'TRITON_ERROR_USER_EXISTS',
    0x00000003 => 'TRITON_ERROR_USER_UNKNOWN',
    0x00000004 => 'TRITON_ERROR_AUTH_FAILED',
    0x00000005 => 'TRITON_ERROR_INVALID_MANIFEST',
    0x00000006 => 'TRITON_ERROR_PROTOCOL',
    0x00000007 => 'TRITON_ERROR_NOT_EXIST',
    0x00000008 => 'TRITON_ERROR_NUM_BLOCKS',
    0x00000009 => 'TRITON_ERROR_STORE_FAILED',
    0x0000000a => 'TRITON_ERROR_QUOTA_EXCEEDED',
    0x0000000b => 'TRITON_ERROR_LOCK_FAILED',
    0x0000000c => 'TRITON_ERROR_DELETE_FAILED',
    0x0000000d => 'TRITON_ERROR_MACHINE_UNKNOWN',
    0x0000000e => 'TRITON_ERROR_BAD_PATCH',
    0x0000000f => 'TRITON_ERROR_OLD_CLIENT',
    0x00000010 => 'TRITON_ERROR_INVALID_STATE',
    0x00000011 => 'TRITON_ERROR_GO_AWAY',
    0x00000012 => 'TRITON_ERROR_ENCRYPT_NOT_SET',
    0x00000013 => 'TRITON_ERROR_INCORRECT_SITE',
    0x00000014 => 'TRITON_ERROR_ACCOUNT_INACTIVE',
    0x00000015 => 'TRITON_ERROR_REPLICATION_FAILED',
    0x00000016 => 'TRITON_ERROR_ACCOUNT_DATA_UNAVAIL',
    0x00000017 => 'TRITON_ERROR_STORAGE_SYSTEM_UNAVAIL',
    0x00000018 => 'TRITON_ERROR_CONTAINER_DATA_UNAVAIL',
    ...
"""

class Error_Codes(object):


    def __init__(self):
        pass

    ERROR_CODE = {
    '0xff000000':'ERROR_SOURCE_MASK',

    '0x00000000':'TRITON_ERROR_NONE',
    '0x00000001':'TRITON_ERROR_INVALID_COMMAND',
    '0x00000002':'TRITON_ERROR_USER_EXISTS',
    '0x00000003':'TRITON_ERROR_USER_UNKNOWN',
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

    '0xffffffff':'TRITON_ERROR_TDN_TIMEOUT',
    '0xfffffffe':'TRITON_ERROR_UNEXPECTED',

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

    '0x80000000':'ERROR_SOURCE_CONNECTION',

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

    ## restore errors
    '0xfff00001': 'RESTORE_ERROR_WRITE_FAILED',
    '0xfff00002': 'RESTORE_ERROR_DIRECTORY',
    '0xfff00003': 'RESTORE_ERROR_SAVE_FAILED',
    '0xfff00004': 'RESTORE_ERROR_FILES_SKIPPED',

    '0xfff00000':'ERROR_SOURCE_RESTORE',

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

    ## Reserved Mac OS X error code block: 0xffff0000 - 0xffffefff
    '0xffff0000':'ERROR_SOURCE_MAC',

    ## the following errors are all client side errors
    '0xffffff01': 'TRITON_ERROR_CALCULATE',
    '0xffffff02': 'TRITON_ERROR_MEMORY',
    '0xffffff03': 'TRITON_ERROR_INVALID_RESPONSE',
    '0xffffff04': 'TRITON_ERROR_UNKNOWN',

    ## these aren't really triton errors, but this is becoming
    ## the place to store errors we can report.

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

    ## Dumb triton stole my error numbers (-1 and -2) without telling me,
    ## so I had to change these
    '0xffffffee': 'KALYPSO_ERROR_REFERER_FRAUD',

    '0xffffffef' :'KALYPSO_ERROR_NOT_IMPLEMENTED',

    '0xff000000':'ERROR_SOURCE_CLIENT'
    }

if __name__ == '__main__':
    if Error_Codes.ERROR_CODE.has_key("0xfffffff7"):
        print Error_Codes.ERROR_CODE.get("0xfffffff7")