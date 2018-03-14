
Feature: End to End
  As a Mac End User, I can backup my data with Mac Client and restore data through Mac Fryr


  Background:
    When Mac Client is activated with credential '{env}_{oemclient}'

  @cleanup @e2e @foo @mac_teardown @macfryr_teardown
  Scenario: I can use mac fryr client to restore files that backup from mac fryr
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | e2e_001     | smoke       | 1000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | e2e_001      |
    When I start backup from GUI
    When I wait to backup finished
    When I click restore button
    When I restore last backup files to dest "e2e_001-in-client"
    Then I expect restore dir "e2e_001-in-client" is the same with backup dir "e2e_001"
    When I close Mac Client
     And I close Mozy Restore application
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to generate mzd
      | entity  |
      | e2e_001 |
    When I launch MacFryr Client from GUI
    When I login MacFryr with current user
    When I restore last mzd to directory "e2e_001-output-mzd"
    Then I expect restore dir "e2e_001-output-mzd" is the same with backup dir "e2e_001"
    When I close Mac Fryr
