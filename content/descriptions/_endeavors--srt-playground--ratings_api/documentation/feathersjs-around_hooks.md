## More Powerful Hooks[​](https://feathersjs.com/guides/whats-new#more-powerful-hooks)

In Feathers Dove there are now two hook formats. One for `before`, `after`, and `error` hooks, and a new one for `around` hooks:

- **Before, after, and error hooks** have been Feathers' most-used API for years.
    - Are registered as `before`, `after`, or `error` hooks in the hook object.
    - Continue to work fully in Feathers Dove.
    - Are less powerful than the new "around" hooks, but visually simpler.
- **Around Hooks** are new in Feathers Dove.
    - Are registered in the `around` key of a hook object.
    - Are capable of handling before, after, and error logic, all within a single hook function.
    - Have a slightly different function definition than before, after, and error hooks
    - Are more powerful yet also more visually complex (The "after" part of each hook runs in reverse-registered order).

Let's compare the signature of the two types of hooks.

### Before, After, & Error Hooks[​](https://feathersjs.com/guides/whats-new#before-after-error-hooks)

Let's look at an example of the before/after/error hook format. These hooks receive the `context` as their only argument. They return either the `context` object or `undefined`.

ts

```
import type { HookContext } from '../../declarations'

export const myHook = async (context: HookContext) => {
  return context
}
```

