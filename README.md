# PickMyChamp
Utility to generate the best choice of champion in a game of League of Legends (LoL).

## License
This project is licensed under the MIT License - see the [LICENSE.txt](https://github.com/vsb321/PickMyChamp/blob/master/LICENSE.txt) file for details

![Project Sample](SampleOutput.png)

### How does it work?

This project can be broken down into 3 components:
   1. Collecting and manipulating user input
      - To keep things simple, we only ask for a summoner username and opponent the user is facing, in order to develop a *pseudo "profile"* of the user and their possible picks for the game.
      - Although we request information from the user at various points, we have to actually interpret it to come to a conclusion. We have basic information about the user, but **how do we actually _transcribe_ it?**
      	- Throughout the whole runtime of the application, we only webscrape two distinct sources:
       	    1. LoL database for user statistics: [op.gg](http://na.op.gg)
	        2. Portal of good/bad picks for any and every champion that exists in LoL: [lolcounter](https://www.lolcounter.com)
	  
       ```python 
       def get_true_url(text_to_add, url_to_add, symbol):
	        final_url = url_to_add
	        if len(text_to_add.split()) == 1:
		          final_url = url_to_add + text_to_add
	        else:
		          words = text_to_add.split()
		          i = 0
		          for word in words:
			          if i < len(words) - 1:
				          final_url = final_url + (word + symbol)
			          else:
				          final_url = final_url + word
			        i = i + 1
	        return final_url
       ```
       To create a final URL to parse and webscrape from, we must generate it from the user input. Let us examine the makeup of URLs for both sources using the sample output above, as well as for another set of inputs.
       
       | Username URL     | Champion URL |
       | ------------- | ------------- |
       | http://na.op.gg/summoner/userName=Imaqtpie | https://www.lolcounter.com/champions/akali/weak or https://www.lolcounter.com/champions/akali/strong      |
       | http://na.op.gg/summoner/userName=Hide+on+Bush | https://www.lolcounter.com/champions/twistedfate/weak or https://www.lolcounter.com/champions/twistedfate/strong      |
       
       The input username (Imaqtpie) and the input enemy champion (Akali) are simply appended to a generic url displaying data and statistics. In the case that either inputs exceed one word, a symbol such as *'+'* is concatenated between each additional word. This is all accomplished through the ```get_true_url()``` function.
   2. Gathering user-specific data
   3. Organizing data in a comprehensible format
