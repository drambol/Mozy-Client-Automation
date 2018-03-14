Feature: As a mozy user, I can check the  current continuous mode

  Background:
    When Linux Client is activated with "{env}_{oemclient}"

  @lin-285 @core @regression
  Scenario: Query backup mode on manual and continuous mode
    When I set backup mode as "continuous"
    Then I expect continuous output is ON
    When I set backup mode as "on-demand"
    Then I expect continuous output is OFF

  @lin-287 @core @regression
  Scenario: Set continuous mode on while in on-demand state
    When I set backup mode as "on-demand"
    Then I expect continuous output is OFF
    When I set backup mode as "continuous"
    Then I expect continuous output is ON

  @lin-288 @core @regression
  Scenario: Set continuous mode on while in continuous state
    When I set backup mode as "continuous"
    Then I expect continuous output is ON
    When I set backup mode as "on-demand"
    Then I expect continuous output is OFF

  @lin-289 @core @regression
  Scenario:  Set continuous mode off while in continuous state
    When I set backup mode as "continuous"
    Then I expect continuous output is ON
    When I set backup mode as "continuous"
    Then I expect continuous output is ON

  @lin-290 @core @regression
  Scenario:  Set continuous mode off while in on-demand stat
    When I set backup mode as "on-demand"
    Then I expect continuous output is OFF
    When I set backup mode as "on-demand"
    Then I expect continuous output is OFF