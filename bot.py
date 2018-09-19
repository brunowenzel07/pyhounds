# !/usr/bin/python 
import utils 

def get_races_results(track, driver):
    dogs_race = utils.get_dogs_links(track, driver)

# Read a page of tracks and returned all links for the races
def get_results_tracks(url, driver):
    """
        get_results_tracks
        param: url (url to get tracks)
        param: pass driver 
    """
    page_html = utils.get_code(url, driver, wait_element="results-race-name", wait_type="class")
    tracks = []
    for race_li in page_html.find("div", class_="meetings").find_all("li"):
        for race_link in race_li.find("div", class_="results-race-list-row").find_all("a"):
            tracks.append(race_link.attrs["href"][1:])
    return tracks