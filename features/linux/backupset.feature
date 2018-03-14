Feature: Backupset sets
  As Linux Client User, I can use backupset to define what files will be backup to mozy

  Background:
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "on-demand" mode


  @lin-482 @regression @cleanup @core
  Scenario: Backup on demand with backup set configured (Baseline)
    When I create 1 test files with
      | file_folder             | file_prefix | file_size | file_ext | file_name |
      | lin482/tc12/dir/tc_ex_1 | lin-482     | 1000      |          | auto      |
    When I create linux backupset with
      | paths                | excludes | name                | exclusionary |
      | lin482/tc1*          |          | lin482-include      | false        |
      | lin482/tc*/*/tc_ex_* |          | lin482-exclusionary | true         |
    When I dump last remote versions for file "lin482/tc12/dir/tc_ex_1/lin-482_auto_0.txt"
    When I start backup
    When I wait state to be "IDLE"
    Then I expect remote versions for file "lin482/tc12/dir/tc_ex_1/lin-482_auto_0.txt" unchanged

  @lin-515 @regression @cleanup @core
  Scenario: Include a file in backupset paths/excludes
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-515     | lin-515     | 1000      |          | auto      |
    When I create linux backupset with
      | paths                      | name       |
      | lin-515/lin-515_auto_0.txt | lin-515-bs |
    When I dump last remote versions for file "lin-515/lin-515_auto_0.txt"
    When I start backup
    When I wait state be one of "IDLE, AUTHENTICATED"
    Then I expect remote versions for file "lin-515/lin-515_auto_0.txt" unchanged

  @lin-532 @regression @cleanup @core
  Scenario: Edit Backupset with rules
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-532-1   | prefix1     | 10        |          | auto      |
      | lin-532-2   | prefix2     | 10        |          | auto      |
      | lin-532-1   | lin-532     | 10        |          | test      |
    When I create linux backupset with
      | paths    | name         | filenames |
      | lin-532* | lin-532-bs_1 | prefix*   |
    When I start backup
    When I wait state be one of "IDLE"
    When I create linux backupset with
      | paths     | name         | filenames      |
      | lin-532-1 | lin-532-bs_2 | prefix*;*test* |
    When I dump last remote versions for file "lin-532-1/lin-532_test_0.txt"
    When I start backup
    When I wait state be one of "AUTHENTICATED,IDLE"
    Then I expected file "lin-532-1/lin-532_auto_0.txt" is deleted from remote
    Then I expect remote versions for file "lin-532-1/lin-532_test_0.txt" changed

  @lin-535 @regression @cleanup @core
  Scenario: List All files for backupset
    When I create 1 test files with
      | file_folder   | file_prefix | file_size | file_ext | file_name |
      | lin-535-1     |             | 10        |          | auto      |
      | lin-535-1/sub |             | 10        |          | auto      |
      | lin-535-1     |             | 10        |          | not       |
    When I create linux backupset with
      | paths    | name  | excludes      | exclusionary | filenames |
      | lin-535* | rule1 | lin-535-1/sub |              | *auto*    |
    Then I expect listallfiles includes files
      | paths                    |
      | lin-535-1/lin_auto_0.txt |
    Then I expect listallfiles not includes files
      | paths                        |
      | lin-535-1/sub/lin_auto_0.txt |
      | lin-535-1/lin_not_0.txt      |

  @lin-537 @regression @cleanup @core
  Scenario: As mozy linux user, I can define multiples rules within one backupset.  those backupset rules will take AND operation.
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-537-1   |             | 10        |          | auto      |
      | lin-537-1   |             | 10        |          | auto.not  |
    When I create linux backupset with
      | paths    | name  | exclusionary | filenames | exclude_filenames |
      | lin-537* | rule1 |              | *auto*    | *not*             |
    Then I expect listallfiles includes files
      | paths                    |
      | lin-537-1/lin_auto_0.txt |
    Then I expect listallfiles not includes files
      | paths                        |
      | lin-537-1/lin_auto.not_0.txt |

  @lin-538 @regression @cleanup @core
  Scenario: Exclusive Rule in exclusionary backupset
    When I create linux backupset with
      | name             | paths   | excludes | exclusionary | filenames                      | exclude_filenames | filetypes | exclude_filetypes |
      | Inclusive_lin538 | lin-538 |          |              | start*,*contain*,*end,fullname |                   |           |                   |
      | Exclusive_lin538 | lin-538 |          | True         |                                |                   | dat       |                   |
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-538     | start       | 10        | txt      |           |
      | lin-538     | start       | 10        | dat      |           |
      | lin-538     |             | 10        | txt      | contains  |
      | lin-538     |             | 10        | dat      | contains  |
    Then I expect listallfiles includes files
      | paths                      |
      | lin-538/lin_contains_0.txt |
      | lin-538/start_0.txt        |
    Then I expect listallfiles not includes files
      | paths                      |
      | lin-538/lin_contains_0.dat |
      | lin-538/start_0.dat        |

  @lin-464 @regression @cleanup @core
  Scenario: As a linux user, I can manually trigger a baseline backup once backupsets is configured
    When I create 1 test files with
      | file_folder     | file_prefix | file_size | file_ext | filename |
      | lin-464         |             | 10        |          |          |
      | lin-464/exclude |             | 10        |          |          |
    When I create linux backupset with
      | name            | paths           | excludes | exclusionary | filenames | exclude_filenames | filetypes | exclude_filetypes |
      | lin-464-include | lin-464         |          |              |           |                   |           |                   |
      | lin-464-exclude | lin-464/exclude |          | True         |           |                   |           |                   |
    When I dump last remote versions for file "lin-464/lin_0.txt"
    When I start backup
    When I wait state to be "IDLE"
    When I delete test files with
      | file_folder | pattern   |
      | lin-464     | lin_0.txt |
    When I start backup
    When I wait state to be "IDLE"
    Then I expected file "lin-464/lin_0.txt" is deleted from remote
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | filename |
      | lin-464     | new         | 10        |          |          |
    When I dump last remote versions for file "lin-464/new_0.txt"
    When I start backup
    When I wait state to be "IDLE"
    Then I expect remote versions for file "lin-464/new_0.txt" changed


  @lin-482 @regression @cleanup @core
  Scenario: Do not backup if included by exclusionary Backupset
    When I create linux backupset with
      | name            | paths           | excludes | exclusionary |
      | lin-482-include | lin-482         |          |              |
      | lin-482-exclude | lin-482/exclude |          | True         |
    When I create 1 test files with
      | file_folder     | file_prefix | file_size | file_ext | filename |
      | lin-482         |             | 10        |          |          |
      | lin-482/exclude |             | 10        |          |          |
    When I start backup
    When I wait state to be "IDLE"
    Then I expect file "lin-482/exclude/lin-0.txt" is not backuped
    When I create linux backupset with
      | name            | paths       | excludes | exclusionary |
      | lin-482-include | lin-482     |          |              |
      | lin-482-exclude | lin-482/ex* |          | True         |
    When I create 1 test files with
      | file_folder     | file_prefix | file_size | file_ext | filename |
      | lin-482         |             | 10        |          |          |
      | lin-482/exclude |             | 10        |          |          |
    When I start backup
    When I wait state to be "IDLE"
    Then I expect file "lin-482/exclude/lin-0.txt" is not backuped

  @lin-472 @regression @cleanup @core
  Scenario: Paths in backup set
    When I create linux backupset with
      | name            | paths                                                                                    | excludes | exclusionary |
      | lin-482-include | not_existed;include;include;test/../sub;INCLUDE;aaaaaaaa/aaaaa/aaaaa/aaaaa;dir1;dir1/sub |          |              |
    Then I expect dump backupset include
      | paths                              |
      | +{root}/INCLUDE                    |
      | +{root}/aaaaaaaa/aaaaa/aaaaa/aaaaa |
      | +{root}/dir1                       |
      | +{root}/dir1/sub                   |
      | +{root}/include                    |
      | +{root}/not_existed                |
      | +{root}/sub                        |

  @lin-413 @regression @cleanup @core
  Scenario: Delete backup dirs locally for backupsets include path
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | filename |
      | lin-413     |             | 10        |          |          |
    When I create 1 test files with
      | name       | paths   | excludes | exclusionary |
      | lin-413-bs | lin-413 |          |              |
    When I start backup
    When I wait state to be "IDLE"
    When I dump last remote versions for file "lin-413/lin_0.txt"
    When I delete test files with
      | file_folder |
      | lin-413     |
    When I start backup
    When I wait state to be "IDLE"
    Then I expect remote versions for file "lin-413/lin_0.txt" unchanged

  @lin-484 @regression @cleanup @core @wip
  Scenario: As a linux user, I can manually trigger a patch backup once backupsets is configured
    When I create  2 test files with
      | file_folder | file_prefix | file_size | file_ext | filename |
      | lin-484     |             | 10        |          |          |
    When I create linux backupset with
      | name       | paths   | excludes         | exclusionary |
      | lin-484-bs | lin-484 | lin-484/excludes |              |
    When I start backup
    When I wait state to be "IDLE"
    When I dump last remote versions for file "lin-484/lin_0.txt"
    When I patch test files with
      | file_folder | patch_method | content | length |
      | lin-484     | append       | @@@     | 100    |
    When I start backup
    When I wait state to be "IDLE"
    When I start backup
    When I wait state to be "IDLE"
    Then I expect remote versions for file "lin-484/lin_0.txt" changed
    When I delete test files with
      | file_folder | pattern   |
      | lin-484     | lin_1.txt |
    When I start backup
    When I wait state to be "IDLE"
    When I start backup
    When I wait state to be "IDLE"
    Then I expected file "lin-484/lin_1.txt" is deleted from remote
    When I create  1 test files with
      | file_folder      | file_prefix | file_size | file_ext | filename |
      | lin-484/excludes |             | 10        |          |          |
    When I start backup
    When I wait state to be "IDLE"
    When I start backup
    When I wait state to be "IDLE"
    Then I expect file "lin-484/excludes/lin_0.txt" is not backuped





