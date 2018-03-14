Feature: Windows Demo
  Background:
    When Windows Client is not activated

  @smoke @KAL-010 @gui
  Scenario: Windows activate from GUI

    When I open Login window
    When I activate windows gui with
      | email | password |  product_key   |  encryption_type  |  encryption_key |   oem  |   env  |
      | clientqa_ent_pkey@mozy.com    | Test_1234     |  QEZA74E9V3RGZ3WT27SQ   | pkey |   test1234  |  MozyEnterprise   |   QA12  |
#      | nativeclient_win_pro_default@emc.com    | Test_1234       |    pkey |  test1234      |   mozypro   |   QA12  |
      | nathan+pro+qa12@mozy.com    | Test_1234       |  3FETZ7A99BXB9QC7XFCR   | pkey |   test1234  |   mozypro   |   QA12  |
      | nathan_prd_pro_pkey@mozy.com    | Test_1234       |                     |  pkey |  test1234      |   mozypro   |   PROD  |

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


