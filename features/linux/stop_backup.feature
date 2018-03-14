# Created by gongc1 at 5/8/17
Feature: Stop command
  As a Linux Client User, I can stop a backup that in progress

  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode


  @smoke @lin-451 @regression @cleanup @core
  Scenario: Stop backup
    When I create 20 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | dir1        | test        | 10000000  |          | test1     |
    When I create linux backupset with
      | name    | paths | excludes |
      | lin-451 | dir1  |          |
    When I wait state be one of "IDLE,AUTHENTICATED,RUNNING"
    When I set backup mode as "on-demand"
    When I start backup
    When I wait backup running
    When I stop backup
    When I wait state to be "IDLE"
    Then I expected last backup result in history is as below
      | result  |
      | Failure |

