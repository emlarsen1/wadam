# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 02:08:52 2023

@author: Mark Larsen
"""


class Locators():

    # Login page objects
    username_textbox_xpath = '//*[@id="user_name_field"]'
    username_button_xpath = '//*[@id="user_name_btn"]'
    password_textbox_xpath = '//*[@id="password_field"]'
    password_button_xpath = '//*[@id="password_btn"]'
    pincode_textbox_xpath = '//*[@id="password_field"]'
    pincode_button_xpath = '//*[@id="password_btn"]'
    amazonlogin_button_xpath = '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/form/div/input'
    austin_login_url = "https://na.ehs-amazon.com/waste-and-donations/search"

    # Austin page objects
    asin_location_xpath = "/html/body/div/div/div/div/div/div/div[3]/div/div[3]/div/div[1]/table/tbody/tr/td/div/div/div/div/div[1]/div/p"
    asin_location_CSSSel = ".css-17zd7ui-cardHeader > div:nth-child(1) > p:nth-child(1)"
    asin_regulated_xpath = "/html/body/div/div/div/div/div/div/div[3]/div/div[3]/div/div[1]/table/tbody/tr/td/div/div/div/div/div[2]/div[2]/div/div[6]/div/div/div[2]/p"
    asin_not_found_CSSSel = "p.MuiTypography-root:nth-child(2) > span:nth-child(1)"
    asin_category_xpath = "/html/body/div/div/div/div/div/div/div[3]/div/div[3]/div/div[1]/table/tbody/tr/td/div/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div[14]/p"
    container_found_CSSSel = "h6.MuiTypography-root"
    container_empty_CSSSel = ".css-12m1n6b-emptyToteText"
    container_input_CSSSel = "#toteId"
    asin_input_CSSSel = "#productId"
    item_inspector_CSSSel = ".core-1vr549o-navIconButton > svg:nth-child(1)"

    # PanDash page Objects
    url = 'https://pandash.amazon.com/index.jsp'
    location_button_xpath = '//*[@id="us"]'
    sourcefilter_dropdown_id = 'sourceFilter'
    sourceFilter_option_text = 'FC'
    siteid_textbox_xpath = '//*[@id="FCinput"]'
    siteid_value_text = 'DEN2'
    asinsFilter_textbox_id = 'asinsFilter'
    search_button_id = 'btOk'

    # CSI page objects
    csiURL = 'https://csi.amazon.com/view?view=blame_o&marketplace_id=1&customer_id=&merchant_id=&sku=&fn_sku=&gcid=&fulfillment_channel_code=&listing_type=purchasable&submission_id=&order_id=&external_id=&search_string={self.tabName}&realm=USAmazon&stage=prod&domain_id=&keyword=&submit=Show'
    csiSearchURL = "f'https://csi.amazon.com/view?view=blame_o&item_id={ASIN}&marketplace_id=1&customer_id=&merchant_id=&sku=&fn_sku=&gcid=&fulfillment_channel_code=&listing_type=purchasable&submission_id=&order_id=&external_id=&search_string={self.tabName}&realm=USAmazon&stage=prod&domain_id=&keyword=&submit=Show'"
    prohibitedWords = ['recalled', 'prohibited', 'yanked',
                       'restricted', 'recall', 'reject', 'rejected', 'shadow']

    # FCR page objects
    fcrLoginUrl = 'https://fcmenu-iad-regionalized.corp.amazon.com/secure/login'
    userbadge_textbox_xpath = '//*[@id="badgeBarcodeId"]'
    userpass_textbox_xpath = '//*[@id="password"]'
    fcr_app_menu_text_CSSSel = '#selectionGuidance'
    fcr_problem_solve_button_xpath = '/html/body/div[3]/div/div[2]/ul[2]/li[5]/a'
    fcr_FCResearch_button_xpath = '/html/body/div[3]/div/div[2]/ul[1]/li[4]/a'
    fcr_FBATable_ASIN_text_CSSSel = '#table-sscc-info > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)'
    fcr_LPNTable_ASIN_text_CSSSel = '#table-inventory-history_info'

    # Delete Items App
    delUrl = 'https://fcmenu-iad-regionalized.corp.amazon.com/secure/login'
    delBadgeID_textbox_CSSSel = '#badgeBarcodeId'
    delPassword_textbox_CSSSel = '#password'
    delProblemSolve_menu_CSSSel = 'div.choices:nth-child(2) > ul:nth-child(2) > li:nth-child(5) > a:nth-child(1)'
    delDeleteItems_menu_CSSSel = 'div.choices:nth-child(2) > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)'
    delDeleteContainer_textbox_CSSSel = '.a-input-text-wrapper > input:nth-child(1)'
    delDeletionMode_text_CSSSel = 'dd.a-list-item'
    delContainerMode_radio_CSSSel = '.a-box:nth-child(2) .a-icon'
    delSingleMode_radio_CSSSel = '.a-box:nth-child(1) .a-icon'
    delAlertMsg_text_CSSSel = '.a-alert-content'
    delInlineAlertMsg_text_Class_Name = "a-alert-inline"
    delAlertHeaderRegulated_text_Class_Name = "a-alert-warning"
    delItemList_radio_Class_Name = 'a-icon-radio'
    delUserMenu_linktext_CSSSel = 'User menu (m)'
    delEnter_button_CSSSel = '.a-button-input'
    delChangeContainer_Button_CSSSel = "#a-autoid-2 > span:nth-child(1) > input:nth-child(1)"
    delDamagedAndUnreturnable_radio_CSSSel = "div.a-box:nth-child(3) > div:nth-child(1) > div:nth-child(1) > label:nth-child(1) > i:nth-child(2)"
    delHeaderMessage_text_CSSSel = ".aft-tool-action-box > div:nth-child(1) > h1:nth-child(1)"
    delConfirmDeletion_button_xpath = "/html/body/div[1]/div[4]/div/div[2]/div[1]/form/span[1]/span/span/input"
    delItemList_radio_xpath = "//*[@type='radio']"
    delServiceFail_text_CSSSel = "#workspace > div:nth-child(1) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > h1:nth-child(1)"
    delServiceFail_text_xpath = "/html/body/div[1]/div[4]/div/div[2]/div[5]/div/div/h1"
    delHeaderMessage_text_CSSSelector = "div.a-span8"

    # Denali App
    denaliUrl = "https://prod.na.denali.scot.amazon.dev/deep-dive"
    denaliEntry_Text_XPATH = "/html/body/div/div/div/div/div[1]/div/div/div[1]/div[2]/label/input"
    denaliSubmit_button_CSSSel = ".button"
