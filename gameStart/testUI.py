# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

def canRunThisTest():
    try:
        webdriver.Firefox()
        return True
    except:
        return False

@unittest.skipUnless(canRunThisTest(), 'No Firefox webdriver')
class TestUI(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://combating-snake.herokuapp.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test1_home_button(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("li.active").click()
        # test for making sure SIGN IN panel shown on page after clicking HOME button
        try: self.assertTrue(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-login").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        #test for making sure other panels not displayed
        try: self.assertFalse(driver.find_element_by_css_selector("section.leaderboard.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertFalse(driver.find_element_by_css_selector("section.intro.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertFalse(driver.find_element_by_css_selector("section.gamerule.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # input user name and password
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("snake2")
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("1234")
        driver.find_element_by_css_selector("input.submit-login").click()

        # test for making sure the room creation panel shown on page after log in
        for i in range(60):
            try:
                if driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(driver.find_element_by_css_selector("input.create_button").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-roomjoin").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("li.active").click()

        # test for making sure the room creattion panel shown on page after clicking HOME button
        try: self.assertTrue(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(driver.find_element_by_css_selector("input.create_button").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-roomjoin").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure other panels not displayed
        try: self.assertFalse(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertFalse(driver.find_element_by_css_selector("section.leaderboard.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertFalse(driver.find_element_by_css_selector("section.intro.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertFalse(driver.find_element_by_css_selector("section.gamerule.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # # ERROR: Caught exception [Error: locator strategy either id or name must be specified explicitly.]


    def test2_gamerules_leaderboard_credits_button(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        # check for game rules button works
        driver.find_element_by_css_selector("li.rule-button").click()
        # test for making sure gamerules displayed
        try: self.assertTrue(driver.find_element_by_css_selector("section.gamerule.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure SIGN IN panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure room creation panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure leaderboard panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.leaderboard.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure designers panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.intro.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # check for leaderboard button works
        driver.find_element_by_css_selector("li.leader-button").click()
        # test for making sure the leaderboard panel is displayed
        try: self.assertTrue(driver.find_element_by_css_selector("section.leaderboard.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the "SIGN IN" panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the room creation panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the designers panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.intro.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the game rules panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.gamerule.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # check for CREDITS button works
        driver.find_element_by_css_selector("li.intro-button").click()
        # test for making sure the designers panel is displayed
        try: self.assertTrue(driver.find_element_by_css_selector("section.intro.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the "SIGN IN" button is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the room creation panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the leaderboard panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.leaderboard.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the gamerules panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.gamerule.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))


    def test3_signup_with_user_name_already_exist(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign up now").click()
        driver.find_element_by_id("signup_username").clear()
        driver.find_element_by_id("signup_username").send_keys("snake2")
        driver.find_element_by_id("signup_nickname").clear()
        driver.find_element_by_id("signup_nickname").send_keys("snake2")
        driver.find_element_by_id("signup_password").clear()
        driver.find_element_by_id("signup_password").send_keys("1111")
        driver.find_element_by_id("signup_password_retype").clear()
        driver.find_element_by_id("signup_password_retype").send_keys("1111")
        driver.find_element_by_css_selector("input.submit-signup").click()

        # test for making sure if the sign up container still on the page
        try: self.assertTrue(driver.find_element_by_css_selector("div.signup_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        # test for makign sure if the correct error message shown
        for i in range(60):
            try:
                if "Internal Server Error IntegrityError: duplicate key value violates unique constraint \"gameStart_user_username_key\" DETAIL: Key (username)=(snake2) already exists." == driver.find_element_by_css_selector("div.signup_error").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Internal Server Error IntegrityError: duplicate key value violates unique constraint \"gameStart_user_username_key\" DETAIL: Key (username)=(snake2) already exists.", driver.find_element_by_css_selector("div.signup_error").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure if the signup_error shown
        try: self.assertTrue(driver.find_element_by_css_selector("div.signup_error").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure if the "SIGN UP" button still on the page
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-signup").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))


    def test4_signup_password_and_retypepassword_not_match(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign up now").click()
        driver.find_element_by_id("signup_username").clear()
        driver.find_element_by_id("signup_username").send_keys("snake")
        driver.find_element_by_id("signup_nickname").clear()
        driver.find_element_by_id("signup_nickname").send_keys("snake")
        driver.find_element_by_id("signup_password").clear()
        driver.find_element_by_id("signup_password").send_keys("1111")
        driver.find_element_by_id("signup_password_retype").clear()
        driver.find_element_by_id("signup_password_retype").send_keys("1112")
        driver.find_element_by_css_selector("input.submit-signup").click()
        # test for making sure if the sign up container is still on the page
        try: self.assertTrue(driver.find_element_by_css_selector("div.signup_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure if the signup_error shown
        for i in range(60):
            try:
                if "Password does not match." == driver.find_element_by_css_selector("div.signup_error").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Password does not match.", driver.find_element_by_css_selector("div.signup_error").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(driver.find_element_by_css_selector( "div.signup_error").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure if the "SIGN UP" button is still on the page
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.submit-signup"))
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test5_signup_password_too_short(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign up now").click()
        driver.find_element_by_id("signup_username").clear()
        driver.find_element_by_id("signup_username").send_keys("aaaa")
        driver.find_element_by_id("signup_nickname").clear()
        driver.find_element_by_id("signup_nickname").send_keys("aaaa")
        driver.find_element_by_id("signup_password").clear()
        driver.find_element_by_id("signup_password").send_keys("11")
        driver.find_element_by_id("signup_password_retype").clear()
        driver.find_element_by_id("signup_password_retype").send_keys("11")
        driver.find_element_by_css_selector("input.submit-signup").click()
        # test for making sure the "SIGN IN" pannel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the "SIGN UP" pannel shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-signup").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "Password is not valid: must be at least 4 characters" == driver.find_element_by_css_selector("div.signup_error").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

        # test for making sure the correct error message shown
        try: self.assertEqual("Password is not valid: must be at least 4 characters", driver.find_element_by_css_selector("div.signup_error").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test6_signup_username_too_short(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign up now").click()
        driver.find_element_by_id("signup_username").clear()
        driver.find_element_by_id("signup_username").send_keys("aaaa")
        driver.find_element_by_id("signup_nickname").clear()
        driver.find_element_by_id("signup_nickname").send_keys("aaaa")
        driver.find_element_by_id("signup_nickname").clear()
        driver.find_element_by_id("signup_nickname").send_keys("aa")
        driver.find_element_by_id("signup_username").clear()
        driver.find_element_by_id("signup_username").send_keys("aa")
        driver.find_element_by_id("signup_password").clear()
        driver.find_element_by_id("signup_password").send_keys("1111")
        driver.find_element_by_id("signup_password_retype").clear()
        driver.find_element_by_id("signup_password_retype").send_keys("1111")
        driver.find_element_by_css_selector("input.submit-signup").click()
        # test for making sure the "SIGN UP" button shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-signup").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "Username is not valid: aa must be from 4 to 64 alphanumeric characters" == driver.find_element_by_css_selector("div.signup_error").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

        # test for making sure the correct error message shown
        try: self.assertEqual("Username is not valid: aa must be from 4 to 64 alphanumeric characters", driver.find_element_by_css_selector("div.signup_error").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test7_signup_user_name_too_long(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign up now").click()
        driver.find_element_by_id("signup_username").clear()
        driver.find_element_by_id("signup_username").send_keys("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        driver.find_element_by_id("signup_nickname").clear()
        driver.find_element_by_id("signup_nickname").send_keys("aa")
        driver.find_element_by_id("signup_password").clear()
        driver.find_element_by_id("signup_password").send_keys("11111")
        driver.find_element_by_id("signup_password_retype").clear()
        driver.find_element_by_id("signup_password_retype").send_keys("11111")
        driver.find_element_by_css_selector("input.submit-signup").click()
        # test for making sure the "SIGN UP" button shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-signup").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the signup_container shown
        try: self.assertTrue(driver.find_element_by_css_selector("div.signup_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the correct error message shown
        for i in range(60):
            try:
                if "Username is not valid: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa must be from 4 to 64 alphanumeric characters" == driver.find_element_by_css_selector("div.signup_error").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Username is not valid: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa must be from 4 to 64 alphanumeric characters", driver.find_element_by_css_selector("div.signup_error").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the singup_error shown
        try: self.assertTrue(driver.find_element_by_css_selector("div.signup_error").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test8_login_user_name_not_exist(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("snakeeeee")
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("1111")
        driver.find_element_by_css_selector("input.submit-login").click()
        # test for making sure the "SIGN IN" button shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-login").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the correct error message shown
        for i in range(60):
            try:
                if "Username is not valid: cannot find user snakeeeee" == driver.find_element_by_css_selector("div.login_error").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Username is not valid: cannot find user snakeeeee", driver.find_element_by_css_selector("div.login_error").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the login_error shown
        try: self.assertTrue(driver.find_element_by_css_selector("div.login_error").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test9_login_incorrect_password(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("snake2")
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("123")
        driver.find_element_by_css_selector("input.submit-login").click()
        # test for making sure the login_error shown
        for i in range(60):
            try:
                if "Incorrect password" == driver.find_element_by_css_selector("div.login_error").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(driver.find_element_by_css_selector("div.login_error").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Incorrect password", driver.find_element_by_css_selector("div.login_error").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the "SIGN IN" button shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-login").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test10_correct_password(self):
        driver = self.driver
        driver.get(self.base_url + "/") # open new window on Firefox,
        driver.find_element_by_id("login_username").clear() # clear text field for username
        driver.find_element_by_id("login_username").send_keys("snake2") # enter text
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("1234")
        driver.find_element_by_css_selector("input.submit-login").click()
        self.assertEqual("Create a Room", driver.find_element_by_css_selector("input.create_button").get_attribute("value"))
        try: self.assertEqual("Join a Random Room", driver.find_element_by_css_selector("input.submit-roomjoin").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the login_container is hidden
        for i in range(60):
            try:
                if not driver.find_element_by_css_selector("div.login_container.form_container").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertFalse(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the "CREATE A ROOM" button shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.create_button").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the "JOIN A RANDOM ROOM" butoon shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.submit-roomjoin").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the "PICK A ROOM" butoon shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.join_specific_room").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the "LOG OUT" button shown
        try: self.assertTrue(driver.find_element_by_css_selector("input.logout.generic-button").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the welcome message shown
        for i in range(60):
            try:
                if "Welcome, snake2 !" == driver.find_element_by_css_selector("div.usernameInfo").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Welcome, snake2 !", driver.find_element_by_css_selector("div.usernameInfo").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertTrue(driver.find_element_by_css_selector("div.usernameInfo").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the navigation bar still shown
        try: self.assertTrue(driver.find_element_by_css_selector("#cssmenu").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # user clicked on logout
        driver.find_element_by_css_selector("input.logout.generic-button").click()

    def test11_logout(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("snake2")
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("1234")
        driver.find_element_by_css_selector("input.submit-login").click()
        driver.find_element_by_css_selector("input.logout.generic-button").click()
        # test for making sure the login_container shown
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.login_container.form_container"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the "SIGN IN" button shown
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.submit-login"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the navigation bar still shown
        try: self.assertTrue(self.is_element_present(By.ID, "cssmenu"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # # test for making sure room creation panel is hidden
        # try: self.assertFalse(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        # except AssertionError as e: self.verificationErrors.append(str(e))
        # # test for making sure if the sign up container is hidden
        # try: self.assertFalse(self.is_element_present(By.CSS_SELECTOR, "div.signup_container.form_container"))
        # except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the designers panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.intro.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the game rules panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.gamerule.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure leaderboard panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.leaderboard.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test12_room_page_show_after_click_on_create_room(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("snake2")
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("1234")
        driver.find_element_by_css_selector("input.submit-login").click()
        driver.find_element_by_css_selector("input.create_button").click()

        # test for making sure the cssmenu hidden
        for i in range(60):
            try:
                if not driver.find_element_by_id("cssmenu").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertFalse(driver.find_element_by_id("cssmenu").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the "SIGN IN" panel hidden
        for i in range(60):
            try:
                if not driver.find_element_by_css_selector("div.login_container.form_container").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertFalse(driver.find_element_by_css_selector("div.login_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the "SIGN UP" panel hidden
        for i in range(60):
            try:
                if not driver.find_element_by_css_selector("div.signup_container.form_container").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertFalse(driver.find_element_by_css_selector("div.signup_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the room creation panel hidden
        for i in range(60):
            try:
                if not driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertFalse(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the player element present
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "div.player.red"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.player.red"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the player name displayed is "snake2"
        for i in range(60):
            try:
                if "snake2" == driver.find_element_by_css_selector("div.name").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("snake2", driver.find_element_by_css_selector("div.name").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the player icon shown
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "img.snake_icon"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img.snake_icon"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the "LEAVE ROOM" button shown
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.submit-leave"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the "START GAME" button shown
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.submit-start"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the health field shown
        for i in range(60):
            try:
                if "10" == driver.find_element_by_css_selector("div.health").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("10", driver.find_element_by_css_selector("div.health").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the room_id shown
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "div.room_id"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.room_id"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the gameboard shown
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.gameboard"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the welcome message still show on the screen
        try: self.assertEqual("Welcome, snake2 !", driver.find_element_by_css_selector("div.usernameInfo").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

        driver.find_element_by_css_selector("input.submit-leave").click()

    def test14_leaveroom_button_click(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("snake2")
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("1234")
        driver.find_element_by_css_selector("input.submit-login").click()
        driver.find_element_by_css_selector("input.create_button").click()
        driver.find_element_by_css_selector("input.submit-leave").click()
        # test for making sure the room creation panel hidden
        for i in range(60):
            try:
                if not driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertFalse(driver.find_element_by_css_selector("div.roomcreate_container.form_container").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | null | ]]

        # test for logout button still on the page
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.logout.generic-button"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for "JOIN A RANDOM ROOM" button shown
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "input.submit-roomjoin"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.logout.generic-button"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for welcome message shown
        for i in range(60):
            try:
                if "Welcome, snake2 !" == driver.find_element_by_css_selector("div.usernameInfo").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Welcome, snake2 !", driver.find_element_by_css_selector("div.usernameInfo").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the cssmenu shown
        try: self.assertTrue(self.is_element_present(By.ID, "cssmenu"))
        except AssertionError as e: self.verificationErrors.append(str(e))

        # test for making sure the designers panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.intro.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the game rules panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.gamerule.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure leaderboard panel is hidden
        try: self.assertFalse(driver.find_element_by_css_selector("section.leaderboard.frame").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))

    def test_click_on_pick_a_room_button(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("snake2")
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys("1234")
        driver.find_element_by_css_selector("input.submit-login").click()
        driver.find_element_by_css_selector("input.join_specific_room").click()
        # test for making sure the room list is present
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.pick_room"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the REFRESH ROOM button is present
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.refresh_rooms"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making the CANCEL button is present
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "input.cancel_room_pick"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        # user clicked on CANCEL button
        driver.find_element_by_css_selector("input.cancel_room_pick").click()
        # test for making sure the room list page is hidden
        for i in range(60):
            try:
                if not driver.find_element_by_css_selector("div.pick_room").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertFalse(driver.find_element_by_css_selector("div.pick_room").is_displayed())
        except AssertionError as e: self.verificationErrors.append(str(e))
        # test for making sure the creatroom panel is shown
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "div.roomcreate_container.form_container"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.roomcreate_container.form_container"))
        except AssertionError as e: self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
