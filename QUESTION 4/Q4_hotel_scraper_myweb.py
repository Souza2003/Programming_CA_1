# QUESTION 4 (PART 2) (PYTHON)
# Hotel Room Price Web Scraper - Scrapes hotel data from local HTML file

import csv
from datetime import datetime
from bs4 import BeautifulSoup

class LocalHotelScraper:
    def __init__(self, html_file_path):
        self.html_file_path = html_file_path
        self.hotels_data = []
        self.csv_filename = "hotel_prices_comparison.csv"
    
    def scrape_and_save(self):
        """Read HTML, scrape data, and save to CSV"""
        print(f"\n{'='*80}\n  HOTEL ROOM PRICE WEB SCRAPING SYSTEM\n{'='*80}")
        
        # Read HTML file
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
            print(f" Loaded HTML file")
        except Exception as e:
            print(f" Error reading file: {e}")
            return False
        
        # Scrape hotel data (10 rooms from each of 2 hotels = 20 rooms total)
        hotel_cards = soup.find_all('div', class_='card')[:2]  # Limit to first 2 hotels
        print(f" Found {len(hotel_cards)} hotels")
        
        for card in hotel_cards:
            hotel_name = card.find('h3').text.strip() if card.find('h3') else 'Unknown'
            table = card.find('table')
            
            if table:
                room_count = 0
                for row in table.find('tbody').find_all('tr'):
                    if room_count >= 10:  # Limit to 10 rooms per hotel
                        break
                        
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        self.hotels_data.append({
                            'hotel_name': hotel_name,
                            'room_id': cols[0].text.strip(),
                            'room_name': cols[1].text.strip(),
                            'room_type': cols[2].text.strip(),
                            'capacity': cols[3].text.strip(),
                            'price_per_night': cols[4].text.strip(),
                            'currency': 'EUR',
                            'total_price': cols[5].text.strip(),
                            'cancellation_policy': cols[6].text.strip(),
                            'check_in_date': '20-Dec-2025',
                            'check_out_date': '30-Dec-2025',
                            'total_nights': 10,
                            'scraped_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        room_count += 1
        
        print(f" Scraped {len(self.hotels_data)} rooms (10 from each of 2 hotels)")
        
        # Save to CSV
        try:
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.hotels_data[0].keys())
                writer.writeheader()
                writer.writerows(self.hotels_data)
            print(f" Saved to {self.csv_filename}\n")
            return True
        except Exception as e:
            print(f" Error saving CSV: {e}")
            return False
    
    def display_from_csv(self):
        """Read and display CSV data in terminal"""
        print(f"{'='*80}\n  HOTEL PRICE COMPARISON REPORT\n{'='*80}")
        print(f"Period: 20-30 December 2025 (10 nights)\n{'='*80}")
        
        try:
            with open(self.csv_filename, 'r', encoding='utf-8') as csvfile:
                rows = list(csv.DictReader(csvfile))
            
            # Display by hotel
            current_hotel = None
            room_num = 0
            for row in rows:
                if current_hotel != row['hotel_name']:
                    current_hotel = row['hotel_name']
                    room_num = 0  # Reset counter for each hotel
                    print(f"\n{'='*80}\n  {current_hotel.upper()}\n{'='*80}")
                
                room_num += 1
                print(f"\n  {room_num}. [{row['room_id']}] {row['room_name']} ({row['room_type']})")
                print(f"     Capacity: {row['capacity']} | Per Night: EUR {row['price_per_night']}")
                print(f"     Total (10 nights): EUR {row['total_price']} | {row['cancellation_policy']}")
            
            # Price analysis
            print(f"\n{'='*80}\n  PRICE ANALYSIS\n{'='*80}")
            hotels = list(set([r['hotel_name'] for r in rows]))
            
            for hotel in hotels:
                prices = [float(r['total_price']) for r in rows if r['hotel_name'] == hotel]
                print(f"\n{hotel}:")
                print(f"  Rooms: {len(prices)} | Min: EUR {min(prices):.2f} | Max: EUR {max(prices):.2f} | Avg: EUR {sum(prices)/len(prices):.2f}")
            
            # Best options
            all_prices = [float(r['total_price']) for r in rows]
            cheapest = min(rows, key=lambda x: float(x['total_price']))
            savings = max(all_prices) - min(all_prices)
            
            print(f"\n{'─'*80}\n  RECOMMENDATIONS\n{'─'*80}")
            print(f"\n Best Budget Option:")
            print(f"   {cheapest['hotel_name']} - {cheapest['room_name']}")
            print(f"   EUR {cheapest['total_price']} for 10 nights")
            
            family_rooms = [r for r in rows if int(r['capacity']) >= 4]
            if family_rooms:
                best_family = min(family_rooms, key=lambda x: float(x['total_price']))
                print(f"\n Best Family Option (4+ guests):")
                print(f"   {best_family['hotel_name']} - {best_family['room_name']}")
                print(f"   Capacity: {best_family['capacity']} | EUR {best_family['total_price']}")
            
            print(f"\n Potential Savings: EUR {savings:.2f}\n{'='*80}\n")
            
        except Exception as e:
            print(f" Error reading CSV: {e}")
    
    def run(self):
        """Main execution"""
        if self.scrape_and_save():
            self.display_from_csv()
            print(" Process completed successfully!\n")
        else:
            print(" Process failed\n")


if __name__ == "__main__":
    # MY HTML FILE PATH
    html_file_path = r"C:\Users\Ruth\OneDrive\Desktop\DBS\Advanced Programming Techniques\CA_ONE\PART 2 (PYTHON)\QUESTION 4\mywebsite.html"
    
    scraper = LocalHotelScraper(html_file_path)
    scraper.run()