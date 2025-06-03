from behave import given


@given("I am on the Rapport Statistiques page")
def step_impl(context):
    context.rapport_page.rapport_statistiques_url()