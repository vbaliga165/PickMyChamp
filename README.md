# PickMyChamp
Do you ever dodge queue or pick Vayne mid because because you don't know who else to play? PickMyChamp is a solution to all your problems: a utility to generate the best choice of champion in a game of League of Legends (LoL).

![Project Sample](images/SampleOutput.png)

## Installing

Clone the repository to your computer 

```
git clone git://github.com/vsb321/PickMyChamp
```

In the directory, execute

```
python PickMyChamp.py
```

## How does it work?

This project can be broken down into 3 components:
   1. Collecting and manipulating user input
      - To keep things simple, I only ask for a summoner username and opponent the user is facing, in order to develop a *pseudo "profile"* of the user and their possible picks for the game.
      - Although we request information from the user at various points, we have to actually interpret it to come to a conclusion. I have basic information about the user, but **how do I actually _transcribe_ it?**
      	- Throughout the whole runtime of the application, I only webscrape two distinct sources:
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
       To create a final URL to parse and webscrape from, I had to generate it from the user input. Let's examine the makeup of URLs for both sources using the sample output above, as well as for another set of inputs.
       
       | Username URL     | Champion URL |
       | ------------- | ------------- |
       | http://na.op.gg/summoner/userName=Imaqtpie | https://www.lolcounter.com/champions/akali/weak or https://www.lolcounter.com/champions/akali/strong      |
       | http://na.op.gg/summoner/userName=Hide+on+Bush | https://www.lolcounter.com/champions/twistedfate/weak or https://www.lolcounter.com/champions/twistedfate/strong      |
       
       The input username (Imaqtpie) and the input enemy champion (Akali) are simply appended to a generic url displaying data and statistics. In the case that either inputs exceed one word, a symbol such as *'+'* is concatenated between each additional word. This is all accomplished through the ```get_true_url()``` function.
   2. Gathering and organizing user-specific data
   
      After opening the connection to our sources and using [Beautifil Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse the HTML to an applicable format for operating upon, I had to scrape the HTML for the variables to use in my calculations.      
      
      ![Data Sample](images/DataSample.png)
      
      When deciding a player's rating on a champion in comparison to the rest of their champion pool, I had to take a few factors into consideration: **Kill/Death/Assist Ratio, Games Played, Win Ratio.** Once this data was identified, I had to _search for and extract it_ within the HTML. Here is a portion of an [HTML sample](SampleChampAttributes.html) for a champion we worked with:
     
		     
		     <td class="RatioGraph Cell" data-value="65.957446808511">
		       <div class="WinRatioGraph">
			 <div class="Graph">
			    <div class="Fill Left" style="width: 65%"></div>
			    <div class="Text Left">62W</div>
			    <div class="Fill Right"></div>
			    <div class="Text Right">32L</div>
			    <div class="Bar" style="left: 65%;"></div>
			 </div>
			 <span class="WinRatio red">66%</span>
		       </div>
		      </td>
		      
	      
         To scrape the static winrate from the HTML, I had to search for ```<td>``` tags, going **layer by layer** until I got to the magic number I was looking for. Repeating this step for KDA ratio and Games played, the simplest way to work with this data was with ```Champion()``` objects in an array storing a user's champion pool. I had to repeat this process to generate the opponent counter list array as well.
   
   3. Coming to a conclusion of champions

      - In order to generate a list of top champions for the user to play, I needed some sort of relation between *games played, KDA and win rate*. 
      ```python 
       X = frame[['Games','KDA']] 
       Y = frame['Win Rate']

       regr = linear_model.LinearRegression()
       regr.fit(X, Y)
       ```
        - Using [pandas](https://pandas.pydata.org) and [sklearn](https://scikit-learn.org/stable/), I implemented a multiple linear regression with a data frame. The **independent (x)** variables were games played and KDA, and the **dependent (y)** variable was win rate. In other words, I was testing the effects that the number games played and the KDA ratio had on a champion's win rate.
![Graph](images/KDAVsWR.png)
        - When I had generated a prediction of weights for each champion using user-specific stats, I also had to take counter picks into account. If the opponent was strong against a champion in the user's pool, that champion's corresponding weight was multipled by ```0.75```. As you can guess, If the opponent was weak against a champion, the weight was multiplied by ```1.25```. 
        - Sorting the array of weights in descending order, the *champions with the top three highest weights* were returned and printed!
## FAQ

- **How do I generate a champion for a *specific* lane?**
    - As of yet, this feature is not supported. Check back for future updates!
- **Will this utility be supported on a mobile platform or website?**
    - I am currently in the process of making http://pickmychampion.com! Expect it in the near future.
- **How can I support PickMyChamp?**
    - Spreading the word or generating test cases is more than enough! I'm always looking for feedback, so please reach out to me with advice or ideas for future capabilities.

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2022 © <a href="http://vijaybaliga.com" target="_blank">Vijay Baliga</a>.
