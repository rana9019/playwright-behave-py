from playwright.sync_api import Page

from playwright.sync_api import expect

from dotenv import load_dotenv

import json

import unicodedata

import re

import os

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

class StatistiquePage:
    def __init__(self, page: Page):
        self.page = page
        self.block_images()
        self.storage_path = "session.json"

    def block_images(self):
        self.page.context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

    def chart1_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/Chart1")

    def chart3_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/Chart3")

    def chart4_url(self):
        self.page.goto(f"http://10.0.5.14:8080/DositraceV2-war/Chart4")