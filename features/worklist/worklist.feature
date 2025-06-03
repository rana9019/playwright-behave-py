Feature: Worklist Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_101
  Scenario: Verify the selection of the tabs "Examens du jour" and "Examens à 7 jours"
    Given I am on the Worklist page
    When I click on the 'Examens du jour' tab
    Then The 'Examens du jour' tab is activated
    When I click on the 'Examens à 7 jours' tab
    Then The 'Examens à 7 jours' tab is activated

  @A_102
  Scenario: Verify the display of filters after clicking on "Ajouter des filtres"
    Given I am on the Worklist page
    When I click on the button 'Ajouter des filtres'
    Then The advanced filters section is displayed
    And The filters "UF" and "Équipement" are visible

  @A_106
  Scenario: Verify that the UFs are displayed when clicking on the UF field
    Given I am on the Worklist page
    When I click on the button 'Ajouter des filtres'
    When I click on the field "UF"
    Then The UF dropdown list is displayed
    And The option "Toutes les UF" is present in the list

  @A_110
  Scenario: The Equipment field displays a dropdown list with all the equipment
    Given I am on the Worklist page
    When I click on the button 'Ajouter des filtres'
    When I click on the field 'Equipement'
    Then The equipment dropdown menu is displayed
    And It contains several available equipment
