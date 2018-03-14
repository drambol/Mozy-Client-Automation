# Created by gongc1 at 12/14/16
Feature: Backup files when existing files changed

  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode


  @smoke @lin-foo @regression @cleanup @core
  Scenario: Backup and patch files under manual backup mode
    When I create 5 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-100     | lin-100     | 1000      |          | test      |
    When I create linux backupset with
      | name | paths   | excludes |
      | lin     | lin-100 |          |
    When I wait state be one of "IDLE,AUTHENTICATED,RUNNING"
    When I start backup
    When I wait state to be "IDLE"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-100     | append       | @@@     | 100    |
    When I start backup
    When I wait state to be "IDLE"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-100     | append       | $$$     | 200    |
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-100" to "lin-100-output"
    Then I expect restore dir "lin-100-output" is the same with backup dir "lin-100"

  @smoke @lin-484 @regression @cleanup @core
  Scenario: Backup and patch files under manual backup mode
    When I create 5 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-484     | lin-484     | 10        |          | test      |
    When I create linux backupset with
      | name    | paths   | excludes    |
      | lin-484 | lin-484 | lin-lin-484 |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-100     | append       | @@@     | 100    |
    When I start backup
    When I wait state to be "IDLE"
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-484     | lin-484-new | 10        |          | test      |
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-484" to "lin-484-output"
    Then I expect restore dir "lin-484-output" is the same with backup dir "lin-484"



