# Created by wann at 09/04/17
Feature: Test KPI.


  @test
  Scenario: Linux KPI
    When I log linux "MZD Download" KPI start time
    When I wait 2 seconds
    When I log linux "MZD Download" KPI end time
