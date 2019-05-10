#
# Results Classe
#


class Results:

    # init function
    def __init__(self, date, driver):

        self.date = date 
        self.driver = driver 
        # Load page of results 
        self.results_page = self.driver.get(
            "https://greyhoundbet.racingpost.com/#results-list/r_date=%s" % self.date,
            element_wait="meetings",
            type_element="class"
        )

    # get links on results page
    def get_links(self):
        # Getting links
        self.results_links = list()
        for headline in self.results_page.find_all("div", class_="results-race-list-row"):
            for link in headline.find_all("a"):
                self.results_links.append(link.attrs["href"])    
        return self.results_links