Feature: Protocoles Dositrace Feature

  @login
  Scenario: Save login session to Dositrace
    Given I Visit the Dositrace login page

  @A_407
  Scenario: Verify opening protocol creation page
    Given I am viewing the list protocol db
    When The user clicks on 'Ajouter'
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/CreateProtocolDB"

  @A_408
  Scenario: Create a protocol and verify the existence of 10 modalities
    Given I am viewing the list protocol db
    When The user clicks on 'Ajouter'
    Then The protocol creation page is displayed
    When The user enters "Test Protocol" in the field "Nom du classeur"
    And Verify if the modality has 10 options
    And The user selects "IRM (MR)" in the dropdown list "Modalité"
    And The user clicks on 'Valider'
    Then A success message "Le classeur de protocole a été créé avec succès" is displayed

  @A_409
  Scenario: Cancel the creation by clicking on Back
    Given I am viewing the create protocol page
    When I click the "Retour" button to cancel
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ListProtocolDB"

  @A_410
  Scenario: By clicking on the first protocol, the user is redirected to the details page
    Given I am viewing the list protocol db
    When I click on the left menu toggle button
    When The user clicks on the first protocol in the list
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ListProtocol"

  @A_411
  Scenario: Duplicate a selected protocol
    Given I am viewing the list protocol db
    When I click on the left menu toggle button
    When The user notes the number of protocols displayed
    When The user checks a protocol in the list
    And The user clicks on 'Dupliquer'
    Then The number of protocols must increase by 1

  @A_412
  Scenario: Verify opening modify protocol page
    Given I am viewing the list protocol db
    When I click on the button modify
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ModifyProtocolDB"

  @A_413
  Scenario: Edit an existing protocol
    Given I am viewing the list protocol db
    When I click on the left menu toggle button
    When I select a protocol to edit
    When I click on the button modify
    And I edit the fields 'Nom du classeur' and 'Modalité'
    And I click on the save button

  @A_414
  Scenario: Cancel the modification by clicking on Back
    Given I am viewing the list protocol db
    When I click on the left menu toggle button
    When I select a protocol to edit
    When I click on the button modify
    When I click the "Retour" button to cancel
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/ListProtocolDB"

  @A_415
  Scenario: Deletion of a protocol
    Given I am viewing the list protocol db
    When I click on the left menu toggle button
    When I select a protocol to edit
    And I click on the "#del" button
    And I confirm deletion
    Then A success message is displayed confirming the deletion

  @A_431
  Scenario: Verify that the user can change the number of results of the list protocol to export per page
    Given I am viewing the list protocol to export
    When The user selects "10" from the "select[name='protocolList_length']" dropdown
    Then The displayed results should show "1 à 10" in "div#protocolList_info"
    When The user selects "25" from the "select[name='protocolList_length']" dropdown
    Then The displayed results should show "1 à 25" in "div#protocolList_info"
    When The user selects "50" from the "select[name='protocolList_length']" dropdown
    Then The displayed results should show "1 à 50" in "div#protocolList_info"
    When The user selects "100" from the "select[name='protocolList_length']" dropdown
    Then The displayed results should show "1 à 100" in "div#protocolList_info"