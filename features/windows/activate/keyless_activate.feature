Feature: Windows client activate with keyless(email&password)

  Background:
    When Windows Client is not activated

  @smoke @KAL-010 @gui @gui-smoke
  Scenario: Windows keyless activate existing account from GUI

    When I create 10 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | smoke    | smoke       | 10000     | dat      | testdata  |

    When I open Login window
    When I keyless activate windows gui with
      | email                        | password  | product_key | encryption_type | encryption_key | oem            | env  |
      | clientqa_ent_pkey@mozy.com   | Test_1234 |             | pkey            | test1234       | MozyEnterprise | QA12 |
      | nathan+ent+stg2@emc.com      | Test_1234 |             | pkey            | test1234       | MozyEnterprise | STD1 |
      | nathan+pro+qa12@mozy.com     | Test_1234 |             | pkey            | test1234       | mozypro        | QA12 |
      | nathan+wan+pro+stg@emc.com   | Test_1234 |             | pkey            | test1234       | mozypro        | STD1 |
      | nathan_prd_pro_pkey@mozy.com | Test_1234 |             | pkey            | test1234       | mozypro        | PROD |

    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    When I open Settings window
    When I select FileSystem panel in Settings
    When I select files in settings filesystem
    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"
    Then Windows backup successfully

    When I open Settings window
    When I select Restore panel in Settings
    Then I download files
#    Then Windows state is "Restoring"
    When I wait windows backup state "IDLE"
    Then Windows restore successfully

  @smoke @KAL-015 @gui @gui-smoke
  Scenario: Windows keyless activate with new user using default key from GUI

    When I create 10 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | smoke    | smoke       | 10000     | dat      | testdata  |

    When I open Login window
    When I create user with
      | password   | license type | licenses | user group               |
      | test123!@# | Desktop      | 1        | automation_no_backupsets |
    Then I do keyless activate with new created user using default via GUI

    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    When I open Settings window
    When I select FileSystem panel in Settings
    When I select files in settings filesystem
    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"
    Then Windows backup successfully

    When I open Settings window
    When I select Restore panel in Settings
    Then I download files
#    Then Windows state is "Restoring"
    When I wait windows backup state "IDLE"
    Then Windows restore successfully

