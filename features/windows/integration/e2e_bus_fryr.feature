Feature: End to End test with Windows client, WinFryr, BUS and Frejya.
  As a Windows client user, I can backup my data with Windows client and restore data through WinFryr.


  Background:
    When Windows Client is not activated

  @e2e-win
  Scenario: I can use WinFryr to restore files that backup from Windows client
    When I create 10 test files with
      | file_dir | file_prefix | file_size | file_ext | file_name |
      | smoke    | smoke       | 10000     | dat      | testdata  |

    When I open Login window
    When I create user with
      | password   | license type | licenses | user group               |
      | test123!@# | Desktop      | 1        | automation_no_backupsets |
    Then I do keyless activate with new created user using default via GUI

    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"

    When I open Settings window
    When I select FileSystem panel in Settings
    When I select files in settings filesystem
    When I start windows backup via UI
    Then Windows state is "BACKINGUP"
    When I wait windows backup state "IDLE"
    Then Windows backup successfully


    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to generate mzd
      | entity      |
      | e2e_win_001 |

    When I launch Windows Restore Manager from GUI
    When I login Windows Restore Manager with current user
    Then I use Windows Restore Manager to restore the selected files by double clicking .mzd file
    Then I check the restore job finished successfully

    Then I close Windows Restore Manager from GUI

