# Created by zhouf10 at 8/10/17
Feature: Backup files large enough to resume with Mac client
  As Mozy Mac Users, I can continue to backup my files to Mozy cloud after pause

  Background:
    When Mac Client is activated with credential '{env}_{oemclient}'

  @high @mac-06000 @cleanup @mac_setup @mac_teardown
  Scenario: Files resume after pause
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | mac-06000   | mac-06000   | 52428800  | txt      | testdata  |
     And I add backup dirs as
      | include_dirs |
      | mac-06000    |
    When I start backup from GUI
     And The backup is 20.0 percent left
    When I click the menu item "Pause Backup"
    Then I shall see the action field displays as "Back Up Now"
    When I start backup from GUI
     And I wait to backup finished
    Then I shall see the status menu gets updated and says 1 files backed up
