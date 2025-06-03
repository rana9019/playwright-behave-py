Feature: Statistique Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_579
  Scenario: Filling calendar manually in Chart1 page
    Given I am on the Chart1 page
    When The user clicks on "input#period"
    Then The calendar "input#period" appears
    When The user manually enters a date in the field "input#period"

  @A_645
  Scenario: Filling calendar manually in Chart3 page
    Given I am on the Chart3 page
    When The user clicks on "input#period"
    Then The calendar "input#period" appears
    When The user manually enters a date in the field "input#period"

  @A_683
  Scenario: Filling calendar manually in Chart4 page
    Given I am on the Chart4 page
    When The user clicks on "input#period"
    Then The calendar "input#period" appears
    When The user manually enters a date in the field "input#period"