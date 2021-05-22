# Delta moves, historically

The aim of this project is to build out a simple Dash web-app that allows a user to compare the probabilities of an option ending ITM (based on the delta of the option) compared to the historical move of the stock. The idea behind this is to figure out if the delta has 'priced in' the historical move of a stock.

For example, if the SPY is at 400 and a 390 Put, with 1 Day-To-Expiration, has a delta of 0.03, the estimated probability of expiring ITM is 3%. In order for this to happen, the stock would have to move ![equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7B400-390%7D%7B400%7D%20*%20100%20%3D%202.5%25). The deltas are hence telling us that there is an approximately 3% chance that the stock will move 2.5% in the day. This app will allow users to compare this probability to historical probabilities based on the stock movement - i.e. historically, what is the probability that a stock moves 3% in the same day. 
