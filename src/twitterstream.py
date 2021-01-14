from requests_oauthlib import OAuth2Session
import urllib.request as ulib

# See assignment1.html instructions or README for how to get these credentials

api_key = "YyVPbobyuRbJ8t9sS0VVDIkhw"
api_secret = "ze5z1IkU6TWDi65hfHpKj9fsFBgjObFhNvTVk4S1zA6ERlQrk6"
access_token_key = "917858269095489538-5mfEafKMMtdo6gq10ZTyuRFBxuQqIpI"
access_token_secret = "UMmjH71sxivCF3yEztcBGW4ZY1ZtM5CCy8hGEKwM9Cx0a"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = ulib.HTTPHandler(debuglevel=_debug)
https_handler = ulib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = ulib.build_opener()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://twitter.com/hashtag/StocksToWatch?src=hashtag_click&f=live"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print(line.strip())

if __name__ == '__main__':
  fetchsamples()