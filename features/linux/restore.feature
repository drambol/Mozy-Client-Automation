# Created by gongc1 at 12/14/16
Feature: Backup Linux Server with personal key


  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode

  @smoke @lin-266 @regression @cleanup @core
  Scenario: Restores backup files
    When I create 5 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-266     | test        | 1000      |          | test1     |
    When I create linux backupset with
      | name    | paths   | excludes |
      | lin-266 | lin-266 |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    Then I expected last backup result in history is as below
      | result  |
      | Success |
    When I download "lin-266" to "lin-266_output"
    Then I expect restore dir "lin-266" is the same with backup dir "lin-266_output"


  @lin-267 @regression @cleanup @smoke @core
  Scenario:Download a file with a single patch
    When I create 5 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-267     | test        | 1000      |          | test1     |
    When I create linux backupset with
      | name    | paths   | excludes |
      | lin-267 | lin-267 |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-267     | append       | $$$     | 1000   |
    When I wait 10 seconds
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-267" to "lin-267-output"
    Then I expect restore dir "lin-267-output" is the same with backup dir "lin-267"

  @lin-268 @regression @cleanup @core
  Scenario: download a file with multiple baseline
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-268     | test        | 100       |          | test1     |
    When I create linux backupset with
      | name    | paths   | excludes |
      | lin-268 | lin-268 |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-268     | test        | 100       |          | test1     |
    When I start backup
    When I wait state to be "IDLE"
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-268     | test        | 100       |          | test1     |
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-268" to "lin-268-output"
    Then I expect restore dir "lin-268-output" is the same with backup dir "lin-268"

  @lin-269 @regression @cleanup @core
  Scenario: download a file with multiple patches
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-269     | test        | 1000      |          | test1     |
    When I create linux backupset with
      | name    | paths   | excludes |
      | lin-269 | lin-269 |          |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-269     | append       | $$$     | 10     |
    When I wait 10 seconds
    When I start backup
    When I wait state to be "IDLE"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-269     | append       | 111     | 10     |
    When I start backup
    When I wait state to be "IDLE"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-269     | append       | 222     | 10     |
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-269" to "lin-269-output"
    Then I expect restore dir "lin-269-output" is the same with backup dir "lin-269"


  @lin-583 @regression @cleanup @core
  Scenario: download files by extension
    When I create 1 test files with
      | file_folder  | file_prefix | file_size | file_ext | file_name |
      | lin-583/dir1 | test        | 1000      | txt      | test1     |
      | lin-583/dir2 | test        | 1000      | dat      | test1     |
    When I create linux backupset with
      | name    | paths   | excludes |
      | lin-583 | lin-583 |          |
    When I start backup
    When I wait state to be "IDLE"
    When I download files with
      | path    | output         | extensions |
      | lin-583 | lin-583-output | txt        |
    Then I expect restore dir "lin-583-output" is the same with backup dir "lin-583/dir1"

