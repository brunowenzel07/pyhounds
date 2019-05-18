# ------------------------------------------------------------------
# Tracks class
# ------------------------------------------------------------------

from bs4 import BeautifulSoup

class Tracks:
    # Construct method

    def __init__(self, link=False, driver = False, t_ = False):
        # Defing components variables
        self.link          = link
        self.driver        = driver
        self.results_links = list()

        if t_ == "train":
            # Return track page
            self.result_page = self.driver.get(
                "https://greyhoundbet.racingpost.com/#results-list/r_date=%s" % self.link,
                element_wait = "meetings",
                type_element = "class")
        elif t_ == "predict":
            with open("html/predict.html", "r") as f_:
                self.result_page = BeautifulSoup(f_, "html.parser")

    # Return all links in result page
    def links(self):
        for headline in self.result_page.find_all("div", class_="results-race-list-row"):
            for link in headline.find_all("a"):
                self.results_links.append(link.attrs["href"])
        return self.results_links

    def future(self):
        for future in self.result_page.find("ul", class_="raceList").find_all("li"):
            self.results_links.append(future.find("a").attrs["href"])
        return self.results_links
