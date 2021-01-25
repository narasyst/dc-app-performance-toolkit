import random
import time

from selenium.webdriver.common.by import By
from selenium_ui.jira import modules

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from util.conf import JIRA_SETTINGS




def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_app_custom_action")
    def measure():

        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()


def app_create_dashboard(jira_webdriver, jira_datasets):
    page = BasePage(jira_webdriver)
    @print_timing("selenium_create_board")
    def measure():
        dashboardTitle = f"My Dashboard {time.time()}"
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/Dashboard.jspa")
        # page.wait_until_visible((By.ID,'dash-options'))
        page.get_element((By.XPATH, '//div//a[@href=\'#tools-dropdown-items\']')).click()  # Wait dashboadr list is visible
        page.get_element((By.ID,'create_dashboard')).click()
        page.wait_until_clickable((By.ID, 'edit-entity-dashboard-name')).send_keys(dashboardTitle)
        page.get_element((By.ID,'edit-entity-submit')).click()
    measure()


def app_add_gadget(jira_webdriver, jira_datasets, gadgetId, isLoadMore, isMulti, isHistory):
    page = BasePage(jira_webdriver)
    gadgetPath = f'//div[@class=\'aui-dialog2-content\']//button[contains(@data-item-id,\'performance-objectives-for-jira:{gadgetId}\')]'
    testName = f'selenium_app_add_gadget_{gadgetId}' 
    @print_timing(testName)
    def measure():
        dsName = 'This week'
        PROJECT_KEY = 'TESTAUTO'
        JQL=f'key={PROJECT_KEY}-1'
        NUMBER_OF_ISSUES = 'Number of Issues'

        @print_timing(f'{testName}: add gadget')
        def sub_measure():
            page.get_element((By.ID,'add-gadget')).click()
            if isLoadMore:
                page.wait_until_visible((By.ID,'load-more-directory-items')).click()

            page.wait_until_visible((By.XPATH, gadgetPath)).click()
            page.get_element((By.CSS_SELECTOR, '.aui-dialog2-header  button.aui-close-button')).click()
        sub_measure()

        @print_timing(f'{testName}: init')
        def sub_measure():
            page.wait_until_invisible((By.CSS_SELECTOR, '.aui-dialog2-header'))
            page.driver.switch_to.frame(page.wait_until_visible((By.CSS_SELECTOR,'.dashboard-item-content iframe')))
        sub_measure()

        @print_timing(f'{testName}: configure')
        def sub_measure():
            page.wait_until_clickable((By.ID, 'data-set-name')).send_keys(dsName)
            page.get_element((By.XPATH, '//select[@id=\'predefined-period\']//option[@value=\'thisWeek\']')).click()
            page.get_element((By.XPATH, '(//button[@id=\'expand-2\'])[3]')).click()
            page.wait_until_visible((By.CSS_SELECTOR, '.react-autosuggest__input')).click()
            page.wait_until_clickable((By.CSS_SELECTOR, '.react-autosuggest__input')).send_keys(PROJECT_KEY)
            page.wait_until_visible((By.XPATH,f'//div[@class=\'suggestion-option\']//span[contains(.,\'({PROJECT_KEY})\')]')).click()
            if isHistory:
                page.get_element((By.XPATH, '(//button[@id=\'expand-2\'])[5]')).click()
                page.wait_until_clickable((By.ID,'textarea-jql')).send_keys(JQL)

            page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModalPortal .maui-button-primary')).click()
            page.wait_until_visible((By.CSS_SELECTOR,'.data-set-item-name'))
            if isMulti:
                page.get_element((By.CSS_SELECTOR, '.button-add-metric')).click()
                page.wait_until_visible((By.CSS_SELECTOR, '.react-autosuggest__input')).click()
                page.wait_until_clickable((By.CSS_SELECTOR, '.react-autosuggest__input')).send_keys(NUMBER_OF_ISSUES)
                page.wait_until_visible((By.XPATH, f'//div[@class=\'suggestion-option\']//span[contains(.,\'{NUMBER_OF_ISSUES}\')]')).click()
                page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModalPortal .maui-button-primary')).click()
                page.wait_until_visible((By.CSS_SELECTOR, '.multi-metric-item'))

        sub_measure()

        @print_timing(f'{testName}: save config')
        def sub_measure():
            page.wait_until_visible((By.CSS_SELECTOR,'.maui-button-primary_wide')).click()
            page.wait_until_invisible((By.CSS_SELECTOR,'.maui-button-primary_wide'))
        sub_measure()

        @print_timing(f'{testName}: load chart')
        def sub_measure():
            page.wait_until_visible((By.CSS_SELECTOR,'.chart-footer'))        
        sub_measure()

        @print_timing(f'{testName}: delete gadget')
        def sub_measure():
            page.driver.switch_to.parent_frame()
            page.get_element((By.CSS_SELECTOR, '.gadget-menu button')).click()
            page.wait_until_visible((By.CSS_SELECTOR, '.gadget-menu .dropdown-item .delete')).click()
            page.driver.switch_to.alert.accept()
            page.wait_until_invisible((By.CSS_SELECTOR, '.gadget-container'))
            page.driver.switch_to.default_content()
        sub_measure()
    measure()


def app_add_multi_metric_combined_gadget(jira_webdriver, jira_datasets):
    page = BasePage(jira_webdriver)
    @print_timing("selenium_app_add_multi_metric_combined_gadget")
    def measure():
        page.get_element((By.ID,'add-gadget')).click()
        page.wait_until_visible((By.ID,'load-more-directory-items')).click()
        page.get_element((By.XPATH, '//div[@class=\'aui-dialog2-content\']//button[contains(@data-item-id,\'performance-objectives-for-jira:multi-metric-bar\')]')).click()
        page.get_element((By.CSS_SELECTOR, '.aui-dialog2-header  button.aui-close-button')).click()
        page.wait_until_invisible((By.CSS_SELECTOR, '.aui-dialog2-header'))
    measure()

def app_add_multi_metric_trend_gadget(jira_webdriver, jira_datasets):
    page = BasePage(jira_webdriver)
    @print_timing("selenium_app_add_multi_metric_trend_gadget")
    def measure():
        page.get_element((By.ID,'add-gadget')).click()
        # page.wait_until_visible((By.ID,'load-more-directory-items')).click()
        page.get_element((By.XPATH, '//div[@class=\'aui-dialog2-content\']//button[contains(@data-item-id,\'performance-objectives-for-jira:multi-metric-trend\')]')).click()
        page.get_element((By.CSS_SELECTOR, '.aui-dialog2-header  button.aui-close-button')).click()
        page.wait_until_invisible((By.CSS_SELECTOR, '.aui-dialog2-header'))
    measure()



def app_delete_dashboard(jira_webdriver, jira_datasets):
    page = BasePage(jira_webdriver)
    @print_timing("selenium_delete_board")
    def measure():
        # page.wait_until_visible((By.ID,'dash-options'))
        page.get_element((By.XPATH, '//div//a[@href=\'#tools-dropdown-items\']')).click()  # Wait dashboadr list is visible
        page.get_element((By.ID, 'delete_dashboard')).click()
        page.wait_until_visible((By.ID,'delete-portal-page-submit'))
        page.get_element((By.ID, 'delete-portal-page-submit')).click()
        page.wait_until_invisible((By.ID, 'delete-dshboard'))
    measure()
