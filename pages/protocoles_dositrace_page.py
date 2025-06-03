from playwright.sync_api import Page

from playwright.sync_api import expect

from urllib.parse import urljoin

import json

import unicodedata

import fnmatch

import time

import re

import os

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class ProtocolesDositracePage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def click_angiographie_first_row(self):
        self.page.evaluate("document.getElementById('accordionSidebar').style.display = 'none'")
        angiographie_link = self.page.locator('#protocolDB tbody tr:first-child td a', has_text="Angiographie")
        angiographie_link.click(force=True)

    def go_to_protocol_db_list_page(self):
        self.page.goto("http://10.0.5.14:8080/DositraceV2-war/ListProtocolDB")
        self.protocoles_dositrace_page = ProtocolesDositracePage(self.page)

    def click_ajouter(self):
        ajouter_button = self.page.locator("a[href='CreateProtocolDB']")
        ajouter_button.evaluate("element => element.click()")

    def creation_page_displayed(self):
        self.page.wait_for_load_state("networkidle")
        form = self.page.locator("form[action*='DoCreateProtocolDB']")
        form.wait_for(state="visible", timeout=5000)
        assert form.is_visible()

    def check_success_message(self):
        self.page.wait_for_selector(".ui-pnotify-text", timeout=5000)
        notif_text = self.page.locator(".ui-pnotify-text").inner_text()
        assert "Données mises à jours avec succès" in notif_text, \
            f"Message attendu non trouvé : {notif_text}"

    def force_delete_protocol(self):
        self.page.locator("input[type='checkbox'].check").first.check()

        self.page.evaluate("window.confirm = () => true")

        self.page.locator("#del").click()

        try:
            self.page.wait_for_selector(".ui-pnotify-text", timeout=5000)
            print("Suppression réussie!")

        except TimeoutError:
            print("Erreur : Le message de succès n'a pas été trouvé dans le délai imparti.")
            assert False, "Suppression échouée ou le message de confirmation n'a pas été affiché à temps"

    def submit_modification(self):
        self.page.locator("input[type='submit'][value='Modifier']").click()
        self.page.wait_for_timeout(2000)

    def fill_edit_fields(self):
        self.page.fill("input[name='dbName']", "Nouveau Classeur Test")
        self.page.select_option("select[name='modality']", value="31")

    def select_protocol_to_delete(self):
        checkbox = self.page.locator("input[type='checkbox'].check").first
        checkbox.check()
        del_button = self.page.locator("#del")
        del_button.wait_for(state="attached")
        btn_handle = del_button.element_handle()
        self.page.wait_for_function("el => !el.disabled", arg=btn_handle)

    def select_protocol_to_edit(self):
        checkbox = self.page.locator("input[type='checkbox'].check").first
        checkbox.check()

    def click_modify_button(self):
        edit_button =self.page.locator("#edit")
        edit_button.wait_for(state="attached")
        btn_handle = edit_button.element_handle()
        self.page.wait_for_function("el => !el.disabled", arg=btn_handle)
        edit_button.click()

    def verify_protocol_duplicated(self):
        self.page.wait_for_selector("div.dataTables_info", timeout=10000)
        info_text = self.page.locator("div.dataTables_info").inner_text()
        match = re.search(r"sur\s+(\d+)\s+élément", info_text)
        assert match, f"Impossible de lire le nombre initial : {info_text}"
        self.initial_count = int(match.group(1))

        self.page.locator("input[type='checkbox'].check").first.check()

        duplicate_btn = self.page.locator("#duplicate")
        duplicate_btn.wait_for(state="attached")
        button_handle = duplicate_btn.element_handle()
        self.page.wait_for_function("el => !el.disabled", arg=button_handle)

        duplicate_btn.click()

        self.page.wait_for_timeout(2000)

    def click_duplicate(self):
        self.page.locator("a#duplicate").click()

    def select_protocol(self):
        checkbox = self.page.locator("input.check[type='checkbox']").first
        checkbox.check()
        duplicate_button = self.page.locator("a#duplicate")
        expect(duplicate_button).to_be_enabled()

    def count_protocols(self):
        self.page.wait_for_selector("div.dataTables_info", timeout=10000)
        info_text = self.page.locator("div.dataTables_info").inner_text()
        match = re.search(r"sur\s+(\d+)\s+élément", info_text)
        assert match, f"Le texte d'information n'a pas été trouvé : {info_text}"
        self.initial_count = int(match.group(1))

    def click_first_protocol(self):
        first_link = self.page.locator("#protocolDB tbody a.btn-link").first
        first_link.click()

    def click_retour(self):
        self.page.locator("a.btn.btn-secondary[href='ListProtocolDB']").click()

        self.page.wait_for_url("**/ListProtocolDB", timeout=5000)
        assert "ListProtocolDB" in self.page.url, "La redirection vers ListProtocolDB a échoué"

    def go_to_create_protocol_page(self):
        self.page.goto("http://10.0.5.14:8080/DositraceV2-war/CreateProtocolDB")
        self.protocoles_dositrace_page = ProtocolesDositracePage(self.page)

    def success_message_displayed(self):
        self.page.wait_for_selector(".ui-pnotify-text", timeout=5000)
        message = self.page.locator(".ui-pnotify-text").inner_text()
        assert "Le classeur de protocole a été créé avec succès" in message
        print(" Protocole créé avec succès.")

    def click_valider_button(self):
        self.page.click("input[type='submit'].btn.btn-primary")

    def verify_modality(self):
        options = self.page.locator("#modality option").all()
        assert len(options) == 10, f"Il y a {len(options)} modalités, au lieu de 10 attendues."

    def fill_protocol_name(self, nom):
        self.page.fill("#db-name", nom)

    def select_modality_option(self, modality):
        self.page.select_option("#modality", label=modality)

    def go_to_list_protocol_to_export(self):
        self.page.goto("http://10.0.5.14:8080/DositraceV2-war/ListProtocolToExport")
        self.protocoles_dositrace_page = ProtocolesDositracePage(self.page)
