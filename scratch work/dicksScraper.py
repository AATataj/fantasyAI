import requests

# Input : a list of integer sku values and integer store ID codes
# Output : json response of the availability of the sku products at the store ID codes given
# OnError : returns "Error" + a short description of the error or HTTP error code
# Default store setting is 'location=0' aka, the nearest store given proximity of the request,
# Timeout value for the get request set to 10 seconds, but this functionality has not been tested 
# I tested this with a random non-existant store number '999999999999', the request doesn't throw an error, 
# just returns a 0 total count on the product.  So care must be taken when inputting the store list

def getAvailability (skus = [], locations = [0]):
    link = 'https://availability.dickssportinggoods.com/v1/inventoryapis/searchinventory?'
    if locations == [0]:
        link += 'location=0&sku='
    else :
        link += 'location='
        for location in locations:
            link += str(location) + ','
        link = link[:-1]
        link += '&sku='
    if skus == []:
        return "Error, no sku values given"
    else:
        for sku in skus:
            link+=str(sku) + ','
        link = link[:-1]
    headers = { 'accept' : 'application/json',
                'accept-encoding' : 'gzip, deflate, br',
                'accept-language' : 'en-US,en;q=0.9',
                'referer' : 'https://www.dickssportinggoods.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
            }
    req = requests.get(link,headers=headers, timeout = 10)        

    if req.status_code != 200:
        return "Error : returned http status code : " + str(req.status_code)
    else : 
        return req.text
    