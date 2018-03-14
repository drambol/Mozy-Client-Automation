Feature: Linux backup continuous feature
  As a Linux User, I can protect my data in continous mode

  Background:
    When I cleanup local state|metric database
    When Linux Client is activated with "{env}_{oemclient}_pk"
    When Linux Client is ready for backup at "continuous" mode

  @smoke  @regression @cleanup @lin-202 @core
  Scenario: Backup files with personal key at continous mode
    When I check current files proccessed
    When I create linux backupset with
      | name | paths | excludes |
      | test | dir1  |          |
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | dir1        | test        | 100       |          | test1     |
    When I restart Linux Client
    When I wait state to be "RUNNING"
    #Then I expect current files proccessed increased greater than 10
    When I download "dir1" to "dir1_output"
    Then I expect restore dir "dir1" is the same with backup dir "dir1_output"

