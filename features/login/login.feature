Feature: Login Feature

  @A_10
  Scenario: Verifying link
    Given The user is on the login page
    Then I verify the link "http://10.0.5.14:8080/SSO-war/"

  @A_13
  Scenario: The login interface contains all the necessary elements
    Given The user is on the login page
    Then The login field is visible
    And The password field is visible
    And The connexion button is visible
    And The 'mot de passe oublié' link is visible

  @A_15
  Scenario: Login with invalid credentials
    Given The user is on the login page
    When I enter an invalid login "fakeuser"
    And I enter an invalid password "wrongpass"
    And I click on login button
    Then An error message "Login ou mot de passe incorrect" is displayed

  @A_16
  Scenario: An interface is displayed with a field for the login, another for the email, and a 'Valider' button
    Given I am on the Mot de passe oublié page
    Then The interface contains a login field, an email field, and a 'Valider' button

  @A_17
  Scenario: By filling in both fields and clicking on 'Valider' a new password is generated and sent by email
    Given I am on the Mot de passe oublié page
    When I enter the login "rana"
    And I enter the email "reneeabidi68@gmail.com"
    And I click on the button 'Valider'
    Then I verify the link "http://10.0.5.14:8080/SSO-war/GenerateEmailMdp"

  @A_14
  Scenario: Login to Dositrace
    Given The user is on the login page
    When I enter username
    And I enter Password
    And I click on login button

  @A_20
  Scenario: Verify clicking on Dositrace button
    Given The user is on the login page
    When I click on the Dositrace button
    Then I verify the link "http://10.0.5.14:8080/DositraceV2-war/?ticket=*"

  @A_23
  Scenario: Verify visibility of 'Voir mon profil' and 'Déconnexion' links after clicking on the username
    Given The user is on the login page
    When I click on the username in the header
    Then I should see the links "Voir mon profil" and "Déconnexion"

  @A_45
  Scenario: The user successfully logs out
    Given The user is on the login page
    When The user clicks on the "Déconnexion" button
    Then A success message is displayed with the "Déconnexion réussie" text