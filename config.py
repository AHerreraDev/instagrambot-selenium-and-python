from time import sleep
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class InstagramBot():
    def __init__(self, username: str, password: str, time: int):
        self.browser = webdriver.Chrome("chromedriver")
        self.username = username
        self.password = password
        self.time = time

    def signIn(self):
        LOGIN_URL = "https://www.instagram.com/accounts/login/"
        self.browser.get(LOGIN_URL)
        
        sleep(2)
        login_input = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
        password_input = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
        
        ActionChains(self.browser)\
            .move_to_element(login_input)\
            .click()\
            .send_keys(self.username)\
            .move_to_element(password_input)\
            .click()\
            .send_keys(self.password)\
            .perform()
        
        login_button = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')

        ActionChains(self.browser)\
            .move_to_element(login_button)\
            .click()\
            .perform()
        sleep(5)

        if (self.browser.current_url == LOGIN_URL):
            self.browser.close()
            raise ValueError("Invalid Credentials. Confirm that your username & password are correct")


    def removeNotificationsPopup(self):
        remove_popup = self.browser.find_element_by_xpath('//button[contains(@class, "aOOlW   HoLwm ")]')
        ActionChains(self.browser)\
            .move_to_element(remove_popup)\
            .click()\
            .perform()
        sleep(2)

    def searchForTag(self, hashtag):
        test_initial_url = self.browser.current_url
        search_bar = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        ActionChains(self.browser)\
            .move_to_element(search_bar)\
            .click()\
            .send_keys('#' + hashtag)\
            .pause(2)\
            .send_keys(Keys.DOWN)\
            .send_keys(Keys.ENTER)\
            .perform()
        sleep(4)
        test_new_url = self.browser.current_url

        if(test_initial_url == test_new_url):
            self.browser.close()
            raise ValueError("Something went wrong. The app was not able to search for your hashtag. Try again")

    def likePhotos(self, time):
        body_element = self.browser.find_element_by_tag_name('body')
        for _ in range(1):
            body_element.send_keys(Keys.END)
            sleep(2)
            body_element.send_keys(Keys.HOME)
            sleep(2)

        sleep(2)

        images = self.browser.find_elements_by_class_name("_9AhH0")

        for i, image in enumerate(images):
            print('{}/{}'.format(i, len(images)))
            sleep(time)
            ActionChains(self.browser)\
                .move_to_element(image)\
                .click().perform()
            sleep(time)

            like_button = self.browser.find_elements_by_xpath('//button[contains(@class, "dCJp8 afkep")]')

            try:
                is_heart_filled = self.browser.find_element_by_xpath('//span[contains(@class, "glyphsSpriteHeart__filled__24__red_5 u-__7")]')
            except:
                is_heart_filled = False
                pass
            if(is_heart_filled):
                self.closePopup()
                continue

            try:
                ActionChains(self.browser)\
                    .move_to_element(like_button[0])\
                    .click()\
                    .perform()
                self.closePopup()
            except IndexError:
                self.browser.close()
                print("Index error")
                raise IndexError
        
            
    def closePopup(self):
        exit_popup = self.browser.find_element_by_class_name("ckWGn")
        ActionChains(self.browser)\
            .move_to_element(exit_popup)\
            .click()\
            .perform()

    def closeBrowser(self):
        print("Operation finished. Closing down the browser...")
        sleep(2)
        self.browser.close()
    
    def searchAndLikePhotos(self, hashtags: list, time: int):
        for tag in hashtags:
            self.searchForTag(tag)
            self.likePhotos(time)

    def startBot(self, hashtag_list):
        self.signIn()
        self.removeNotificationsPopup()
        self.searchAndLikePhotos(hashtag_list,self.time)
        

def argsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, required=True, help='Instagram account')
    parser.add_argument('--password', type=str, required=True, help='Password for your instagram account')
    parser.add_argument('--time', type=int, required=False, default=5, help="Seconds between browser actions")
    args = parser.parse_args()
    return args