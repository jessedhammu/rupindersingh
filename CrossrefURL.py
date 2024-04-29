import pandas as pd
import requests

# Function to fetch publication date and URL from CrossRef API using DOI
def fetch_publication_info(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        publication_date = data['message']['created']['date-time']
        article_url = data['message']['resource']['primary']['URL']
        return publication_date, article_url
    else:
        return None, None

# Read DOIs from the CSV file and fetch publication dates and URLs
def get_publication_info_from_csv(file_name):
    data = pd.read_csv(file_name)
    dois = data['doi'].tolist()
    publication_info = {}
    for doi in dois:
        publication_date, article_url = fetch_publication_info(doi)
        publication_info[doi] = {'Publication Date': publication_date, 'Article URL': article_url}

    return publication_info

# Function to write DOI, publication date, and URL to a new CSV file
def write_to_csv(output_file, data):
    df = pd.DataFrame([(key, value['Publication Date'], value['Article URL']) for key, value in data.items()],
                      columns=['DOI', 'Publication Date', 'Article URL'])
    df.to_csv(output_file, index=False)

# Mention the name and absolute path of the CSV file that contains the DOI numbers and the file where the output must be written.
input_csv_file = 'C:/Users/rupin/Desktop/doi.csv'
output_csv_file = 'C:/Users/rupin/Desktop/output_dates_and_urls.csv'

# Fetch publication dates and URLs
publication_info = get_publication_info_from_csv(input_csv_file)

# Write output to a new CSV file
write_to_csv(output_csv_file, publication_info)
