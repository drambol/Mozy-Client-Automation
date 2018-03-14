Feature: Windows Client longevity test

    Background:
    When Windows Client is installed
    When I generate clean configuration of windows Client
    When I open Login window
    When I create user with
      | password   | license type | licenses | user group               |
      | test123!@# | Desktop      | 1        | no_backupsets            |
    Then I do keyless activate with new created user using default via GUI
    When I clean backup folder

    @longevity
    Scenario: do longevity test on windows client
      When I clean reatore folder
      When I prepare 10 files with
       | file_dir     | file_prefix | file_size | file_ext | file_name |patch_method | content | length |
       | schedule     | schedule   | 20000     | dat     | testdata  |insert     | random    | 1000   |
      When I create windows backupset as longevitytest via CLI
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

      When I logon Freyja through BUS console
      When I click backup files for current machine
      When I select below files to generate mzd
        | entity      |
        | schedule    |
      When I launch Windows Restore Manager from GUI
      When I login Windows Restore Manager with current user
      Then I use Windows Restore Manager to restore the selected files by double clicking .mzd file
      Then I check the restore job finished successfully

      When I logon Freyja through BUS console
      When I click backup files for current machine
      When I select below files to generate tarball
        | entity    |
        | schedule  |
      Then I use Windows Restore Manager to decrypt the package by archive restore
      Then I check the restore job finished successfully

