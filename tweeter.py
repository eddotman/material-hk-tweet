from pymatgen import (MPRester, Composition)
import tweepy as tp

def str_kisses_per_mol(chemical):
  KISS_ENERGY = 4.75E23
  AVOGADRO = 6.02E23

  rester = MPRester()
  comp = Composition(chemical)

  entries = rester.get_entries_in_chemsys([str(elem) for elem in comp.elements])

  for entry in entries:
    if entry.composition == comp:
      try:
        form_energy = entry.data["formation_energy_per_atom"]
        n_atoms = entry.data["nsites"]
        break
      except:
        return "I couldn't find the energy to make " + chemical + "."

  try:
    num_kisses = round(form_energy * n_atoms * AVOGADRO / KISS_ENERGY, 8)
  except:
    return "I couldn't figure out the energy to make " + chemical + "."

  if num_kisses > 0:
    return "Please give me " + str(num_kisses) + " Hershey's Kisses to form 1 mol of " + chemical + "."
  elif num_kisses == 0:
    return "We don't need any Hershey's Kisses to form " + chemical + "."
  else:
    return "I'll give you " + str(abs(num_kisses)) + " Hershey's Kisses from forming 1 mol of " + chemical + "."

def tweet_reply_kisses(in_tweet=None):
  try:
    auth = tp.OAuthHandler(consumer_token, consumer_secret)
    redirect_url = auth.get_authorization_url()
  except tp.TweepError:
    print 'Error! Failed to get request token.'

tweet_reply_kisses()
