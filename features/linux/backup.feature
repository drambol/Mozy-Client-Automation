Feature: Linux Backup feature
  I can Run backup command to start a backup

  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode

  @smoke @lin-176 @regression @cleanup @core
  Scenario: Backup 10 files under linux os and restore
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | dir1        | test        | 100       |          | test1     |
      | dir2/dir3   | test2       | 200       |          | test2     |
    When I create linux backupset with
      | name    | paths           | excludes |
      | lin-176 | dir1, dir2/dir3 |          |
    When I start backup
    When I wait state to be "IDLE"
    When I download "dir1" to "outout_lin001"
    Then I expect restore dir "outout_lin001" is the same with backup dir "dir1"


  @smoke @lin-88 @regression @cleanup @core
  Scenario: Add backupdirs
    When I create 2 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-88      | lin-88      | 1000      |          | test      |
    When I add backupdirs with
      | path   |
      | lin-88 |
    When I wait state be one of "IDLE,AUTHENTICATED"
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-88" to "lin-88-output"
    Then I expect restore dir "lin-88-output" is the same with backup dir "lin-88"
    When I clear backupdirs


  @smoke @lin-481 @regression @cleanup @core
  Scenario: Add two backupsets
    When I create 2 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-481-01  | lin-481     | 1000      |          | test      |
      | lin-481-02  | lin-481     | 1000      |          | test      |
    When I create linux backupset with
      | paths      | excludes | name |
      | lin-481-01 |          | bs1  |
      | lin-481-02 |          | bs2  |
    Then I expect listbackfiles from backupset with
      | summary                                 |
      | 4 files to backup, 4000 bytes in total. |
    When I start backup
    When I wait state to be "IDLE"


  @smoke @lin-464 @regression @cleanup @core
  Scenario: Add two backupsets test
    When I create 2 test files with
      | file_folder        | file_prefix | file_size | file_ext | file_name |
      | lin-464-01         | lin-464     | 1000      |          | test      |
      | lin-464-02/subdir1 | lin-464     | 1000      |          | test      |
      | lin-464-02/subdir2 | lin-464     | 1000      |          | test      |
    When I create linux backupset with
      | paths      | excludes           | name |
      | lin-464-01 |                    | bs1  |
      | lin-464-02 | lin-464-02/subdir2 | bs2  |
    Then I expect listbackfiles from backupset with
      | summary                                 |
      | 4 files to backup, 4000 bytes in total. |
    When I start backup
    When I wait state to be "IDLE"

  @smoke @lin-485 @regression @cleanup @core
  Scenario: Add two backupsets test
    When I create 2 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-464-01  | lin-464     | 1000      |          | test      |
      | lin-464-02  | lin-464     | 1000      |          | test      |
    When I create linux backupset with
      | paths      | excludes           | name |
      | lin-464-01 |                    | bs1  |
      | lin-464-02 | lin-464-02/subdir2 | bs2  |
    Then I expect listbackfiles from backupset with
      | summary                                 |
      | 4 files to backup, 4000 bytes in total. |
    When I start backup
    When I wait state to be "IDLE"


  @lin-493 @regression @cleanup @core
  Scenario: Backup with backupdirs and backupsets
    When I create 2 test files with
      | file_folder |
      | lin-493-dir |
      | lin-493-bs  |
    When I create linux backupset with
      | paths      | excludes | name    |
      | lin-493-bs |          | lin-493 |
    When I add backupdirs with
      | paths       |
      | lin-493-dir |
    When I start backup
    When I wait state to be "IDLE"
    When I download "lin-493-dir" to "lin-493-dir-output"
    When I download "lin-493-bs" to "lin-493-bs-output"
    Then I expect restore dir "lin-493-dir-output" is the same with backup dir "lin-493-dir"
    Then I expect restore dir "lin-493-bs-output" is the same with backup dir "lin-493-bs"
    When I clear backupdirs


  @lin-177 @regression @cleanup @core
  Scenario: Incremental backup where no files have changed
    When I create 2 test files with
      | file_folder |
      | lin-177     |
    When I create linux backupset with
      | paths   | name    |
      | lin-177 | lin-177 |
    When I start backup
    When I wait state to be "IDLE"
    When I start backup
    When I wait state to be "IDLE"
    Then I expected last backup result in history is as below
      | transfer_size |
      | 0             |


