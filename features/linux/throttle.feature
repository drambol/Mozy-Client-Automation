Feature: As a Mozy Linux Client User,
  I can set the maximum amount of network bandwidth that can be used

  Background:
    When Linux Client is activated with "{env}_{oemclient}"

  @lin-326 @core @regression
  Scenario: Throttle command to query state
    When I disable throttle
    Then I expect throttle is disabled
    When I enable throttle to bps 100
    Then I expect throttle value is "100 bits per second"


  @lin-327 @core @regression
  Scenario: user can enable the throttle function
    When I enable throttle to bps 200
    Then I expect throttle value is "200 bits per second"

  @lin-328 @core @regression
  Scenario: Throttle command to enable (while already enabled)
    When I enable throttle to bps 200
    Then I expect throttle value is "200 bits per second"
    When I enable throttle to kps 3
    Then I expect throttle value is "3072 bits per second"


  @lin-329 @core @regression
  Scenario: Throttle command to disable
    When I enable throttle to bps 200
    Then I expect throttle value is "200 bits per second"
    When I disable throttle
    Then I expect throttle is disabled

  @lin-330 @core @regression
  Scenario:Throttle command to disable (while already disabled)
    When I disable throttle
    Then I expect throttle is disabled
    When I disable throttle
    Then I expect throttle is disabled


  @lin-331 @core @regression @cleanup
  Scenario: Throttle command to enable (while backup running)
    When I disable throttle
    When Linux Client is ready for backup at "on-demand" mode
    When I create 20 test files with
      | file_folder |
      | lin-331     |
    When I create linux backupset with
      | paths   | name    |
      | lin-331 | lin-331 |
    When I start backup
    When I wait state to be "RUNNING"
    When I enable throttle to bps 100
    Then I expect throttle value is "100 bits per second"

  @lin-332 @core @regression @cleanup
  Scenario: Throttle command to disable (while backup running)
    When I enable throttle to bps 200
    When Linux Client is ready for backup at "on-demand" mode
    When I create 20 test files with
      | file_folder |
      | lin-332     |
    When I create linux backupset with
      | paths   | name    |
      | lin-332 | lin-332 |
    When I start backup
    When I wait state to be "RUNNING"
    When I disable throttle
    Then I expect throttle is disabled
    When I wait state to be "IDLE"


  @lin-333 @core @regression @cleanup
  Scenario:Throttle command to disable (continuous mode)
    When I enable throttle to bps 200
    When Linux Client is ready for backup at "continuous" mode
    When I create 20 test files with
      | file_folder |
      | lin-333     |
    When I create linux backupset with
      | paths   | name    |
      | lin-333 | lin-333 |
    When I restart Linux Client

    When I disable throttle
    Then I expect throttle is disabled

  @lin-334 @core @regression @cleanup
  Scenario: Throttle command to enable (continuous mode)
    When I disable throttle
    When Linux Client is ready for backup at "continuous" mode
    When I create 20 test files with
      | file_folder |
      | lin-334     |
    When I create linux backupset with
      | paths   | name    |
      | lin-334 | lin-334 |
    When I restart Linux Client
    When I wait state to be "RUNNING"
    When I enable throttle to kps 1
    Then I expect throttle value is "1024 bits per second"


  @lin-336 @core @regression @cleanup
  Scenario: Use throttle --bps to set (while enabled)
    When I disable throttle
    When I enable throttle to bps 500
    Then I expect throttle value is "500 bits per second"

  @lin-337 @core @regression @cleanup
  Scenario: Use throttle --bps 0 to remove limit
    When I enable throttle to bps 500
    When I enable throttle to bps 0
    Then I expect throttle is disabled

  @lin-339 @core @regression @clean
  Scenario: Use throttle --kps to set (while disabled)
    When I disable throttle
    When I enable throttle to kps 2
    Then I expect throttle value is "2048 bits per second"

  @lin-340 @core @regression @clean
  Scenario: Use throttle --kps to set (while disabled)
    When I enable throttle to kps 2
    When I enable throttle to kps 0
    Then I expect throttle is disabled