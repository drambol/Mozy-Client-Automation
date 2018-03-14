# Created by gongc1 at 2/8/17
Feature: Backup Files to Mozy Cloud with mac Client
  As Mozy Mac Users, I want to backup my files to mozy cloud


  Background:
    When Mac Client is activated with credential '{env}_{oemclient}'

  @smoke @mac-02005 @cleanup @mac_setup @mac_teardown
  Scenario: Backup files with Mac Client
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | smoke-002   | smoke       | 1000      | txt      | testdata  |
    When I add backup dirs as
      | include_dirs |
      | smoke-002    |
    Then I expected "Total Selected:" is 10 files
    When I start backup from GUI
    When I wait to backup finished
    Then I expected "Awaiting Backup:" is 0 files

  @high @mac-02010 @cleanup @mac_setup @mac_teardown
  Scenario: Backup many small files with Mac Client
    When I create 5000 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-02010   | mac         | 1000      | txt      | testdata  |
     And I add backup dirs as
      | include_dirs |
      | mac-02010    |
    When I start backup from GUI
     And I wait to backup finished
    Then I shall see the status menu gets updated and says 5000 files backed up

  @high @mac-02015 @cleanup @mac_setup @mac_teardown
  Scenario: Backup patch to files with Mac Client
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-02015   | mac         | 5120000   | txt      | testdata  |
     And I add backup dirs as
      | include_dirs |
      | mac-02015    |
    When I start backup from GUI
     And I wait to backup finished
    When I patch test files with
      | file_folder | patch_method | content | length |
      | mac-02015   | append       | aaa     | 1000   |
    Then I expected "Awaiting Backup:" is 1 files
    When I start backup from GUI
     And I wait to backup finished
    When I click restore button
     And I restore last backup files to dest "restore_02015"
    Then I expect restore dir "restore_02015" is the same with backup dir "mac-02015"

  @high @mac-02020 @cleanup @mac_setup @mac_teardown
  Scenario: Backup for file deletion with Mac Client
    When I create 5 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-02020-1 | mac         | 1000      | txt      | testdata  |
      | mac-02020-2 | mac         | 1000      | txt      | testdata  |
     And I add backup dirs as
      | include_dirs |
      | mac-02020-1  |
      | mac-02020-2  |
    When I start backup from GUI
     And I wait to backup finished
    Then I shall see the status menu gets updated and says 10 files backed up
    When I delete test files with
      | file_folder |
      | mac-02020-2 |
    When I start backup from GUI
     And I wait to backup finished
    Then I shall see the status menu gets updated and says 5 files backed up
