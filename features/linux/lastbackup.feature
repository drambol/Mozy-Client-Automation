# Created by root at 5/16/17
Feature: Last backup
  As A linux User, I can view last backup result via last backup command on demand state

  Background: Linux Client is activate and ready for backup
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode

  @smoke  @regression @cleanup @lin-605 @core
  Scenario: I can query last backup status
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-234     |             | 100       |          |           |
    When I create linux backupset with
      | name       | paths   | excludes |
      | lin-234-bs | lin-234 |          |
    When I start backup
    When I wait state to be "IDLE"
    Then I expect last backup status with
      | result  |
      | SUCCESS |