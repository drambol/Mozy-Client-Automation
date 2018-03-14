Feature: As a mozy backup software user, I can backup large number of files


  @KAL-9101 @long @windows-performance
  Scenario: backup large (1 GB) file
    # 1 GB
    #When I backup performance backupset includes 1 files with 1073741824 byte random content
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | win-perf-1G     | wp     | 1073741824      |    dat      | perf      |
    When I keyless activate windows client with
      | email                        | password  | product_key | encryption_type | encryption_key | oem            | env  |
      | clientqa_ent_pkey@mozy.com   | Test_1234 |             | pkey            | test1234       | MozyEnterprise | QA12 |
      | nathan+ent+stg2@emc.com      | Test_1234 |             | pkey            | test1234       | MozyEnterprise | STD1 |
      | nathan+pro+qa12@mozy.com     | Test_1234 |             | pkey            | test1234       | mozypro        | QA12 |
      | nathan+wan+pro+stg@emc.com   | Test_1234 |             | pkey            | test1234       | mozypro        | STD1 |
      | nathan_prd_pro_pkey@mozy.com | Test_1234 |             | pkey            | test1234       | mozypro        | PROD |
    When I create windows backupset as perflarge via CLI

    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"
    Then Windows backup successfully

