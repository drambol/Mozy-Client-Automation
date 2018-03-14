Feature: Windows client auto-activate

  Background:
    When Windows Client is not activated


  @smoke @auto-activate
  Scenario: Windows auto-activate from command-line
    When I activate windows mozypro in autoactivate environment
    When I auto activate client with user auto_test
