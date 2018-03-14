Feature: Windows client activate with keyless(email&password)


  Background:
    When Windows Client is not activated


  @smoke @keyless @KAL-026 @gui @gui-smoke @ckey
  Scenario: Windows keyless activate existing account using ckey from GUI

    When I create 10 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | smoke    | smoke       | 10000     | dat      | testdata  |

    When I open Login window
    When I keyless activate windows gui with
      | email                         | password  | product_key | encryption_type | encryption_key | oem     | env  |
      | clientqa_pro_ckey@mozy.com | Test_1234 |             | ckey         | test1234       | mozypro | QA12 |


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


  @e2e-win @smoke @keyless @KAL-027 @gui @gui-smoke @ckey
  Scenario: Windows keyless activate new account using ckey from GUI
#    When I create 10 test files with
#      | file_dir | file_prefix | file_size | file_ext | file_name |
#      | smoke    | smoke       | 10000     | dat      | testdata  |

    When I create user with
      | password   | license type | licenses | user group   |
      | test123!@# | Desktop      | 1         | CKey_to_KMIP |

#    When I log in BUS console to select my partner info
#      | partner name                    |
#      | test elk framework test partner |
#    When I create client config with
#      | name | type    | user group    | backup sets          | encryption |
#      | ckey | Desktop | CKey_to_KMIP | windows_backup_sets |  ckey       |

    When I open Login window
    Then I do keyless activate with new created user using ckey via GUI

    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    When I open Settings window
    When I select FileSystem panel in Settings
    When I select files in settings filesystem
    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"
    Then Windows backup successfully

    Then I encrypt data with ckey successfully

