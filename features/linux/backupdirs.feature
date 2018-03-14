Feature: Backup dirs related Feature
  Demo Feature for Client Automation

  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode

  @smoke @lin-97 @regression @cleanup @core
  Scenario: Backup 10 files under linux os and restore
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | dir1        | test        | 100       |          | test1     |
      | dir2        | test2       | 200       |          | test2     |
      | dir3        | test3       | 200       |          | test2     |
    When I add backupdirs with
      | paths |
      | dir1  |
      | dir2  |
      | dir3  |
    Then I list backupdirs and verify
      | paths |
      | dir1  |
      | dir2  |
      | dir3  |
    When I remove backupdirs
      | paths |
      | dir1  |
      | dir2  |
    Then I list backupdirs and verify
      | paths |
      | dir3  |
    When I clear backupdirs
    Then I list backupdirs and verify
      | paths |


