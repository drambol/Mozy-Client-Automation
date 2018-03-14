# Created by wann at 09/04/17
Feature: Longvity test: Backup files when existing files changed, and restore in different ways.

  Background:
    When Linux Client is activated with "{env}_{oemclient}_pk"
    When Linux Client is ready for backup at "on-demand" mode

    When I create linux backupset with
      | name    | paths   | excludes    |
      | lin-int | lin-int | lin-lin-int |

  @lin-int @longevity @long @cleandownload @cleanup
  Scenario: Longevity Backup and patch files under manual backup mode
    When I prepare 100 files with
       | file_dir     | file_prefix | file_size | file_ext | file_name |patch_method | content | length |
       | lin-int    | lin-int   | 200000     | dat      | testdata  |append     | random    | 1000   |

    #When I log linux "backup" KPI start time
    When I start backup
    When I wait state to be "IDLE"
    #When I log linux "backup" KPI end time

    # In client restore
    #When I log linux "Restore" KPI start time
    When I download "lin-int" to "lin-int-output"
    #When I log linux "Restore" KPI end time
    Then I expect restore dir "lin-int-output" is the same with backup dir "lin-int"

    # Direct download
    When I visit cas host to be authenticated to do direct download from freyja site
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to direct download
      | entity                |
      | lin-int/lin-int_testdata_1.dat |
#    When I log linux "Direct Download" KPI start time
    When I decrypt files "lin-int_testdata_1.dat" to "decrypt"
#    When I log linux "Direct Download" KPI end time
    Then I expect restore dir "decrypt/lin-int_testdata_1.dat" is the same with backup dir "lin-int/lin-int_testdata_1.dat"


    # MZD restore
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to generate mzd
      | entity |
      | lin-int   |
#    When I log linux "MZD Download" KPI start time
    When I restore files through mzd to output "int_restore_001"
#    When I log linux "MZD Download" KPI end time
    Then I expect restore dir "int_restore_001" is the same with backup dir "lin-int"

    # Archive restore
    # QA12 Environment broke when download archive package, will add this part when it is fixed
    When I logon Freyja through BUS console
    When I click backup files for current machine
    When I select below files to generate tarball
      | entity |
      | lin-int  |
#    When I log linux "Archive Download" KPI start time
    When I decrypt tarball files to "archive"
#    When I log linux "Archive Download" KPI end time
    Then I expect restore dir "archive" is the same with backup dir "lin-int"
