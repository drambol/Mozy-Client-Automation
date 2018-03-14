
Feature: Backup files when existing files are changed

  Background:
    When Windows Client is not activated

  @smoke @KAL-050
  Scenario: Windows cli backup patch files
    When I create 10 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | smoke    | smoke       | 10000    | dat      | testdata  |
    When I keyless activate windows client with
      | email                        | password  | product_key | encryption_type | encryption_key | oem            | env  |
      | clientqa_ent_pkey@mozy.com   | Test_1234 |             | pkey            | test1234       | MozyEnterprise | QA12 |
      | nathan+ent+stg2@emc.com      | Test_1234 |             | pkey            | test1234       | MozyEnterprise | STD1 |
      | nathan+pro+qa12@mozy.com     | Test_1234 |             | pkey            | test1234       | mozypro        | QA12 |
      | nathan+wan+pro+stg@emc.com   | Test_1234 |             | pkey            | test1234       | mozypro        | STD1 |
      | nathan_prd_pro_pkey@mozy.com | Test_1234 |             | pkey            | test1234       | mozypro        | PROD |
    When I create windows backupset as smoketest via CLI
    When I start windows backup via CLI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    When I wait 300 seconds
    
    When I patch test files with
      | file_folder | patch_method | content | length |
      | smoke     | append       | _+%$#     | 100    |
    When I start windows backup via CLI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    When I wait 300 seconds

    When I patch test files with
      | file_folder | patch_method | content | length |
      | smoke     | append       | ~!@*():";'     | 200    |
    When I start windows backup via CLI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    When I open Settings window
    When I select Restore panel in Settings
    Then I download files
#    Then Windows state is "Restoring"
    When I wait windows backup state "IDLE"
    Then Windows restore successfully