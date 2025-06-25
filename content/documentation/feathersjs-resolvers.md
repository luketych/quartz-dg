## Resolvers[​](https://feathersjs.com/guides/whats-new#resolvers)

Combined with the new [schemas](https://feathersjs.com/guides/whats-new#official-schemas), resolvers allow to dynamically populate properties. It's a powerful tool that has many use cases from populating associations, securing queries or protecting secure data to easily setting values like the creation date or associated user. See the [chat guide](https://feathersjs.com/guides/basics/generator.html) for an example on how to set the user avatar, populate the user associated with a message and let users only modify their own data.

### Resolver Utility Hooks[​](https://feathersjs.com/guides/whats-new#resolver-utility-hooks)

Resolvers are powered by new hook utilities:

- [resolveData](https://feathersjs.com/api/schema/resolvers.html#data-resolvers) for incoming data.
- [resolveResult](https://feathersjs.com/api/schema/resolvers.html#result-resolvers) for results coming from databases or other services
- [resolveDispatch](https://feathersjs.com/api/schema/resolvers.html#safe-data-resolvers) for cleanly defining safe data for WebSocket / Real-time events.
- [resolveQuery](https://feathersjs.com/api/schema/resolvers.html#query-resolvers) for incoming query parameters

Read about the new hooks using the links, above. These new hook utils allow you to

- More cleanly manage properties on incoming records, query objects, and/or results
- Perform advanced validation beyond what's possible with JSON Schema.
- More efficiently write code for populating relational data (often faster than a normal ORM)
- Save yourself a lot of boilerplate compared to writing the three features, above, manually with hooks.

You can start using resolvers right away. The new [CLI](https://feathersjs.com/guides/basics/services.html#generating-a-service) generates them with all new services. Resolvers are one of the new tools provided in the new core package: [@feathersjs/schema](https://feathersjs.com/api/schema/).

You can read more about resolvers, [here](https://feathersjs.com/api/schema/resolvers.html).

### Hooks vs Resolvers[​](https://feathersjs.com/guides/whats-new#hooks-vs-resolvers)

At first glance, choosing where to put logic might seem complex. Should the feature go into a hook or a resolver? Here are some general guidelines to assist you:

- Data manipulation and **custom** validation probably fit best in a resolver.
- Adding or pulling in data from other sources will likely fit best in a resolver.
- Side effects that manipulate external data should go into a hook with few exceptions.