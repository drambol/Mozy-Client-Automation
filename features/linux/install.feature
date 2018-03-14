Feature: As Mozy User, I can install Mozy Linux Client on my Linux Machine

  Background: Linux Client is not installed
    When Linux Client is not installed


  @smoke @lin-454 @regression @cleanup
  Scenario: Install Linux Client
    When I install linux client with
      | job | build |
      |     | -1    |
    Then Linux Client should be installed
    Then I setup environment
