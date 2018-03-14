
Feature: Windows demo feature
  Demo Feature for Client Automation

  Background:
    When Windows client is installed

  @smoke @KAL-001
  Scenario: Windows demo cli backup
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
    Then Windows backup successfully

  @smoke @KAL-002 @gui
  Scenario: Windows demo backup from UI
    When I create 1 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | test    | test       | 1000    | dat      | test  |
    When I keyless activate windows client with
      | email                        | password  | product_key | encryption_type | encryption_key | oem            | env  |
      | clientqa_ent_pkey@mozy.com   | Test_1234 |             | pkey            | test1234       | MozyEnterprise | QA12 |
      | nathan+ent+stg2@emc.com      | Test_1234 |             | pkey            | test1234       | MozyEnterprise | STD1 |
      | nathan+pro+qa12@mozy.com     | Test_1234 |             | pkey            | test1234       | mozypro        | QA12 |
      | nathan+wan+pro+stg@emc.com   | Test_1234 |             | pkey            | test1234       | mozypro        | STD1 |
      | nathan_prd_pro_pkey@mozy.com | Test_1234 |             | pkey            | test1234       | mozypro        | PROD |

    When I select files in settings filesystem
    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I cancel windows backup via UI
    When I wait windows backup state "IDLE"
    Then Windows backup is cancelled successfully

  @smoke @KAL-003 @cli
  Scenario: Windows demo cancel backup
    When I create 1 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | test    | test       | 1000    | dat      | test  |
    When I create windows backupset as smoketest via CLI
    When I start windows backup via CLI
    Then Windows state is "BACKINGUP"
    When I cancel windows backup via CLI
    When I wait windows backup state "IDLE"
    Then Windows backup is cancelled successfully

  @smoke @KAL-004 @cli
  Scenario: Windows backup without activate
    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"
    Then Windows backup successfully
    Then I download files
