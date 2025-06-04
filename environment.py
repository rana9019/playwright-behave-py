from playwright.sync_api import sync_playwright
from utils.excel_updater import update_excel_with_results

from pages.dositrace_page import DositracePage
from pages.alerts_page import AlertsPage
from pages.exams_page import ExamsPage
from pages.login_page import LoginPage
from pages.nrd_nri_page import NrdNriPage
from pages.patients_page import PatientsPage
from pages.protocoles_dositrace_page import ProtocolesDositracePage
from pages.rapport_page import RapportPage
from pages.risk_patient_page import RiskPatientPage
from pages.statistique_page import StatistiquePage
from pages.worklist_page import WorklistPage

from pathlib import Path
import dotenv
import os
import datetime

dotenv.load_dotenv(dotenv_path=Path("config/.env"))

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)

    storage_path = "session.json"

    if os.path.exists(storage_path):
        context.browser_context = context.browser.new_context(storage_state=storage_path)
    else:
        context.browser_context = context.browser.new_context()

    context.page = context.browser_context.new_page()
    context.dositrace_page = DositracePage(context.page)
    context.test_results = []

def before_feature(context, feature):
    pass

def before_scenario(context, scenario):
    context.scenario_name = scenario.name

    if context.page.is_closed():
        context.page = context.browser.new_page()
        context.dositrace_page = DositracePage(context.page)
    context.exams_page = ExamsPage(context.page)
    context.alerts_page = AlertsPage(context.page)
    context.login_page = LoginPage(context.page)
    context.nrd_nri_page = NrdNriPage(context.page)
    context.patients_page = PatientsPage(context.page)
    context.protocoles_dositrace_page = ProtocolesDositracePage(context.page)
    context.rapport_page = RapportPage(context.page)
    context.risk_patient_page = RiskPatientPage(context.page)
    context.statistique_page = StatistiquePage(context.page)
    context.worklist_page = WorklistPage(context.page)

def before_step(context, step):
    pass

def after_step(context, step):
    if step.status.name == "failed":
        context.failed_message = str(step.exception)
    else:
        context.failed_message = ""

def after_scenario(context, scenario):
    result = {
        "name": scenario.name,
        "tags": scenario.tags,
        "status": scenario.status.name,
        "timestamp": datetime.datetime.now().isoformat(),
        "message": context.failed_message if hasattr(context, 'failed_message') else ""
    }
    context.test_results.append(result)

    context.failed_message = ""

    if "login" in scenario.tags and hasattr(context, "login_page"):
        try:
            if not context.page.is_closed():
                context.dositrace_page.save_storage()
        except Exception as e:
            print(f" Error saving session: {e}")

def after_feature(context, feature):
    storage_path = "session.json"
    if os.path.exists(storage_path):
        try:
            os.remove(storage_path)
            print(f"{storage_path} removed after feature '{feature.name}'")
        except Exception as e:
            print(f"Failed to remove {storage_path} after feature '{feature.name}': {e}")

def after_all(context):
    if hasattr(context, "browser") and context.browser:
        try:
            context.browser.close()
        except Exception as e:
            print(f" Browser close() failed: {e}")

    excel_path = "/Users/ranaabidi/Desktop/Testing.xlsx"
    update_excel_with_results(context.test_results, excel_path)
