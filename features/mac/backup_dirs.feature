# Created by gongc1 at 2/8/17
Feature: Backup Files to Mozy Cloud with mac Client
  As Mozy Mac Users, I want to backup my files to mozy cloud


  Background:
    When Mac Client is activated with credential '{env}_{oemclient}'

  @mac-02030 @cleanup @mac_setup @mac_teardown
  Scenario: Backup folders with Mac Client
    When I create 5 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-008-1   | smoke       | 1000      | txt      | testdata  |
      | mac-008-2   | smoke       | 1000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | mac-008-1    |
      | mac-008-2    |
    Then I expected "Total Selected:" is 10 files
    When I start backup from GUI
    When I wait to backup finished
