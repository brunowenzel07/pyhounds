# ------------------------------------------------------------------
# Tracks class
# ------------------------------------------------------------------


class Tracks:

    # Construct method
    def __init__(self, link, driver):
        # Defing components variables
        self.url = link
        self.driver = driver
        # Return track page
        self.result_page = self.driver.get(
            "https://greyhoundbet.racingpost.com/#results-list/r_date=%s" % self.url,
            element_wait="meetings",
            type_element="class")

    # Return all links in result page
    def links(self):
        self.results_links = list()
        for headline in self.result_page.find_all("div", class_="results-race-list-row"):
            for link in headline.find_all("a"):
                self.results_links.append(link.attrs["href"])
        return self.results_links
