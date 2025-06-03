from playwright.sync_api import Page

from playwright.sync_api import expect

from dotenv import load_dotenv

import unicodedata

import time

import os

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class WorklistPage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def worklist_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/Worklist")

    def click_examens_du_jour(self):
        page: Page = self.page

        examens_du_jour = page.locator("input[id='switch_left']")
        expect(examens_du_jour).to_be_visible(timeout=5000)

        examens_du_jour.scroll_into_view_if_needed()
        examens_du_jour.click(force=True)

        print(" Clic sur 'Examens du jour' effectué.")

    def verify_examens_du_jour_active(self):
        page: Page = self.page

        radio_button = page.locator("input[id='switch_left']")
        expect(radio_button).to_be_checked()

        print(" L'onglet 'Examens du jour' est bien activé.")

    def click_examens_7_jours(self):
        page: Page = self.page

        examens_7_jours = page.locator("input[id='switch_right']")
        expect(examens_7_jours).to_be_visible(timeout=5000)

        examens_7_jours.scroll_into_view_if_needed()
        examens_7_jours.click(force=True)

        print(" Clic sur 'Examens à 7 jours' effectué.")

    def verify_examens_7_jours_active(self):
        page: Page = self.page

        radio_button = page.locator("input[id='switch_right']")
        expect(radio_button).to_be_checked()

        print(" L'onglet 'Examens à 7 jours' est bien activé.")

    def click_champ_equipement(self):
        page = self.page
        champ_equipement = page.locator("#s2id_equi")
        champ_equipement.click()
        print(" Clic sur le champ 'Equipement' effectué.")

    def click_ajouter_filtres(self):
        page: Page = self.page

        bouton_ajouter = page.locator("a#addButton")
        expect(bouton_ajouter).to_be_visible(timeout=5000)

        bouton_ajouter.click(force=True)
        print(" Clic sur 'Ajouter des filtres' effectué.")

    def verify_filtres_section(self):
        page: Page = self.page

        section_filtres = page.locator("nav#page-rightbar")
        expect(section_filtres).to_be_visible(timeout=5000)

        print(" La section des filtres avancés est bien affichée.")

    def verify_filtres_uf_equipement(self):
        page: Page = self.page

        filtre_uf = page.locator("label[for='s2id_autogen2']")
        expect(filtre_uf).to_be_visible(timeout=5000)

        filtre_equipement = page.locator("label[for='s2id_autogen3']")
        expect(filtre_equipement).to_be_visible(timeout=5000)

        print(" Les filtres 'UF' et 'Équipement' sont bien affichés.")

    def click_uf(self):
        page: Page = self.page

        champ_uf = page.locator("a.select2-choice")
        expect(champ_uf).to_be_visible(timeout=5000)

        champ_uf.click()
        print(" Clic sur le champ 'UF' effectué.")

    def verify_dropdown_uf(self):
        page = self.page

        dropdown_uf = page.locator("#select2-drop")

        expect(dropdown_uf).to_be_visible(timeout=5000)

        print(" La liste déroulante des UF est bien affichée.")

    def verify_all_uf(self):
        page: Page = self.page

        dropdown_uf = page.locator("#select2-drop")
        expect(dropdown_uf).to_be_visible(timeout=5000)

        option_toutes_uf = page.locator(".select2-results li", has_text="Toutes les UF")

        time.sleep(1)
        expect(option_toutes_uf).to_be_visible(timeout=5000)

        print(" L'option 'Toutes les UF' est bien présente et visible dans la liste.")

    def verify_dropdown_equipement(self):
        page = self.page
        dropdown_equipement = page.locator("div.select2-drop-active")
        expect(dropdown_equipement).to_be_visible(timeout=5000)
        print(" Le menu déroulant des équipements est visible.")

    def verify_equipements_list(self):
        page = self.page

        equipements = page.locator("select#equi option")

        equipements_count = equipements.count()

        print(f" Nombre total d'équipements détectés : {equipements_count}")

        assert equipements_count > 0, "La liste des équipements est vide"

        print(" La liste contient des équipements disponibles.")

