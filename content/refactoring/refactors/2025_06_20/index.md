## Separate Benzinga fetch function

Currently, the Benzinga fetch function is embedded in the fetchRatings function. This is not ideal as it makes the code more difficult to understand and maintain. It also makes it more difficult to test the Benzinga fetch function in isolation.