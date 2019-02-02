# @auther Jisson Varghse
# 02/02/2019

# Alogrithm to matach a new serarch against the properites in the db
# 1. find all the records which satisfies all the search criteria
# use Haversine formula and use b/w clause to find  min_price- min_price * 25  and max_price + max_price * 25/100
# and bedroom b/w  min_bedroom - 2 and max_bed_room +2
# and bathroom b/w min_bathroom -2 and  max_bathroom + 2.



# Give a weight to each of the valid record, If the distance b/w the given place and the record in db in range of
#  miles give it a weight of 30 and give the weight for different distance as follows

# 2 miles : 30
# 3 & 4   : 25
# 5 & 6   : 20
# 7 & 8   : 15
# 9 & 10  : 10


# 2. Price:

# Give a weight to each of the records
# if  min < Price < max   : 30   or   min-min * 1/10 < min <  min + min* 1/10 or max-max * 1/10 < max <  max + max* 1/10
# else if the Price in not in the given range but its valid give different weights, Divide the exta 25% we choose and\
# divide it into 5 groups,
#  so if price in the db is 5% less than given min give a weight of 25/2
#     if price in the db is in 6-10 % less than given min give a weight of 20/2
#     if price in the db is 11-15 % less than given min give a weight of 15/2
#     if price in the db is 16-20 % less than given min give a weight of 10/2
#     if price in the db is 21-25 %  less than given min give a weight of 5/2

# same is applied for the max
# so if min = 12500, max = 17500, an item having price 15000 get a 30 weight and if its not in range but near to the range get more weightage
# Price 12000 get a more weight than 10000.


# 2. Bedroom:


# Check the given min-2 and max+2 are match with the record and apply weight to each
# if  min < No of rooms(from db) < max  . Give weight 20
# min -1 <     Give weight 10/2
# min -1 <     Give weight 5/2
# Consider the edge case of min- 2 <= 0.

# apply same logic for Bathroom.
# Find the total weight and order the records according to the wight in desc.



