from pymatgen import (MPRester, Composition)
from os import environ
from time import sleep
import tweepy as tp

def str_kisses_per_mol(chemical):
  KISS_ENERGY = 4.75E23
  AVOGADRO = 6.02E23

  try:
    rester = MPRester()
    comp = Composition(chemical)

    entries = rester.get_entries_in_chemsys([str(elem) for elem in comp.elements])
  except:
    return "Please tweet a chemical formula to me! I didn't understand your last request. :("

  for entry in entries:
    if entry.composition == comp:
      try:
        form_energy = entry.data["formation_energy_per_atom"]
        n_atoms = entry.data["nsites"]
        break
      except:
        return "I couldn't find the energy to make " + chemical + "."

  try:
    num_kisses = round(form_energy * n_atoms * AVOGADRO / KISS_ENERGY, 2)
  except:
    return "I couldn't figure out the energy to make " + chemical + "."

  if num_kisses > 0:
    return "Please give me " + str(num_kisses) + " Hershey's Kisses to form 1 mol of " + chemical + "."
  elif num_kisses == 0:
    return "We don't need any Hershey's Kisses to form " + chemical + "."
  else:
    return "I'll give you " + str(abs(num_kisses)) + " Hershey's Kisses from forming 1 mol of " + chemical + "."

def tweet_reply_kisses():
  auth = tp.OAuthHandler(environ.get("TWIT_KEY"), environ.get("TWIT_SEC_KEY"))
  auth.set_access_token(environ.get("TWIT_ACC_KEY"), environ.get("TWIT_ACC_SEC_KEY"))
  api = tp.API(auth)

  with open('latest_tweet', 'r') as f:
    latest_tweet_id = int(f.read())
    print "Old latest tweet: " + str(latest_tweet_id)

  try:
    public_tweets = api.mentions_timeline(count=20)
    new_latest_tweet_id = public_tweets[0].id
  except tp.TweepError:
    print "API limit exceeded!"
    return None

  for tweet in public_tweets:
    if tweet.id > latest_tweet_id:
      print "Current tweet id: " + str(tweet.id)
      reply_to_status_id = str(tweet.id)
      reply_to_username = str(tweet.user.screen_name)
      chemical = str(tweet.text.encode('utf-8').replace('@mat_e_tweeter', '').strip(' '))

      api.update_status("@" + reply_to_username + " " + str_kisses_per_mol(chemical), reply_to_status_id)
      print "@" + reply_to_username + " " + str_kisses_per_mol(chemical), reply_to_status_id

  with open('latest_tweet', 'wb') as f:
    print "New latest tweet: " + str(new_latest_tweet_id)
    f.write(str(new_latest_tweet_id))

if __name__ == '__main__':
  while True:
    if tweet_reply_kisses() is None:
      sleep(900)
    sleep(65)
