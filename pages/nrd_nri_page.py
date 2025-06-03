from playwright.sync_api import Page

from playwright.sync_api import expect

from dotenv import load_dotenv

import json

import unicodedata

import re

import os

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class NrdNriPage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def calcul_protocole_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/ListNRDProtocolRaw")

    def view_irsn_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/ViewIRSN")

    def list_protocol_national_page_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/ListProtocolNational")

    def select_equipement_filter(self):
        self.page.locator("#s2id_equi").click()

        self.page.wait_for_timeout(1000)

        dropdown = self.page.locator("ul.select2-results li", has_text="AXIOM Iconos R200 C90-C")
        dropdown.wait_for(state="visible", timeout=10000)

        dropdown.click()

    def fill_up_filters(self):
        # Remplace les mauvais IDs par les vrais <select>
        self.page.select_option("#uf", "17")
        self.page.select_option("#equi", "23")
        self.page.select_option("#pediatrique", "true")
        self.page.select_option("#nbexams", "1")

    def verify_filters_are_reset(self):
        expect(self.page.locator("#uf")).to_have_value("")
        expect(self.page.locator("#equi")).to_have_value("")
        expect(self.page.locator("#pediatrique")).to_have_value("")
        expect(self.page.locator("#nbexams")).to_have_value("")

    def go_to_list_nrd_protocol_raw(self):
        self.page.goto("http://10.0.5.14:8080/DositraceV2-war/ListNRDProtocolRaw")
        self.login_page = NrdNriPage(self.page)