class AgentDeskCriteria(object):

    LOCATION_WEIGHT = {}
    property_data_from_db = [
        {"id": 1, "latitude": 12.98765, "longitude": 77.67567, "price": 25000, "bedroom": 2, "bathroom": 4,
         "distance": 1},
        # {"id": 2, "latitude": 12.98765, "longitude": 77.67567, "price": 7000, "bedroom": 1, "bathroom": 3,
        #  "distance": 1},
        # {"id": 3, "latitude": 12.98765, "longitude": 77.67567, "price": 10000, "bedroom": 1, "bathroom": 2,
        #  "distance": 1},
        # {"id": 4, "latitude": 12.98765, "longitude": 77.67567, "price": 15000, "bedroom": 2, "bathroom": 5,
        #  "distance": 1},
        # {"id": 5, "latitude": 12.98765, "longitude": 77.67567, "price": 16000, "bedroom": 2, "bathroom": 2,
        #  "distance": 1},
        # {"id": 6, "latitude": 12.98765, "longitude": 77.67567, "price": 22000, "bedroom": 4, "bathroom": 5,
        #  "distance": 1},
        # {"id": 7, "latitude": 12.98765, "longitude": 77.67567, "price": 18000, "bedroom": 3, "bathroom": 2,
        #  "distance": 1},
        # {"id": 8, "latitude": 12.98765, "longitude": 77.67567, "price": 19000, "bedroom": 3, "bathroom": 10,
        #  "distance": 1},
        # {"id": 9, "latitude": 12.98765, "longitude": 77.67567, "price": 20000, "bedroom": 3, "bathroom": 2,
        #  "distance": 1},
        # {"id": 9, "latitude": 12.98765, "longitude": 77.67567, "price": 20000, "bedroom": 30, "bathroom": 20,
        #  "distance": 11}
    ]

    def __init__(self, latitude, longitude, min_price, max_price, min_bedroom=None, max_bedroom=None, min_bathroom=None, max_bathroom=None):
        self.latitude = latitude
        self.longitude = longitude
        self.min_price = min_price
        self.max_price = max_price
        self.min_bedroom = min_bedroom
        self.max_bedroom = max_bedroom
        self.min_bathroom = min_bathroom
        self.max_bathroom = max_bathroom

    # The method to match the new search criteria with the properities from the database.
    def new_serach_criteria(self):

        # fetch all the places are with in range of 10 miles and
        # The database query should fetch the records which are in range of 10 miles and the no_of_bedroom in range of
        self.get_properites_from_db()
        price_weight = self.get_price_weight_method()
        bed_room_weight = self.get_bed_room_weight_method()
        bath_room_weight = self.get_bath_room_weight_method()

        for item in self.property_data_from_db:
            item["location_weight"] = self.fetch_location_weight(item)
            item["price_weight"] = price_weight(item)
            item["bedroom_weight"] = bed_room_weight(item)
            item["bath_room_weight"] = bath_room_weight(item)
            total_wt = item["location_weight"] + item["price_weight"] + item["bedroom_weight"]+ item["bath_room_weight"]
            item["total_wt"] = total_wt

        # order it total_wt des order.
        print(self.property_data_from_db)


    def get_properites_from_db(self):
        """
        The query should have all the records having all the search criteria.
        and cache it.
        :return:
        """
        # fetch the records which are in 10 miles boundary and price between self.min_price - self.min_price / 10
        # and self.max_price+ self.max_price/10
        # and the no of bedrooms b/w self.min_bed_room - self.min_bed_room /10 and self.max_bedroom + self.max_bedroom /10
        # and no of bathrooms b/w self.min_bathroom - min_bathroom /10 and self.max_bathroom + max_bathroom /10.
        return self.property_data_from_db


    def fetch_location_weight(self, item):
        loc_wt = None
        if 0 <= item["distance"] <= 2:
            loc_wt = 30

        elif 3 <= item["distance"] <= 4:
            loc_wt = 25

        elif 5 <= item["distance"] <= 6:
            loc_wt = 20

        elif 7 <= item["distance"] <= 8:
            loc_wt = 15

        elif 9 <= item["distance"] <= 10:
            loc_wt = 10
        else:
            loc_wt = 0
        return loc_wt

    def get_price_weight_method(self):
        """
        :return: any of the method assign_price_weight_both or assign_price_weight_min or assign_price_weight_max
        """
        if self.min_price and self.max_price:
            met = self.assign_price_weight_both
            # only min_price given
        elif not self.max_price:
            met = self.assign_price_weight_min()

        # only max_price given
        else:
            met = self.assign_price_weight_max()
        return met

    def get_bed_room_weight_method(self):
        # return any of the method to call
        if self.min_bedroom and self.max_bedroom:
            met = self.fetch_bedroom_weight_both
        elif not self.max_bedroom:
            met = self.fetch_bedroom_min_weight
        else:
            met = self.fetch_bedroom_max_weight
        return met

    def get_bath_room_weight_method(self):
        # return any of the method to call.
        if self.min_bathroom and self.max_bathroom:
            met = self.fetch_bathroom_weight_both
        elif not self.max_bathroom:
            met = self.fetch_bathroom_weight_min
        else:
            met = self.fetch_bathroom_weight_max
        return met

    def assign_price_weight_both(self, item):
        # both min and max given and with in range
        price_wt = None
        if self.min_price <= item["price"] <= self.max_price:
            price_wt = 30
        else:
            price_wt = self.get_price_min_weight(item) + self.get_price_max_weight(item)
        return price_wt

    def get_price_min_weight(self, item):
        min_wt = None
        if self.min_price < item["price"]:
            return 0
        if self.min_price - self.min_price * 5/100 <= item["price"]:
            min_wt = 25
        elif self.min_price - self.min_price / 10 <= self.min_price:
            min_wt = 20
        elif self.min_price - self.min_price * 15/100 <= self.min_price:
            min_wt = 15
        elif self.min_price - self.min_price * 20/100 <= self.min_price:
            min_wt = 10
        elif self.min_price - self.min_price * 25/100 <= self.min_price:
            min_wt = 5
        else:
            min_wt = 0
        return min_wt

    def get_price_max_weight(self, item):
        max_wt = None
        if self.max_price > item["price"]:
            return 0
        if self.max_price + self.max_price * 5/100 >= item["price"]:
            max_wt = 25
        elif self.max_price + self.max_price / 10 >= item["price"]:
            max_wt = 20
        elif self.max_price + self.max_price * 15/100.0 >= item["price"]:
            max_wt = 15
        elif self.max_price + self.max_price * 20/100  >= item["price"]:
            max_wt = 10
        elif self.max_price + self.max_price * 25 /100 >= item["price"]:
            max_wt = 5
        else:
            max_wt = 0
        print("get_price_max_weight {}".format(max_wt))
        return max_wt

    def fetch_bedroom_weight_both(self, item):

        bedroom_wt = None
        if self.min_bedroom <= item["bedroom"] <= self.max_bedroom:
            bedroom_wt = 20
        else:
            bedroom_wt = self.fetch_bedroom_min_weight(item) + self.fetch_bedroom_max_weight(item)

        return bedroom_wt

    def fetch_bathroom_weight_both(self, item):
        bathroom_wt = None
        if self.min_bathroom <= item["bathroom"] <= self.max_bathroom:
            bathroom_wt = 20
        else:
            bathroom_wt = self.get_bathroom_min_weight(item) + self.get_bathroom_max_weight(item)
        return bathroom_wt

    def fetch_bathroom_weight_min(self, item):
        bathroom_wt = None

        if self.min_bathroom < item["bathroom"]:
            bathroom_wt =  0
        if self.min_bathroom - 1 == item["bathroom"]:
            bathroom_wt = 10
        elif self.min_bathroom - 2 == item["bathroom"]:
            bathroom_wt = 5
        return bathroom_wt

    def fetch_bathroom_weight_max(self, item):
        bathroom_wt = None
        if self.max_bathroom > item["bathroom"]:
            bathroom_wt = 0
        if self.max_bathroom + 1 == item["bathroom"]:
            bathroom_wt = 10
        elif self.max_bathroom + 2 == item["bathroom"]:
            bathroom_wt = 5
        return bathroom_wt

    def fetch_bedroom_min_weight(self, item):
        min_wt = None
        if self.min_bedroom < item["bedroom"]:
            min_wt = 0
        if self.min_bedroom - 1 == item["bedroom"]:
             min_wt = 10
        elif self.min_bedroom - 2 == item["bedroom"]:
            min_wt = 5
        else:
            min_wt = 0
        return min_wt

    def fetch_bedroom_max_weight(self, item):
        max_wt = None
        if self.max_bedroom > item["bedroom"]:
            max_wt = 0
        if self.max_bedroom + 1 == item["bedroom"]:
            max_wt = 10
        elif self.min_bedroom + 2 == item["bedroom"]:
            max_wt = 5
        else:
            max_wt = 0
        return max_wt

    def get_bathroom_min_weight(self, item):
        min_wt = None
        if self.min_bathroom < item["bathroom"]:
            min_wt = 0
        if self.min_bathroom - 1 == item["bathroom"]:
             min_wt = 10
        elif self.min_bathroom - 2 == item["bathroom"]:
            min_wt = 5
        else:
            min_wt = 0
        return min_wt

    def get_bathroom_max_weight(self, item):
        max_wt = None
        if self.max_bathroom > item["bathroom"]:
            max_wt = 0
        if self.max_bathroom - 1 == item["bathroom"]:
             max_wt = 10
        elif self.max_bathroom - 2 == item["bathroom"]:
            max_wt = 5
        else:
            max_wt = 0
        return max_wt


    def assign_price_weight_min(self, item):
        min_wt = None
        # only min_price given and with +/-  10 %
        if self.min_price - self.min_price /10 <= self.price <= self.min_price + self.min_price/10:
            min_wt = 30
        else:
            min_wt = self.get_price_min_weight(item)
        return min_wt

    def assign_price_weight_max(self, item):
        max_wt = None
        # only max_price given and with +/-  10 %
        if self.max_price - self.max_price/10 <= self.price <= self.max_price + self.max_price/10:
            max_wt = 30
        else:
            max_wt = self.get_price_max_weight(item)
        return max_wt


