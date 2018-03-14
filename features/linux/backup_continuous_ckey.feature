Feature: Linux backup continuous feature
  As a Linux User, I can protect my data in continous mode

  Background:
    When I cleanup local state|metric database
    When Linux Client is activated with "{env}_{oemclient}_ckey"
    When Linux Client is ready for backup at "continuous" mode

  @smoke  @regression @cleanup @lin-102 @core
  Scenario: Backup files with ckey key at continous mode
    When I check current files proccessed
    When I create linux backupset with
      | name    | paths   | excludes |
      | lin-102 | lin-102 |          |
    When I create 10 test files with
      | file_folder | file_prefix | file_size | file_ext | file_name |
      | lin-102     | lin-102     | 100       |          | auto      |
    When I restart Linux Client
    When I wait state to be "RUNNING"
    #Then I expect current files proccessed increased greater than 10
    When I download "lin-102" to "lin-102_output"
    Then I expect restore dir "lin-102" is the same with backup dir "lin-102_output"



