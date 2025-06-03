from behave import given, when, then


@given("I am on the Worklist page")
def step_impl(context):
    context.worklist_page.worklist_page_url()

@when("I click on the 'Examens du jour' tab")
def step_impl(context):
    context.worklist_page.click_examens_du_jour()

@then("The 'Examens du jour' tab is activated")
def step_impl(context):
    context.worklist_page.verify_examens_du_jour_active()

@when("I click on the 'Examens à 7 jours' tab")
def step_impl(context):
    context.worklist_page.click_examens_7_jours()

@then("The 'Examens à 7 jours' tab is activated")
def step_impl(context):
    context.worklist_page.verify_examens_7_jours_active()

@when("I click on the field 'Equipement'")
def step_impl(context):
    context.worklist_page.click_champ_equipement()

@when("I click on the button 'Ajouter des filtres'")
def step_impl(context):
    context.worklist_page.click_ajouter_filtres()

@then("The advanced filters section is displayed")
def step_impl(context):
    context.worklist_page.verify_filtres_section()

@then('The filters "UF" and "Équipement" are visible')
def step_impl(context):
    context.worklist_page.verify_filtres_uf_equipement()

@when('I click on the field "UF"')
def step_impl(context):
    context.worklist_page.click_uf()

@then("The UF dropdown list is displayed")
def step_impl(context):
    context.worklist_page.verify_dropdown_uf()

@then('The option "Toutes les UF" is present in the list')
def step_impl(context):
    context.worklist_page.verify_all_uf()

@then("The equipment dropdown menu is displayed")
def step_impl(context):
    context.worklist_page.verify_dropdown_equipement()

@then("It contains several available equipment")
def step_impl(context):
    context.worklist_page.verify_equipements_list()
