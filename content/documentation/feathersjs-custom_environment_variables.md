Custom Environment Variables
While node-config used for application configuration recommends to pass environment based configuration as a JSON string in a single NODE_CONFIG environment variable, it is also possible to use other environment variables via the config/custom-environment-variables.json file which looks like this by default:


{
  "port": {
    "__name": "PORT",
    "__format": "number"
  },
  "host": "HOSTNAME",
  "authentication": {
    "secret": "FEATHERS_SECRET"
  }
}
This sets app.get('port') using the PORT environment variable (if it is available) parsing it as a number and app.get('host') from the HOSTNAME environment variable and the authentication secret to the FEATHERS_SECRET environment variable.

tip

See the node-config custom environment variable documentation for more information.

Dotenv
To add support for dotenv .env files run


npm install dotenv --save
And update src/app.ts as follows:


// dotenv replaces all environmental variables from ~/.env in ~/config/custom-environment-variables.json
import * as dotenv from 'dotenv'
dotenv.config()

// or for ES6

import 'dotenv/config';

import configuration from '@feathersjs/configuration'
important

dotenv.config() needs to run before import configuration from '@feathersjs/configuration'