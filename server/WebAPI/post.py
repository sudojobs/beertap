# importing the requests library 
import requests
import json

# defining the api-endpoint  
API_ENDPOINT = "https://dev-api.hk.eats365.net/o/oauth2/token"

RestaurantName  ="BeerTap" 
RestaurantCode  ="HK054042"
APIClientID     ="d3c345808af848adb6c89a43a48e18be"
APIClientSecret ="66f7456893ca4dce855bfa481a68aa9fe3a42b04a95d4ee2bbb385096cecded0"
  
# data to be sent to api 
data = {'client_id':APIClientID, 
        'client_secret':APIClientSecret, 
        'grant_type':"client_credentials"} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
pastebin_url = r.text 

accessdata=r.json()
AccessToken= accessdata['access_token']
TokenType= accessdata['token_type']
#print AccessToken 
#print TokenType
# api-endpoint 
URL = "https://dev-opi.hk.eats365.net/v1/menu/init"
head= "Bearer %s" % AccessToken
#print head
### defining a params dict for the parameters to be sent to the API 
PARAMS = { 'restaurant_code':RestaurantCode }
HEADER = { 'Authorization':head } 
### sending get request and saving the response as response object 
p = requests.get(url = URL, headers=HEADER, params = PARAMS) 
### extracting data in json format 
data = p.json()
#print data
ProductID=data["restaurant_list"]
print(json.dumps(ProductID, indent=4, separators=(". ", " = ")))
#Catlist=ProductID["category_list"]

##
#for i in ProductID:
#    print(ProductID[0]) 
