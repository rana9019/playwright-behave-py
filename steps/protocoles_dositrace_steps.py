from behave import given, when, then


@when('The user clicks on the "Angiographie" link in the first row of the table')
def step_impl(context):
    context.protocoles_dositrace_page.click_angiographie_first_row()

@given('I am viewing the list protocol db')
def step_impl(context):
    context.protocoles_dositrace_page.go_to_protocol_db_list_page()

@when("The user clicks on 'Ajouter'")
def step_impl(context):
    context.protocoles_dositrace_page.click_ajouter()

@then("The protocol creation page is displayed")
def step_impl(context):
    context.protocoles_dositrace_page.creation_page_displayed()

@when('The user enters "{nom}" in the field "Nom du classeur"')
def step_impl(context, nom):
    context.protocoles_dositrace_page.fill_protocol_name(nom)

@when('Verify if the modality has 10 options')
def step_impl(context):
    context.protocoles_dositrace_page.verify_modality()

@when('The user selects "{modality}" in the dropdown list "Modalité"')
def step_impl(context, modality):
    context.protocoles_dositrace_page.select_modality_option(modality)

@when("The user clicks on 'Valider'")
def step_impl(context):
    context.protocoles_dositrace_page.click_valider_button()

@then('A success message "Le classeur de protocole a été créé avec succès" is displayed')
def step_impl(context):
    context.protocoles_dositrace_page.success_message_displayed()

@given('I am viewing the create protocol page')
def step_impl(context):
    context.protocoles_dositrace_page.go_to_create_protocol_page()

@when('I click the "Retour" button to cancel')
def step_impl(context):
    context.protocoles_dositrace_page.click_retour()

@when("The user clicks on the first protocol in the list")
def step_impl(context):
    context.protocoles_dositrace_page.click_first_protocol()

@when("The user notes the number of protocols displayed")
def step_impl(context):
    context.protocoles_dositrace_page.count_protocols()

@when("The user checks a protocol in the list")
def step_impl(context):
    context.protocoles_dositrace_page.select_protocol()

@when("The user clicks on 'Dupliquer'")
def step_impl(context):
    context.protocoles_dositrace_page.click_duplicate()

@then("The number of protocols must increase by 1")
def step_impl(context):
    context.protocoles_dositrace_page.verify_protocol_duplicated()

@when("I click on the button modify")
def step_impl(context):
    context.protocoles_dositrace_page.click_modify_button()

@when("I select a protocol to edit")
def step_impl(context):
    context.protocoles_dositrace_page.select_protocol_to_edit()

@when("I select a protocol to delete")
def step_impl(context):
    context.protocoles_dositrace_page.select_protocol_to_delete()

@when("I edit the fields 'Nom du classeur' and 'Modalité'")
def step_impl(context):
    context.protocoles_dositrace_page.fill_edit_fields()

@when("I click on the save button")
def step_impl(context):
    context.protocoles_dositrace_page.submit_modification()

@when("I confirm deletion")
def step_impl(context):
    context.protocoles_dositrace_page.force_delete_protocol()

@then("A success message is displayed confirming the deletion")
def step_impl(context):
    context.protocoles_dositrace_page.check_success_message()

@given('I am viewing the list protocol to export')
def step_impl(context):
    context.protocoles_dositrace_page.go_to_list_protocol_to_export()

