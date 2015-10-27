# Lockdown

**Benjamin Donnelly** -- **@zaeyx**

Two events caused me to decide that the creation of this tool was a worthy endeavor.
The "hacking" of the director of the CIA's email by a 13 year old kid; and a conversation I had with some peers about
the viability of current mobile device security.

It's not hard for an attacker to get access to your digital life.  Whether by social engineering, guessing security questions,
or stealing your phone.  This script is the digital equivalent of a safe room during a home invasion.

For now, the functionality is limited (though still powerful).  But if there's interest, I'll happily grow it.

###How to Set Up
  * Set up a gmail account to act as a listener
  * Configure this script to be able to access the emails for that gmail account
  * Feed this script the credentials to your critical accounts
  * Configure a "new_password"
  * Configure your panic phrase
  
###How to Trigger
  In the event of an emergency, all you need to do is send an email to the listening gmail account, containing your panic
  phrase.  Upon detecting your panic phrase the script will trigger.  It will authenticate to your accounts using the provided
  credentials and immediately change the password to the "new_password"
  
###Features
**Currently supports**
  * twitter
  * facebook
  * google
  
  
**Next Steps**
  * Credentials Encrypted -- Unlocked by password in panic email
  * Additional Sites
  * App/Session unlinking
  
Please direct any questions to me on Twitter **@zaeyx** or via Email **ben@prometheaninfosec.com**
