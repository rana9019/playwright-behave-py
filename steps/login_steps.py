from behave import given, when, then

import os

@given("I Visit the Dositrace login page")
def step_impl(context):
    context.dositrace_page.save_session()

@given("The user is on the login page")
def step_impl(context):
    context.login_page.go_to_login_page()

@then('I verify the link "{expected_url}"')
def step_impl(context, expected_url):
    context.login_page.verify_current_url(expected_url)

@when("I enter username")
def step_impl(context):
    if not os.path.exists("session.json"):
        context.login_page.enter_username()

@when("I enter Password")
def step_impl(context):
    if not os.path.exists("session.json"):
        context.login_page.enter_password()

@when("I click on login button")
def step_impl(context):
    if not os.path.exists("session.json"):
        context.login_page.click_on_login_button()

@when('I enter an invalid login "{login}"')
def step_impl(context, login):
    context.login_page.enter_wrong_login(login)

@when('I enter an invalid password "{password}"')
def step_impl(context, password):
    context.login_page.enter_wrong_password(password)

@when("I click on the Dositrace button")
def step_impl(context):
    if not os.path.exists("session.json"):
        context.login_page.click_dositrace_button()

@then('An error message "{message}" is displayed')
def step_impl(context, message):
    context.login_page.verify_error_message(message)

@given('I am on the Mot de passe oublié page')
def step_impl(context):
    context.login_page.navigate_to_password_reset_page()

@when('I enter the login "{login}"')
def step_impl(context, login):
    context.login_page.enter_login(login)

@when('I enter the email "{email}"')
def step_impl(context, email):
    context.login_page.enter_email(email)

@when("I click on the button 'Valider'")
def step_impl(context):
    context.login_page.click_submit_button()

@then("The interface contains a login field, an email field, and a 'Valider' button")
def step_impl(context):
    context.login_page.verify_login_email_and_submit_button()

@then("The login field is visible")
def step_impl(context):
    context.login_page.is_login_field_visible()

@then("The password field is visible")
def step_impl(context):
    context.login_page.is_password_field_visible()

@then("The connexion button is visible")
def step_impl(context):
    context.login_page.is_login_button_visible()

@then("The 'mot de passe oublié' link is visible")
def step_impl(context):
    context.login_page.is_forgot_password_link_visible()

@when('I click on the username in the header')
def step_impl(context):
    context.login_page.click_header_username()

@then('I should see the links "Voir mon profil" and "Déconnexion"')
def step_impl(context):
    context.login_page.verify_profile_and_logout_links()

@then('A success message is displayed with the "Déconnexion réussie" text')
def step_impl(context):
    context.login_page.check_logout_success_message()

@when('The user clicks on the "Déconnexion" button')
def step_impl(context):
    context.login_page.click_logout()