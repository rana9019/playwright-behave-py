from behave import given


@given("I am on the Chart1 page")
def step_impl(context):
    context.statistique_page.chart1_url()

@given("I am on the Chart3 page")
def step_impl(context):
    context.statistique_page.chart3_url()

@given("I am on the Chart4 page")
def step_impl(context):
    context.statistique_page.chart4_url()