import ast
import re

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase

import requests
from bs4 import BeautifulSoup


url_1 = "https://web.archive.org/web/20220313182641/https://www.imdb.com/title/tt10048342/?ref_=nv_sr_srsg_0"
url_2 = "https://web.archive.org/web/20220312014418/https://www.imdb.com/title/tt0068646/?ref_=nv_sr_srsg_0"


class WebScraperTest(StageTest):
    def generate(self):
        return [TestCase(stdin=url_1, check_function=self.check_answer,
                         attach=url_1, time_limit=50000),
                TestCase(stdin=url_2, check_function=self.check_answer,
                         attach=url_2, time_limit=50000),
                TestCase(stdin="https://www.imdb.com/name/nm0001191/", check_function=self.check_incorrect_url,
                         time_limit=50000),
                TestCase(stdin="https://www.google.com/", check_function=self.check_incorrect_url, time_limit=50000)]

    def check_url(self, url):
        try:
            response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'}).content
        except Exception:
            CheckResult.wrong("An error occurred when tests tried to connect to the Internet page.\n"
                              "Please, try again.")
        else:
            soup = BeautifulSoup(response, 'html.parser')
            h_link = soup.find('h1')
            title = h_link.text
            span_link = soup.find('span', {'data-testid': 'plot-l'})
            description = span_link.text
            return title, description

    def check_incorrect_url(self, reply, attach=None):
        if "Invalid movie page!" in reply:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("""If the link does not contain movie info or not an IMDB resource, 
            please respond with 'Invalid movie page!' message!""")

    def check_answer(self, reply, attach=None):

        output = re.search('({.+})', reply)
        if output is None:
            return CheckResult.wrong("Output dictionary was expected.\n"
                                     "However, it was not found.")
        try:
            reply_dict = ast.literal_eval(output.group(0))
        except (AttributeError, ValueError, SyntaxError):
            return CheckResult.wrong("An error occurred while your output was being parsed.\n"
                                     "Make sure you output a dictionary and its keys and values contain no HTML tags.")

        if 'title' not in reply_dict:
            return CheckResult.wrong("There's no \'title\' field in your output.")
        if 'description' not in reply_dict:
            return CheckResult.wrong("There's no \'description\' field in your output.")

        user_description = reply_dict["description"]
        user_title = reply_dict["title"]

        if not user_title or not user_description:
            return CheckResult.wrong("Seems like there is a title or a description missing in the output dictionary.")

        if type(user_description) != str or type(user_title) != str:
            return CheckResult.wrong("The values of keys 'title' and 'description' should be strings.\n"
                                     "However, it seems that in your output the type of one or both of these values "
                                     "isn't string.")

        try:
            title, description = self.check_url(attach)
        except Exception:
            return CheckResult.wrong("An error occurred when tests tried to connect to the Internet page.\n"
                                     "Please, try again.")
        if user_title == title and user_description == description:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("Title or description in returned dict do not seem to be correct.")


if __name__ == '__main__':
    WebScraperTest().run_tests()
