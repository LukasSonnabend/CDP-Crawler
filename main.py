import requests
from bs4 import BeautifulSoup
import yaml
import csv



def load_urls():
  # load urls from file
  urls = []
  with open("urls.txt", "r") as f:
    for line in f:
      urls.append(line.strip())
  return urls

def load_yaml():
  # load urls from file
  with open("scrape.yaml", "r") as f:
    try:
      parsed_yaml = yaml.safe_load(f)['headings_to_scrape']
      return parsed_yaml
    except yaml.YAMLError as exc:
      print(exc)
      return None

def get_page_html(url):
  # make get request to url
  response = requests.get(url)
  return response.content.decode("utf-8")

def get_page_soup(html):
  # parse html
  soup = BeautifulSoup(html, "html.parser")
  return soup

def get_company_from_dict(data_dict, company_name):
  if company_name not in data_dict:
    data_dict[company_name] = {}

  return dict[company_name]

def write_data_to_csv(data_dict):
  with open("data.csv", "w") as f:
    writer = csv.writer(f)
    # write header
    writer.writerow(["Company", "Year", "Top Heading", "Heading", "Data"])

    for company_name in data_dict:
      for year in data_dict[company_name]:
        for top_heading_to_scrape in data_dict[company_name][year]:
          for heading in data_dict[company_name][year][top_heading_to_scrape]:
            writer.writerow([company_name, year, top_heading_to_scrape, heading, data_dict[company_name][year][top_heading_to_scrape][heading]])


def main():
  # load urls from file
  urls = load_urls()
  top_headings_to_scrape = load_yaml()

  data_dict = {}


  # for url in urls:
  # testing
  with open("./CDP_BASF_2021.html", "r") as f:
    html = f.read()
   # html = get_page_html(url)
    parsed_html = get_page_soup(html)

    # get company name (erste h1 on page)
    company_name = parsed_html.find("h1").text.split("-")[0].strip()
    year = int(parsed_html.find("h1").text.split(" ")[-1].strip())-1




    for top_heading_to_scrape in top_headings_to_scrape:
        # find Top heading first
        top_heading = parsed_html.find("h3", class_="ndp_formatted_response__header", text=top_heading_to_scrape)
        correspoding_section = top_heading.parent

        for heading in top_headings_to_scrape[top_heading_to_scrape]:
          h3 = correspoding_section.find("h3", class_="ndp_formatted_response__header", text=heading)
          # go to next div with class "ndp_formatted_response__value"
          data_section = h3.parent.find("section")
          while data_section == None:
            data_section = h3.parent.nextSibling()

          data_div = None
          try:
            data_div = data_section.find("div", class_="ndp_formatted_response__value")
          except:
            data_div = data_section[0]

          ## hier gibt es mehrere spans
          data_string = ""

          if data_div:
            spans = data_div.find_all("span")
            if len(spans) > 0:
              for span in spans:
                data_string += span.text.strip()
            else:
              # Handles case where data is sibling of the heading
              data_string = data_div.text.strip()

          else:
            data_string = data_section.find("section", class_="ndp_formatted_response__answer_option").text.strip()

          if company_name not in data_dict:
              data_dict[company_name] = {}
          if year not in data_dict[company_name]:
              data_dict[company_name][year] = {}
          if top_heading_to_scrape not in data_dict[company_name][year]:
              data_dict[company_name][year][top_heading_to_scrape] = {}
          if heading not in data_dict[company_name][year][top_heading_to_scrape]:
            data_dict[company_name][year][top_heading_to_scrape][heading] = data_string

  write_data_to_csv(data_dict)


print("Welcome to web-eicker V1")
main()


if __name__ == "main__":
  main()

