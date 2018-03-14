# Created by gongc1 at 2/8/17
Feature: Mac Demo - Restore
  # Enter feature description here
  #

  Background:
    When Mac Client is activated with credential '{env}_{oemclient}'

  @smoke @mac-03005 @cleanup @mac_setup @mac_teardown
  Scenario: Activate Mozy Mac Client
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | smoke-005   | smoke       | 100       | txt      | testdata  |
   When I add backup dirs as
      | include_dirs |
      | smoke-005    |
    Then I expected "Total Selected:" is 10 files
    When I start backup from GUI
    When I wait to backup finished
    When I click restore button
    When I restore last backup files to dest "mac_005"
    Then I expect restore dir "mac_005" is the same with backup dir "smoke-005"
