Feature: New User Scenario
  As a Mac Client User, When My account is newly created, I can use my account to protect my data

  Background:
    When Mac Client is not activated

  @mac-01900 @cleanup @mac_setup @mac_teardown @web_teardown
  Scenario: Activate Mozy Mac Client
    When I create user with
      | password   | license type | licenses |
      | test123!@# | Desktop      | 1        |
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | smoke-005   | e2e         | 1000      | txt      | testdata  |
    When I launch Mac Client from GUI
    When I activate with bifrost created credential
    When I add backup dirs as
      | include_dirs |
      | smoke-005    |
    Then I expected "Total Selected:" is 10 files
    When I start backup from GUI
    When I wait to backup finished
    When I click restore button
    When I restore last backup files to dest "mac_005"
    Then I expect restore dir "mac_005" is the same with backup dir "smoke-005"
