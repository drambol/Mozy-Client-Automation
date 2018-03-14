# Created by gongc1 at 12/14/16
Feature: Linux Backup feature
  I can Run backup command to start a backup

  Background:
    When Linux Client is activated with "{env}_{oemclient}_ckey"
    When Linux Client is ready for backup at "on-demand" mode

  @regression @cleanup @lin-100 @core
  Scenario: Backup 10 files with administration ckey under linux os and restore
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-100     | lin-100     | 100       |          | test1     |
    When I create linux backupset with
      | name    | paths | excludes |
      | lin-100 |       |          |
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-100" to "output_lin-100"
    Then I expect restore dir "output_lin-100" is the same with backup dir "lin-100"


