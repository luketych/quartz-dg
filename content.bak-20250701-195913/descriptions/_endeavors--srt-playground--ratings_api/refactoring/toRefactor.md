Why is a test/data/ratings.sqlite and test/data/tradeSignals.sqlite file created when running tests? Shouldn't these be somewhere else?


Get rid of the tradeSignals stuff. I think the reason why it exists is that I started calling everyting "ratings" and started to migrate towards tradeSignals, but that is incorrect. Let's stick with "ratings."




### Get rid of hardFlags, soft flags.
I think the idea behind these flags was so that if a hook kept calling itself recursively we could set flags so that we could pass information internally. The issue with this is that fathers uses its own flags prefixed with $, so it gets confusing.

The other issue is that it creates a confusingly deep, nested call stack. This is a code smell. I think if I encounter a need for these flags again in the future I should probably consider if there is an alternative strategy.