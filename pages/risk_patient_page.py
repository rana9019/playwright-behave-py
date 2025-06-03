from playwright.sync_api import Page

from playwright.sync_api import expect

from dotenv import load_dotenv

import json

import unicodedata

import re

import os

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class RiskPatientPage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def risk_patient_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/RiskPatient")

    def fill_filters(self):
        self.page.select_option("#modality", "7")
        self.page.select_option("#equi", "25")
        self.page.select_option("#followup", "1")
        self.page.select_option("#realization", "1")
        self.page.select_option("#patientRisk", "2")

    def verify_filters_reset(self):
        expect(self.page.locator("#modality")).to_have_value("")
        expect(self.page.locator("#equi")).to_have_value("")
        expect(self.page.locator("#followup")).to_have_value("")
        expect(self.page.locator("#realization")).to_have_value("")
        expect(self.page.locator("#patientRisk")).to_have_value("")

    def click_oui_in_suivi_necesaire(self):
        oui_button = self.page.locator('input[name="monitoring-185637"][value="true"]').first
        oui_button.click()

    def verify_table_filtered_by_oui(self):
        rows = self.page.locator("table tbody tr")
        count = rows.count()
        assert count > 0, "Le tableau ne contient aucune ligne."

        for i in range(count):
            row = rows.nth(i)
            radio_oui = row.locator("input[type='radio'][value='true']")
            assert radio_oui.is_checked(), f"Ligne {i+1} n'est pas filtrée avec 'OUI'."

    def select_oui_filter(self):
        self.page.locator("#s2id_realization").click()
        self.page.locator("li.select2-result-selectable", has_text="Oui").click()

    def get_table_header(self, page, table_number):
        locator = page.locator(f"table:nth-of-type({table_number}) thead th")
        headers = [
            locator.nth(i).inner_text().strip().replace("\n", " ")
            for i in range(locator.count())
            if locator.nth(i).inner_text().strip()
        ]
        return headers

    def verify_last_suivi_statut(self):
        rows = self.page.locator("tbody.text-center tr")
        count = rows.count()
        assert count > 0, "Le tableau est vide ou non chargé"

        for i in reversed(range(count)):
            row = rows.nth(i)
            row_text = row.inner_text().strip()
            if "Aucune donnée disponible" in row_text:
                continue

            status_cell = row.locator("td").last
            status_text = status_cell.inner_text().strip()
            print(f"Statut de la dernière ligne : {status_text}")

            expected_statuses = [
                "Suivi réalisé",
                "Suivi non réalisé",
                "Suivi non demandé"
            ]

            assert any(s in status_text for s in expected_statuses), "Statut inattendu"
            break

    def suivi_non_realise_red(self):
        suivi_badge = self.page.locator('.badge', has_text="Suivi non réalisé").nth(0)
        suivi_badge.wait_for(state="visible", timeout=10000)

        assert suivi_badge.is_visible(), "Suivi non réalisé is not visible"
        badge_class = suivi_badge.get_attribute("class")
        assert "badge-danger" in badge_class, f"Expected red badge, got class='{badge_class}'"

    def button_activated(self):
        print("Waiting for any visible element with class 'icon-list-unCheck'...")

        locator = self.page.locator('a.icon-list-unCheck')
        count = locator.count()

        for i in range(count):
            element = locator.nth(i)
            if element.is_visible():
                print(f" Found visible element with data-id={element.get_attribute('data-id')}")
                return

        raise Exception(" No visible element found.")

    def click_follow_up_button(self):
        button = self.page.locator("a[data-id='185641']").nth(1)
        button.click()

    def popup_appears(self):
        expect(self.page.locator("div.modal-dialog")).to_be_visible()
        expect(self.page.locator("input#monitoringDone")).to_be_visible()
        expect(self.page.locator("textarea#commentaire")).to_be_visible()
        expect(self.page.locator("button.btn-secondary")).to_be_visible()
        expect(self.page.locator("button.btn-primary")).to_be_visible()

    def check_follow_up_checkbox(self):
        checkbox = self.page.locator("input#monitoringDone")
        checkbox.check()

    def fill_comment(self):
        comment_area = self.page.locator("textarea#commentaire")
        comment_area.fill("Commentaire de suivi")

    def click_save_button(self):
        save_button = self.page.locator("button[type='submit']")
        save_button.click()

    def check_suivi_status(self):
        status_locator = self.page.locator('a[data-id="185641"][data-done="true"]').first

        assert status_locator.is_visible(), "Status 'Suivi réalisé' is not visible"

        color = status_locator.evaluate('el => window.getComputedStyle(el).color')
        expected_color = "rgb(70, 128, 255)"
        assert expected_color in color, f"Status color is not green, it is {color}"

    def page_reload_with_filters(self):
        self.page.wait_for_load_state('load')

    def click_non_in_suivi_necesaire(self):
        non_button = self.page.locator('input[name="monitoring-185637"][value="false"]').first
        non_button.wait_for(state="visible", timeout=5000)
        non_button.click()

    def click_non_in_suivi_necessary(self):
        non_button = self.page.locator('input[name="monitoring-185641"][value="true"]').first
        non_button.wait_for(state="visible", timeout=5000)
        non_button.click()

    def status_is_no_follow_up(self):
        try:
            suivi_badge = self.page.locator('.badge', has_text="Suivi non nécessaire").nth(0)

            suivi_badge.wait_for(state="visible", timeout=10000)

            assert suivi_badge.is_visible(), "'Suivi non nécessaire' badge is not visible"

            badge_class = suivi_badge.get_attribute("class")

            assert "badge-secondary" in badge_class, f"Expected 'badge-secondary', got class='{badge_class}'"

            background_color = suivi_badge.get_attribute("style")
            assert "background-color: gray" in background_color, f"Expected gray background, got '{background_color}'"

            print(" Suivi non nécessaire badge is correct")

        except Exception as e:
            print(" Erreur dans check_suivi_non_nécessaire :", str(e))
            self.page.screenshot(path="screenshot_suivi_non_nécessaire_error.png", full_page=True)
            raise

    def is_column_empty(self, row_locator):
        column_14 = row_locator.locator('td:nth-of-type(14)')

        column_14.wait_for(state='visible', timeout=5000)

        if column_14.inner_text().strip() == "":
            return True
        else:
            return False

    def follow_up_button_is_inactive(self):
        row = self.page.locator('table#exam tr:nth-child(2)')

        row.wait_for(state='visible', timeout=5000)

        is_empty = self.is_column_empty(row)
        if is_empty:
            print("La colonne 14 est vide.")
        else:
            print("La colonne 14 contient des données.")

    def verify_tooltip_matches_status(self, page):
        first_row = page.locator("table tbody tr").first

        status_locator = first_row.locator("div.badge")
        status_locator.wait_for(state='visible', timeout=5000)
        status_text = status_locator.inner_text().strip()

        tooltip_icon = first_row.locator(f"span.tooltips[data-original-title='{status_text}']")
        tooltip_icon.hover()

        tooltip_text = tooltip_icon.get_attribute("data-original-title").strip()
        print(f"Tooltip text: {tooltip_text}")

        assert tooltip_text == status_text, f"Expected tooltip to be '{status_text}', but got '{tooltip_text}'"
