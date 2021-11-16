## How to run the CLI app
- Run `sh start-cli.sh` to run the CLI app.
- `HOUSE_ACCOUNT` is `"HOUSE_ADDRESS"`, configured in `jobcoin.config`

## How to run tests
- Run `sh run-tests.sh` to run tests under `./tests` directory

## What DOESN'T this version of CoinMixer do?
- Revert transaction on service failure
- Persist `pseudoAddress -> realAddresses` mapping is in memory only, so once the cli app terminates the mapping will be erase.

## Future work
- Mapping persistance (redis or database) can be a good improvement in the future
- Horizontally scale the service by sharding pseudo keys
- Convert fund/number to string and calculate it digit by digit / decimal by decimal for better precision
- Deduct commission


## Architecture Diagram

![Jobcoin Mixer Design](https://user-images.githubusercontent.com/7697903/142051892-47e10cf5-7b09-4467-93e4-afa6a789f20d.png)
