Feature: Linux backup continuous feature
  As a Linux User, I can protect my data in continous mode

  Background:
    When I cleanup local state|metric database
    When Linux Client is activated with "{env}_{oemclient}"
    When Linux Client is ready for backup at "continuous" mode

  @smoke  @regression @cleanup @lin-102 @core
  Scenario: Backup 10 files under linux os and restore
    When I check current files proccessed
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-102     | lin-102     | 100       |          | lin-102   |
    When I create linux backupset with
      | name       | paths   | excludes |
      | lin-102-bs | lin-102 |          |
    When I restart Linux Client
    When I wait state to be "RUNNING"
    When I download "lin-102" to "lin-102_output"
    Then I expect restore dir "lin-102" is the same with backup dir "lin-102_output"


  @lin-383  @smoke  @regression @cleanup @core
  Scenario: Create new file in a backedup directory in continuous mode
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-383     | lin-383     | 100       |          | lin-383   |
    When I create linux backupset with
      | name       | paths   | excludes |
      | lin-383-bs | lin-383 |          |
    When I restart Linux Client
    When I wait state to be "RUNNING"
    When I check current files proccessed
    When I create 2 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-383     | lin-383-new | 100       |          | lin-383   |
    Then I expect current files proccessed increased greater than 2


  @lin-465 @regression @cleanup @core @wip
  Scenario: As a linux user, I can manually trigger a patch backup once backupsets is configured
    When I create linux backupset with
      | name       | paths   | excludes         | exclusionary |
      | lin-465-bs | lin-465 | lin-465/excludes |              |
    When I restart Linux Client
    When I wait state to be "RUNNING"
    When I dump last remote versions for file "lin-465/lin_0.txt"
    When I create 1 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-465     |             | 100       |          |           |
    Then I expect remote versions for file "lin-465/lin_0.txt" changed