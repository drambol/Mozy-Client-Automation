Feature: Activate Mac Client


  Background:
    When Mac Client is not activated

  @smoke @mac-01005 @cleanup @mac_setup @mac_teardown
  Scenario: Activate Mozy Mac Client
    When I launch Mac Client from GUI
    Then I shall see "StaticText" with "value" "Enter your account information*"
    When I activate with credential "{env}_{oemclient}"
    When I create 2 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | smoke       | smoke       | 10000     | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | smoke        |
    Then I expected "Total Selected:" is 2 files
    When I start backup from GUI
    When I wait to backup finished
    Then I shall see the status menu gets updated and says 2 files backed up

  @mac-01005-1 @bifrost_with_mac
  Scenario: Activate Mozy Mac Client with new created bifrost credential
    When I create user with
    | password    | license type | licenses | user group  |
    | test123!@#  | Desktop      | 1        | test        |
    When I launch Mac Client from GUI
    Then I shall see "StaticText" with "value" "Enter your account information*"
    When I activate with bifrost created credential
    When I create 2 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | smoke-1     | smoke       | 10000     | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | smoke-1      |
    Then I expected "Total Selected:" is 2 files
    When I start backup from GUI
    When I wait to backup finished
    When I delete the new created user

  @high @mac-01020 @cleanup @mac_setup @mac_teardown
  Scenario: Mac client auto-activation
    When I auto-activate client with credential "{env}_{oemclient}"
    Then I shall see the activated username in summary tab

  @medium @mac-01030 @cleanup @mac_setup @mac_teardown
  Scenario: Try to activate Mac Client with wrong credentials
    When I launch Mac Client from GUI
     And I try to activate with credential "{env}_{oemclient}" but enter wrong password
    Then I shall see a dialog with message "Incorrect username or password" is shown
    When I close the dialog
     And I activate with credential "{env}_{oemclient}"
    Then I shall see the activated username in summary tab
