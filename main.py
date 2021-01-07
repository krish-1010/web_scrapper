import requests
from bs4 import BeautifulSoup
import pandas
import dbconnect

headers = {'user-agent': 'Mozilla/70.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}



place_info  = input("Enter the city to search for oyo hotels:  ")

oyo_url = f"https://www.oyorooms.com/hotels-in-{place_info}/?page="



page_num_MAX = int(input("Enter the number of pages you want to search : "))

scraped_list_info = []

dbconnect.connect('oyo.db')

for page_num in range(1,page_num_MAX+1):
    
    req = requests.get(url=oyo_url+str(page_num), verify=True, headers=headers)
    content = req.content
    soup = BeautifulSoup(content,"html.parser")
    all_hotels = soup.find_all("div",{"class":"hotelCardListing"})

    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"]  = hotel.find("h3",{"class":"listingHotelDescription__hotelName"}).text
        hotel_dict["address"]  = hotel.find("span",{"class":"u-line--clamp-2"}).text
        try:
            hotel_dict["price"] = hotel.find("span",{"class":"listingPrice__finalPrice"}).text
            
            parent_amenities_element = hotel.find("div",{"class":"amenityWrapper"})
            amenities_list = []
            for amenity in parent_amenities_element:
                amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())
            
            if 'more' in amenities_list[len(amenities_list)-1]:
                amenities_list = amenities_list[:-1]

            hotel_dict["amenities"] = ', '.join(amenities_list)
            print(amenities_list)
        
        except AttributeError:
            hotel_dict["amenities"] = None
            
        try:
            hotel_dict["rating"]  = hotel.find("span",{"class":"hotelRating__ratingSummary"}).text
        except AttributeError:
            hotel_dict["rating"] = None


            
        
        scraped_list_info.append(hotel_dict)

        dbconnect.insert_into_table('oyo.db', tuple(hotel_dict.values()))

dataFrame =  pandas.DataFrame(scraped_list_info)
dataFrame.to_csv("Oyo.csv")

dbconnect.get_hotel_info('oyo.db')





