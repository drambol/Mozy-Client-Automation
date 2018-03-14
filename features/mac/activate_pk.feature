# Created by gongc1 at 2/8/17
Feature: Backup Files to Mozy Cloud with mac Client
  As Mozy Mac Users, I want to backup my files to mozy cloud


  Background:
    When Mac Client is activated with credential '{env}_{oemclient}_pk'

  @smoke @mac-01010 @cleanup @mac_teardown
  Scenario: Backup with pk account
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | smoke-002   | smoke       | 1000      | txt      | testdata  |
    When I create backup rules
      | name         | path      |
      | mac_002_rule | smoke-002 |
    Then I expected "Total Selected:" is 10 files
    When I start backup from GUI
    When I wait to backup finished

  @smoke @mac-01015 @cleanup @mac_setup @mac_teardown
  Scenario: Restore with pk account
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | smoke-004   | smoke       | 1000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | smoke-004    |
    Then I expected "Total Selected:" is 10 files
    When I start backup from GUI
    When I wait to backup finished
    When I click restore button
    When I restore last backup files to dest "test"
    Then I expect restore dir "test" is the same with backup dir "smoke-004"
