from requests_html import HTMLSession

session = HTMLSession()
session.browser

def scrape_url(url, sleep=10):
    """Intiate browser session for provided url and scrape its content.
    MechDB uses their own table class '.col.col-half.tbl' to wrap stats and values:
    <table _ngcontent-mxx-c66="" class="col col-half tbl">
        <tr _ngcontent-mxx-c66="">
            <th _ngcontent-mxx-c66="">Speed</th>
            <td _ngcontent-mxx-c66=""> 153.1 / 102.1 </td>
        </tr>
    </table>
    Time to render a page is required and it may differ based on server load.

    Args:
        url (string): valid MechDB url.
        sleep (integer): time is seconds that method will wait until page is rendered.

    Returns:
        dictionary: mech stats and their values
    """
    response = session.get(url)
    response.html.render(sleep=sleep)

    tables = response.html.find('.col.col-half.tbl')

    supported_stats = {
        'Armor': 'armor',
        'Engine': 'engine',
        'Speed': 'speed',
        'Firepower': 'firepower',
        'DPS (SUS/MAX)': 'dps',
        'Heat Sinks': 'heatsinks',
        'Dissipation': 'dissipation'
    }

    stats = {}
    for table in tables:
        rows = table.find('tr')
        for row in rows:
            header_text = row.find('th', first=True).text
            data_text = row.find('td', first=True).text
            if header_text in supported_stats:
                stats[supported_stats[header_text]] = data_text.replace(" ", "")
    
    return stats

