Feature: Windows client activate with keyless(email&password)


  Background:
    When Windows Client is not activated

  @e2e-win @smoke @keyless @KAL-045 @gui @gui-smoke @changeencryption
  Scenario: Windows keyless activate new account using pkey from GUI, then change encryption type to KMIP.

    When I create 10 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | smoke    | smoke       | 10000     | dat      | testdata  |

    When I create user with
      | password   | license type | licenses | user group   |
      | test123!@# | Desktop      | 1        | PKey_to_KMIP |

    When I log in BUS console to select my partner info
      | partner name                    |
      | test elk framework test partner |
    When I create client config with
      | name | type    | user group   | backup sets         | encryption | multi_encryption |
      | pkey | Desktop | PKey_to_KMIP | windows_backup_sets | pkey       |                  |
    # Activate with default key
    When I open Login window
    Then I do keyless activate with new created user using pkey via GUI

    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

#    When I open Settings window
#    When I select FileSystem panel in Settings
#    When I select files in settings filesystem
#    When I start windows backup via UI
#    Then Windows state is "BACKINGUP"
#    When I wait windows backup state "IDLE"
    Then Windows backup successfully
    # Verify data encrypted with default key
    Then I encrypt data with PKEY successfully

    # Change encryption to KMIP
    When I navigate to Dashboard
    When I change encryption type in client config
      | name    | type    | encryption |
      | pkey | Desktop | kmip       |

    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"
    When I wait 15 seconds
    When I apply change encryption
    # Window backup start automatically after apply new encrpytion type
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    Then I encrypt data with KMIP successfully