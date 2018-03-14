# Created by gongc1 at 12/14/16
Feature: Linux demo feature
  Demo Feature for Client Automation

  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode

  @smoke @lin-355 @regression @cleanup @core
  Scenario: Backup 10 files under linux os and restore
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | dir1        | test        | 100       |          | test1     |
    When I create linux backupset with
      | name | paths | excludes |
      |      | dir1  |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    Then I expected last backup result in history is as below
      | result  | transfer_size | failures |
      | Success | 1540          | 0        |

