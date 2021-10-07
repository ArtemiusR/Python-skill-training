# Python-skill-training
Parser of financial information from investing/trading web-platform. Working with requests, pandas, asyncio libraries + OOP realization + asynchronous realization

This is how technical information of a random equity from ru.investing.com looks like

![image](https://user-images.githubusercontent.com/92031990/136464425-3ecd7b78-6004-46af-92ef-d1cb3eb12001.png)

The goal of the script was 

1) to get the data about all technical indicators (moaning averages and other technical indicators) in different time steps
of all equities from RTS+DowJones500 indecies and to archive it for future calculations.

2) to test the simplest trading strategy of buying and selling stocks when sum of all technical indicators >=100, >=90, >=80 and <=-100, <=-90, <=-80

3) to count posiible profit (while taking broker comission into account)

[Trader 0.3.ipynb] Script was kept running every hour in working days. The stock data it collects looks like
![image](https://user-images.githubusercontent.com/92031990/136465571-08b76e59-a322-42ec-82b4-1201d0f7b8b3.png)

Then it converts into buy/sell recomendations
![image](https://user-images.githubusercontent.com/92031990/136465656-c9fd6201-3e9e-434f-ab5a-707bd93163f6.png)

[Target Analyzer.ipynb] And in the end other script counts profit
![image](https://user-images.githubusercontent.com/92031990/136465877-3ed12ff5-7fb5-4a88-a31d-986e153f3823.png)

The usual script with blocking I/O execution time was around 10 mins (around 1500 consecutive HTTP requests)
[Async.ipynb] The project contains asynchronous realization of the same script with parallel I/O. It works ~10 times faster,
but unfortunately the server quickly starts to block HTTP requests due to their high frequency
