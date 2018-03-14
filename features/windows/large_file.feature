Feature: Windows demo feature


    Background:
    When Windows client is installed

#    @large_file
#    Scenario: Windows backup large file
#      When I create 1 test files with
#        | file_dir     | file_prefix   | file_size     | file_ext | file_name |
#        | large_file   | large_file    | 10740000000   | dat      | testdata  |
#      When I create windows backupset as smoketest via CLI
#      When I start windows backup via CLI
#      Then Windows state is "BACKINGUP"
#      When I wait windows backup state "IDLE"
#      Then Windows backup successfully
#      When I open Settings window
#      When I select Restore panel in Settings
#      When I log windows "Direct Download" KPI start time
#      Then I search by date to download files
#      When I wait windows backup state "IDLE"
#      Then Windows restore successfully
#      When I log windows "Direct Download" KPI end time

#    @overwrite_file
#    Scenario: Windows backup and overwrite file
#      When I create 1 test files with
#        | file_dir     | file_prefix   | file_size      | file_ext | file_name |
#        | file_change   | large_file    | 107400        | dat      | testdata  |
#      When I create windows backupset as smoketest via CLI
#      When I start windows backup via CLI
#      Then Windows state is "BACKINGUP"
#      When I wait windows backup state "IDLE"
#      Then Windows backup successfully
#      When I overwrite testdata with
#        |file_folder |offset_pattern|maxsize|minsize|
#        |file_change | random       |1000   |100    |
#      When I start windows backup via CLI
#      Then Windows state is "BACKINGUP"
#      When I wait windows backup state "IDLE"
#      Then Windows backup successfully

    @backup_new_file
    Scenario: Windwos always backup new files
      When I clean backup folder
      When I create 100 test files with
        | file_dir     | file_prefix   | file_size      | file_ext | file_name |
        | new_files    | new_file      |107400          |dat       | testdata   |
      When I create windows backupset as smoketest via CLI
      When I start windows backup via CLI
      Then Windows state is "BACKINGUP"
      When I wait windows backup state "IDLE"
      Then Windows backup successfully
      When I open Settings window
      When I select Restore panel in Settings
      When I log windows "Direct Download" KPI start time
      Then I search by date to download files
      When I wait windows backup state "IDLE"
      Then Windows restore successfully
      When I log windows "Direct Download" KPI end time
