# Created by root at 5/16/17
Feature: Linux Client Usability
  As A linux Client User, I can use lots of usability command to help check current status

  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode

  @smoke  @regression @cleanup @lin-234 @core
  Scenario: I can query file account
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-234     |             | 100       |          |           |
    When I create linux backupset with
      | name       | paths   | excludes |
      | lin-234-bs | lin-234 |          |
    When I start backup
    When I wait state to be "IDLE"
    Then I expect backup filecount is 10

