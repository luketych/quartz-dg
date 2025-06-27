### New App Structure[​](https://feathersjs.com/guides/whats-new#new-app-structure)

The file and folder structure of generated apps has changed a little bit. Here's an overview of the changes:

- Each service has its own schema and resolver file
- The service hooks are now found together with the service registration.
- The `src/models` folder no longer gets created, since [Feathers schemas](https://feathersjs.com/guides/whats-new#official-schemas) replace models.
- Each service has its own folder inside the `tests` folder.


## Official Schemas[​](https://feathersjs.com/guides/whats-new#official-schemas)

Feathers Dove (v5) introduces new, official tools for data validation in the new core package, [@feathersjs/schema](https://feathersjs.com/api/schema/). This same package includes schema-based resolvers, which you'll learn about in the next section. Schemas are powered by JSON Schema (an IETF standard) which makes them powerful and portable.

### Schema-Driven Types[​](https://feathersjs.com/guides/whats-new#schema-driven-types)

One of the problems we wanted to avoid was the need to define schemas and/or types in multiple places. If we had a motto/slogan for types, it would be

**"Define it once, use it everywhere."**

So in Feathers Dove, when you create a schema, it dynamically generates validation and proper TypeScript types. You can use the powerful and concise [TypeBox schema format](https://feathersjs.com/api/schema/typebox.html) or [plain JSON schema](https://feathersjs.com/api/schema/schema.html).

### Configuration Schemas[​](https://feathersjs.com/guides/whats-new#configuration-schemas)

If you've ever experienced pains of deploying to production, you'll appreciate this feature. When your app starts in production, all of your configuration and environment variables are checked against the configuration schema. The app won't start if the schema validation fails. This keeps bugs from missing environment variables from showing up in production days to weeks after deployment.

Configuration schemas also produce TypeScript types, so the [TypeScript improvements](https://feathersjs.com/guides/whats-new#new-typescript-benefits) in Feathers Dove include typed configuration lookup for `app.get()` and `app.set()`. It's really convenient.

Read more about configuration schemas, [here](https://feathersjs.com/api/configuration.html#configuration-schema)