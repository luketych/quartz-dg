### Setup and Teardown Hooks[​](https://feathersjs.com/guides/whats-new#setup-and-teardown-hooks)

Feathers v5 Dove adds built-in support for app-level `setup` and `teardown` hooks. They are special hooks that don't run on the service level but instead directly on [app.setup](https://feathersjs.com/api/application.html#setupserver) or `app.listen` and [app.teardown](https://feathersjs.com/api/application.html#teardownserver). They allow you to perform some async logic while starting and stopping the Feathers server.

ts

```
app.hooks({
  setup: [connectMongoDB],
  teardown: [closeMongoDB]
})
```


### Setup and teardown[​](https://feathersjs.com/api/hooks.html#setup-and-teardown)

A special kind of application hooks are [app.setup](https://feathersjs.com/api/application.html#setupserver) and [app.teardown](https://feathersjs.com/api/application.html#teardownserver) hooks. They are around hooks that can be used to initialize database connections etc. and only run once when the application starts or shuts down. Setup and teardown hooks only have `context.app` and `context.server` available in the hook context.

ts

```
import { MongoClient } from 'mongodb'

app.hooks({
  setup: [
    async (context: HookContext, next: NextFunction) => {
      // E.g. wait for MongoDB connection to complete
      await context.app.get('mongoClient').connect()
      await next()
    }
  ],
  teardown: [
    async (context: HookContext, next: NextFunction) => {
      // Close MongoDB connection
      await context.app.get('mongoClient').close()
      await next()
    }
  ]
})
```