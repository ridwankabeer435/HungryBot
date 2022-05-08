import discord
import requests
import random

#from env import TOKEN
from SECRETS import TOKEN
from SECRETS import YELP_KEY

# use the Yelp Fusion API to get a random restaurant
# for now, the bot can only recommend restaurants located in Toronto
def find_a_restaurant(user_cat=""):
  # get the category from the user, 
  selected_business = None
  #yelp_url = "https://api.yelp.com/v3/categories"
  yelp_search_url = "https://api.yelp.com/v3/businesses/search"
  key = YELP_KEY
  headers = {'Authorization': 'Bearer %s' % key}
  restaurant_params = {'locale' : 'en_CA','category_filter' : 'restaurants', 'categories' : user_cat, 'location' :  "Toronto, ON" } # this is just for demo purposes
  
  business_response = requests.get(yelp_search_url, headers=headers, params=restaurant_params)
  business_data = business_response.json()

  if(business_data["total"]== 0 ):
    # say that there is no restaurants with that category
    pass
  else:
    # select a random restaurant and return the message
    selected_business = random.choice(business_data["businesses"])    
    pass

  return selected_business



client = discord.Client()

# no message is sent out when the bot is started -- only that it is active on the server
@client.event
async def on_ready():
 
  print('{0.user} just logged in'.format(client))
  '''
  channel = client.get_channel()
  await channel.send("I am the hungry bot!!! \n Type in '$find-restaurant <type of restaurant>' and I will recommend you a ")
  '''


@client.event
async def on_message(message):
  #if the bot itself sends a message, then simply ignore the message
  if message.author == client.user:
    return
  # the user will enter a category
  if message.content.startswith('$find-restaurant '):
    restaurant_cats = message.content.split('$find-restaurant ')[1]
    restaurant_found = find_a_restaurant(user_cat=restaurant_cats)
    if restaurant_found == None:
       await message.channel.send("I am sorry I don't have a restaurant to recommend to you. Try with another keyword maybe")
    else:
      message_to_send = "Try this place: {} \nAddress: {}, {}, {}, {} \n {} \n {}".format(restaurant_found["name"], restaurant_found["location"]["address1"], restaurant_found["location"]["city"], restaurant_found["location"]["state"], restaurant_found["location"]["country"], restaurant_found["url"], restaurant_found["image_url"])
    await message.channel.send(message_to_send)

client.run(TOKEN)
