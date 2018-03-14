# Created by gongc1 at 12/14/16
Feature: Backup Linux Server with personal key


  Background:
    When Linux Client is activated with "{env}_{oemclient}_pk"
    When Linux Client is ready for backup at "on-demand" mode

  @smoke @lin-200 @regression @cleanup @core
  Scenario: Backup files with personal key
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-003     | test        | 100       |          | test1     |
    When I create linux backupset with
      | name | paths   | excludes |
      |      | lin-003 |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-003" to "output_lin003"
    Then I expect restore dir "output_lin003" is the same with backup dir "lin-003"

  @smoke  @regression @cleanup @lin-276 @core
  Scenario: Download files that with personal key
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-276     | lin-276     | 100       |          | test1     |
    When I create linux backupset with
      | name    | paths   | excludes |
      | lin-276 | lin-276 |          |
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-276" to "lin-276-output"
    Then I expect restore dir "lin-276-output" is the same with backup dir "lin-276"