Feature: Risk Patient Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_469
  Scenario Outline: Select a date range on the page
    Given I am on the Risk Patient page
    When I click on the left menu toggle button
    When The user clicks on the button "<periode>"
    Then The selected dates match the period "<periode>"

    Examples:
      | periode           |
      | 3 derniers mois      |
      |  6 derniers mois  |
      |  12 derniers mois  |
      | dernier mois  |

  @A_470
  Scenario: Clicking on the "ajouter un filtre" field displays the expected filters on the Risk Patient page
    Given I am on the Risk Patient page
    When I click on the button 'Ajouter des filtres'
    Then I should see the following filters: Modalité, Equipement, Suivi nécessaire, Réalisation du suivi, Patient à risques

  @A_471
  Scenario: Click on Reset to clear all filters
    Given I am on the Risk Patient page
    When I click on the button 'Ajouter des filtres'
    When I fill in some filters
    And I click on the "Réinitialiser" right bar
    Then All filter fields should be reset

  @A_472
  Scenario: Filter the table based on the selection "Oui"
    Given I am on the Risk Patient page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    When I click on the button 'Ajouter des filtres'
    When The user selects 'Oui' in the filter
    Then Wait
    Then I click on the button filter "#filter_buttons input#fil"
    Then The table should display only the rows with 'Oui' selected

  @A_474
  Scenario: Clicking the radio button should make the patient and exam visualization visible
    Given I am on the Risk Patient page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    When I click on the left menu toggle button
    When I click on the first radio button in the table
    Then The "a.btn.btn-secondary#viewPatient" button should be visible
    Then The "a.btn.btn-secondary#viewExam" button should be visible

  @A_475
  Scenario: Compare column headers between the two tables
    Given I am on the Risk Patient page
    When I get the column headers of the first table
    Given I am on the Examens page
    When I get the column headers of the second table
    Then All column headers in the second table should exist in the first table

  @A_476
  Scenario: Verify that the follow-up status is displayed at the bottom of the table
    Given I am on the Risk Patient page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    Then The last 'statut de suivi' should be 'Suivi non réalisé' or 'Suivi réalisé' or 'Suivi non demandé'

  @A_477
  Scenario: Clicking on "Oui" in "Suivi nécessaire" activates the button and turns "Suivi non réalisé" red
    Given I am on the Risk Patient page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    When I click on "Oui" in "Suivi nécessaire"
    Then Wait
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    Then "Suivi non réalisé" becomes red
    Then The button in "Réalisation du suivi" gets activated

  @A_478
  Scenario: The follow-up button can be clicked, the form can be filled out and saved
    Given I am on the Risk Patient page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    When I click on the button 'réalisation du suivi'
    Then A popup appears with a checkbox, a comment area, and two buttons 'Annuler' and 'Enregistrer'
    When I check the checkbox 'Suivi réalisé'
    And I fill the comment area with 'Commentaire de suivi'
    And I click on the button 'Enregistrer'
    Then The page reloads with the active filters retained
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    Then If 'Suivi réalisé' is checked then the status becomes 'Suivi réalisé' in green

  @A_479
  Scenario: If "No" is clicked then the status "Suivi non nécessaire" appears in black and the "réalisation du suivi" button remains disabled
    Given I am on the Risk Patient page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    When I click on "Non" in "Suivi nécessaire"
    Then Wait
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    Then The status becomes 'Suivi non nécessaire' and appears in black
    And The 'réalisation du suivi' button remains inactive

  @A_480
  Scenario: Change the follow-up status and verify tooltip text on hover
    Given I am on the Risk Patient page
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    When I click on the left menu toggle button
    When I click on "Oui" in Suivi necessary
    Then Wait
    When The user clicks on "#daterangepicker1"
    Then The calendar "#daterangepicker1" appears
    Then The user selects a date "29/08/2023 - 05/05/2025" in the field "#daterangepicker1"
    Then I click enter
    Then The tooltip text should match the follow-up status from the table