new_serarch_agent = AgentDeskCriteria(12.98765, 77.67567, 12500, 17500, 3, 4, 1, 2)
new_serarch_agent.new_serach_criteria()



# To find the search matches when a new property added
# Fetch the data from db satisfying all the criteria.

class AgentDeskSearchMatch(object):

    searches = [

        {"id": 1, "latitude": 12.6787, "longitude": 77.657,"min_price": 14000, "max_price": 18000, "min_bedroom": 1, "max_bedroom": 7, "min_bathroom": 2, "max_bathroom": 3, "distance": 10},
        # {"id": 2, "latitude": 12.6787, "longitude": 77.657, "min_price": 10000, "max_price": 14000, "min_bedroom": 2, "max_bedroom": 3, "min_bathroom": 2, "max_bathroom": 3, "distance": 4},
        # {"id": 3, "latitude": 12.6787, "longitude": 77.657, "min_price": 12500, "max_price": 20000, "min_bedroom": 2, "max_bedroom": 3, "min_bathroom": 2, "max_bathroom": 3, "distance": 10}
    ]

    def __init__(self, latitude, longitude, price, bedroom, bathroom):
        self.latitude = latitude
        self.longitude = longitude
        self.price = price
        self.bedroom = bedroom
        self.bathroom = bathroom

    def get_data_from_db(self):
        # fetch the data from db statisfying all the conditions.
        return self.searches

    def get_search_matches(self):
        for item in self.searches:
            self.get_location_weightage()
            item["location_weight"] = self.fetch_location_weight(item)
            item["price_weight"] = self.get_price_weightage(item)
            item["bedroom_weight"] = self.get_bedroom_weightage(item)
            item["bathroom_weight"] = self.bathroom_weightage(item)
            item["total_weight"] = item["location_weight"] + item["price_weight"] + item["bedroom_weight"]+ item["bathroom_weight"]
        print(self.searches)

    def get_location_weightage(self):
        pass

    def get_price_weightage(self, item):
        price_wt = 0
        if item.get("min_price") and item.get("max_price"):
            price_wt = self.get_min_price_wt(item) + self.get_max_price_wt(item)

        elif item.get("min_price"):
            if self.price - self.price /10 <= item["min_price"] <= self.price + self.price /10:
                price_wt = 30
            else:
                place_wt = self.get_min_price_wt(item)
        else:
            place_wt = self.get_max_price_wt(item)

        return price_wt

    def fetch_location_weight(self, item):
        loc_wt = None
        if 0 <= item["distance"] <= 2:
            loc_wt = 30

        elif 3 <= item["distance"] <= 4:
            loc_wt = 25

        elif 5 <= item["distance"] <= 6:
            loc_wt = 20

        elif 7 <= item["distance"] <= 8:
            loc_wt = 15

        elif 9 <= item["distance"] <= 10:
            loc_wt = 10
        else:
            loc_wt = 0
        return loc_wt

    def get_min_price_wt(self, item):
        if self.price - self.price * 5 / 100 <= item["min_price"]:
            price_wt = 30 / 2
        elif self.price - self.price * 10 / 100 <= item["min_price"]:
            price_wt = 25 / 2
        elif self.price - self.price * 15 / 100 <= item["min_price"]:
            price_wt = 20 / 2
        elif self.price - self.price * 20 / 100 <= item["min_price"]:
            price_wt = 15 / 2
        elif self.price - self.price * 10 / 100 <= item["min_price"]:
            price_wt = 10 / 2
        else:
            price_wt = 0
        return price_wt

    def get_max_price_wt(self, item):
        if self.price + self.price * 5 / 100 >= item["max_price"]:
            price_wt = 30 / 2
        elif self.price + self.price * 10 / 100 >= item["max_price"]:
            price_wt = 25 / 2
        elif self.price + self.price * 15 / 100 >= item["max_price"]:
            price_wt = 20 / 2
        elif self.price + self.price * 20 / 100 >= item["max_price"]:
            price_wt = 15 / 2

        elif self.price + self.price * 25 / 100 >= item["max_price"]:
            price_wt = 10 / 2
        else:
            price_wt = 0
        return price_wt

    def get_bedroom_weightage(self, item):
        bedroom_wt = 0
        if item.get("min_bedroom") and item.get("max_bedroom"):
            bedroom_wt = self.get_min_bedroom_wt(item) + self.get_max_bedroom_wt(item)
        elif item.get("min_bedroom"):
            bedroom_wt = self.bedroom(item)
        else:
            bedroom_wt = self.get_max_bedroom_wt(item)
        return bedroom_wt

    def get_min_bedroom_wt(self, item):
        bedroom_min_wt =0
        if item["min_bedroom"] <= self.bedroom <= item["max_bedroom"]:
            bedroom_min_wt = 20
        elif self.bedroom - 1 == item["min_bedroom"]:
            bedroom_min_wt = 10
        elif self.bedroom -2 == item["min_bedroom"]:
            bedroom_min_wt = 5
        else:
            bedroom_min_wt =0
        return bedroom_min_wt

    def get_max_bedroom_wt(self, item):
        bedroom_max_wt = 0
        if item["max_bedroom"] <= self.bedroom <= item["max_bedroom"]:
            bedroom_min_wt = 20
        if self.bedroom + 1 == item["max_bedroom"]:
            bedroom_max_wt = 10
        elif self.bedroom + 2 == item["max_bedroom"]:
            bedroom_max_wt = 5
        else:
            bedroom_max_wt = 0
        return bedroom_max_wt

    def bathroom_weightage(self, item):
        if item.get("min_bathroom") and item.get("max_bathroom"):
            bathroom_wt = self.get_min_bathroom_wt(item) + self.get_max_bathroom_wt(item)
        elif item.get("min_bathroom"):
            bathroom_wt = self.get_min_bathroom_wt(item)
        else:
            bathroom_wt = self.get_max_bathroom_wt(item)
        return bathroom_wt

    def get_min_bathroom_wt(self, item):
        bathroom_min_wt = 0
        if self.bathroom - 1 == item["min_bedroom"]:
            bathroom_min_wt = 10
        elif self.bathroom - 2 == item["min_bedroom"]:
            bathroom_min_wt = 5
        else:
            bedroom_min_wt = 0
        return bathroom_min_wt

    def get_max_bathroom_wt(self, item):
        bathroom_max_wt = 0
        if self.bathroom - 1 == item["min_bathroom"]:
            bathroom_max_wt = 10
        elif self.bathroom - 2 == item["min_bathroom"]:
            bathroom_max_wt = 5
        else:
            bedroom_min_wt = 0
        return bathroom_max_wt

AgentDeskSearchMatch(12.9876, 77.675, 15000, 2, 2).get_search_matches()
