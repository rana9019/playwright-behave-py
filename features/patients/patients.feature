Feature: Patients Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_
  Scenario: Close the filter panel
    Given I am viewing the patient list
    When The user clicks on 'Ajouter des filtres'
    When The user has opened the filter panel
    Then The user clicks the close button
    And The filter panel is closed

  @A_220
  Scenario: Verify filters are displayed after clicking "Add Filters"
    Given I am viewing the patient list
    When The user clicks on 'Ajouter des filtres'
    Then The filter section appears with 'Sexe' and 'Date de naissance'

  @A_223
  Scenario: Verify the gender filter dropdown
    Given I am viewing the patient list
    When The user clicks on 'Ajouter des filtres'
    Then The options 'Tous', 'Homme', 'Femme', and 'Non défini' are available
    And The user selects a gender option
    Then The selected gender is applied correctly

  @A_224
  Scenario: Filter patients by gender
    Given I am viewing the patient list
    When The user clicks on 'Ajouter des filtres'
    Then The options 'Tous', 'Homme', 'Femme', and 'Non défini' are available
    Then The user selects a gender option
    Then The selected gender is applied correctly
    Then I click on the button filter "#filter_buttons input.btn.btn-primary[value="Filtrer"]"
    And I verify the selected gender is filtered correctly

  @A_226
  Scenario: Verify the date of birth filter displays the calendar
    Given I am viewing the patient list
    When The user clicks on 'Ajouter des filtres'
    Then The user clicks on the 'Date de naissance' field
    Then A calendar appears
    And The calendar disappears

  @A_228
  Scenario: Filter patients by birth date
    Given I am viewing the patient list
    When The user clicks on 'Ajouter des filtres'
    Then I fill the date of birth field with '08/03/1947'
    Then I click on the button filter "#filter_buttons input.btn.btn-primary.mr-1"
    Then I check if the table is filtered correctly
    And I verify that the first displayed patient has "08/03/1947" in the "Date de naissance" column

  @A_229
  Scenario: Reset the filters applied to the patients
    Given I am viewing the patient list
    When The user clicks on 'Ajouter des filtres'
    Then I fill the date of birth field with '08/03/1947'
    When I click on the left menu toggle button
    When I click on the "Réinitialiser" right bar
    Then I check if the fields are reset

  @A_231
  Scenario: Verify that the global search filters patient results correctly
    Given I am viewing the patient list
    When I take the first value from the table 'table#patient tbody'
    And I search for it in the global search field 'input[type="search"]'
    Then I should see the correct row displayed in the table 'table#patient tbody tr'

  @A_232
  Scenario: The table can be sorted by last name
    Given I am viewing the patient list
    When I click on the left menu toggle button
    When The user clicks once on the column header "Nom de famille"
    Then The table must be sorted in descending order by "#patient tbody tr td.sorting_1 a"
    When The user clicks once on the column header "Nom de famille"
    Then The table must be sorted in ascending order by "#patient tbody tr td.sorting_1 a"

  @A_235
  Scenario: Verify that the user can change the number of results of the patient list per page
    Given I am viewing the patient list
    When The user selects "10" from the "select[name='patient_length']" dropdown
    Then The displayed results should show "1 à 10" in "#patient_info"
    When The user selects "25" from the "select[name='patient_length']" dropdown
    Then The displayed results should show "1 à 25" in "#patient_info"
    When The user selects "50" from the "select[name='patient_length']" dropdown
    Then The displayed results should show "1 à 50" in "#patient_info"
    When The user selects "100" from the "select[name='patient_length']" dropdown
    Then The displayed results should show "1 à 100" in "#patient_info"

  @A_236
  Scenario: Verify that clicking on a patient's name opens the details page
    Given I am viewing the patient list
    When I click on the first patient's first name
    Then The patient's details page should be displayed

  @A_283
  Scenario: User selects a patient from the list of patients without exams
    Given I am on the 'Patients Without Study' page
    When I check the first checkbox in the table
    Then The checkbox should be checked

  @A_291
  Scenario: Verify that the global search filters patient results without exams correctly
    Given I am on the 'Patients Without Study' page
    When I take the first value from the table 'table#protocol tbody'
    And I search for it in the global search field 'input[aria-controls='protocol']'
    Then I should see the correct row displayed in the table 'table#protocol tbody tr'

  @A_295
  Scenario: Compare extracted numbers from the UI
    Given I am on the 'Patients Without Study' page
    When I extract the total number of elements displayed
    Given I am on the Dositrace page
    When I extract the number of patients without an exam
    Then The two numbers should not be equal