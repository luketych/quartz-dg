Why is a test/data/ratings.sqlite and test/data/tradeSignals.sqlite file created when running tests? Shouldn't these be somewhere else?


Get rid of the tradeSignals stuff. I think the reason why it exists is that I started calling everyting "ratings" and started to migrate towards tradeSignals, but that is incorrect. Let's stick with "ratings."