You can learn more about before/after/error hooks, [here](https://feathersjs.com/api/hooks.html#before-after-and-error)

### Around Hooks[​](https://feathersjs.com/guides/whats-new#around-hooks)

Now let's see an around hook. An around hook receives two arguments: the `context` object and a `next` function.

ts

```
import type { HookContext, NextFunction } from '../../declarations'

export const myHook = async (context: HookContext, next: NextFunction) => {
  await next()
}
```

You can learn more about around hooks, [here](https://feathersjs.com/api/hooks.html#around)

### Registering Hooks[​](https://feathersjs.com/guides/whats-new#registering-hooks)

The hooks object now has a new `around` property, which is specifically for `around` hooks. Since around hooks have different function signatures, they are not interchangeable with before/after/error hooks.

ts

```
export const serviceHooks = {
  // `around` hook are new in Feathers Dove
  around: {
    all: [],
    find: [],
    get: [],
    create: [],
    update: [],
    patch: [],
    remove: []
  },
  // before/after/error hooks also continue to work
  before: {},
  after: {},
  error: {}
}
```

Learn more about registering hooks, [here](https://feathersjs.com/api/hooks.html#registering-hooks).

### When to use Around Hooks[​](https://feathersjs.com/guides/whats-new#when-to-use-around-hooks)

Using `around` hooks or `regular` hooks is mostly a matter of preference. There's no imminent need to rewrite all of your regular hooks into around hooks. Both hooks work together, as explained [here](https://feathersjs.com/api/hooks.html#hook-flow).

Starting with Dove, the CLI templates and new tooling features are written in `around` hooks. The around hooks simplify code in core tools because we can keep the logic for the entire hook flow (before, after, error) all in one file.

Here are a couple of examples of where `around` hooks work really well:

Data Caching Example

One great use case for `around` hooks is data caching. A caching hook typically has the following responsibilities:

- Check the cache for existing results. (before the service method executes)
- Push new results into the cache, once received. (after the service method executes)
- Handle and report errors which occur in the hook.

With regular hooks, a cache hook has to be split into three parts, one for each responsibility. Instead, a single `around` hook can handle everything on its own.

Below is an example of an overly-simple cache hook using JavaScript's `Map` API. Everything before `await next()` runs before the database call. Everything afterwards runs after the database call. You could also drop in a try/catch to handle possible errors.

ts

```
import type { HookContext, NextFunction } from '../../declarations'

export const simpleCache = new Map()

export const myHook = async (context: HookContext, next: NextFunction) => {
  // Check the cache for an existing record
  const existing = simpleCache.get(context.id)

  // If an existing record was found, set it as context.result to skip the database call.
  if (existing) {
    context.result = existing
  }

  await next()

  // Cache the latest record by its id
  simpleCache.set(context.result.id, context.result)
}
```

### Setup and Teardown Hooks[​](https://feathersjs.com/guides/whats-new#setup-and-teardown-hooks)

Feathers v5 Dove adds built-in support for app-level `setup` and `teardown` hooks. They are special hooks that don't run on the service level but instead directly on [app.setup](https://feathersjs.com/api/application.html#setupserver) or `app.listen` and [app.teardown](https://feathersjs.com/api/application.html#teardownserver). They allow you to perform some async logic while starting and stopping the Feathers server.

ts

```
app.hooks({
  setup: [connectMongoDB],
  teardown: [closeMongoDB]
})
```

Learn more about `setup` and `teardown` hooks, [here](https://feathersjs.com/api/hooks.html#setup-and-teardown)

## Rebuilt CLI[​](https://feathersjs.com/guides/whats-new#rebuilt-cli)

The new CLI is completely different under the hood, and very familiar on the surface. There are a few differences in file structure compared to apps generated with previous versions of the CLI.

### State of the Art[​](https://feathersjs.com/guides/whats-new#state-of-the-art)

When creating the new generator, we looked at open-source generators already available. We were very impressed with [Hygen](https://hygen.io/). It's absolutely impressive work, for sure, so we even wrote a custom generator to try it out. Then [@fratzinger](https://github.com/fratzinger) came up with the idea of a 100% TypeScript generator based on JavaScript template strings. We couldn't find an existing project, so we made one!

The new Feathers CLI is built on top of [Pinion](https://github.com/feathershq/pinion), our own generator with TypeScript-based templates. Instead of using some custom templating language, like Handlebars or EJS, Pinion uses Typed [Template Literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals), providing some wonderful benefits:

- No more mystery context. You always know the exact context of the templates and what helpers are available.
- It just works™ with existing npm packages. There's no need to make an EJS plugin for some custom helper using an obscure API. Just import the module and use it in your template.
- Integrates with all existing TypeScript tooling. Hover over a variable and inspect the context like you would any TS code.

Now that we have what we consider the best generator on the planet, we have some exciting plans for the Feathers CLI, which we will announce in the future.

You can read more about Pinion, [here](https://github.com/feathershq/pinion)

### Fully TypeScript[​](https://feathersjs.com/guides/whats-new#fully-typescript)

We have dramatically reduced the surface area for bugs to be introduced into the app. We've committed 100% to TypeScript, while making sure that you can still generate a JavaScript app.

When you select `JavaScript` to generate an app, the CLI works some magic under the hood by

- Compiling the `.ts` templates to JavaScript, in memory
- Formatting the JavaScript code with Prettier
- Writing clean `.js` to the file system.

For Feathers Maintainers, committing to TypeScript means we only contribute to a single set of templates. And they get magically compiled - on the fly - to plain JavaScript when you want it.

### Shared Types[​](https://feathersjs.com/guides/whats-new#shared-types)

We covered this [in more detail, earlier](https://feathersjs.com/guides/whats-new#typed-client), but it's worth briefly mentioning again. The new generator powers Shared Types for both the Feathers server and client. You can make your public-facing API easier to use and give developers a typed client SDK.

Read more about shared types, [here](https://feathersjs.com/guides/whats-new#typed-client).

### New App Structure[​](https://feathersjs.com/guides/whats-new#new-app-structure)

The file and folder structure of generated apps has changed a little bit. Here's an overview of the changes:

- Each service has its own schema and resolver file
- The service hooks are now found together with the service registration.
- The `src/models` folder no longer gets created, since [Feathers schemas](https://feathersjs.com/guides/whats-new#official-schemas) replace models.
- Each service has its own folder inside the `tests` folder.

You can learn more about the generated files in the [CLI guide](https://feathersjs.com/guides/cli/).

## The Future[​](https://feathersjs.com/guides/whats-new#the-future)

We are self-funded and community powered. In every way, Feathers has a solid foundation for a steady, stable future. How did we ever manage to build such a great framework without millions of dollars? Really, we have a wonderful, active community of contributors who share values of good API design, boilerplate elimination, and making development fun. This is rewarding for us!

We started in 2013 from a core architecture that's unique among frameworks - in **any** language. We offer the same API across multiple transports, which allows us all to build real-time, restful applications. The result is a robust, flexible framework that continues to be unique while showing its maturity. Feathers has made its way into enterprises that serve a large portion of the connected planet. With all of the new features in Feathers v5 (Dove), we're excited to build! And we're even more excited to see what you build!

We have a few more things to show off in the coming months. Stay tuned!

Enjoy the release! And come chat with us on [Discord](https://discord.gg/qa8kez8QBx) when you feel like it.

[Suggest changes to this page](https://github.com/feathersjs/feathers/edit/dove/docs/guides/whats-new.md)

Last updated: 5/19/25, 2:11 PM

Pager

[Previous page📄 tsconfig.json](https://feathersjs.com/guides/cli/tsconfig.html)

[Next pageMigration guide](https://feathersjs.com/guides/migrating.html)

![](https://feathersjs.com/logo.svg)feathers

- About
- [Philosophy](https://blog.feathersjs.com/why-we-built-the-best-web-framework-you-ve-probably-never-heard-of-until-now-176afc5c6aac)
- [Comparison](https://feathersjs.com/comparison)
- [Ecosystem](https://github.com/feathersjs/awesome-feathersjs)

- Learn
- [Guides](https://feathersjs.com/guides/)
- [API](https://feathersjs.com/api/)
- [Blog](https://blog.feathersjs.com/)

- Ecosystem
- [Become a Backer](https://github.com/sponsors/daffl)
- [Find Help](https://feathersjs.com/help/)
- [Github Issues](https://github.com/feathersjs/feathers/issues)

Released under the MIT License.

Copyright © 2012-2025 FeathersJS contributors