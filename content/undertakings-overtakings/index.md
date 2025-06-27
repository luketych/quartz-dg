Overtakings vs Undertakings

**Overtakings** start with a seed, and then over time take over the entire project.
Imagine the imagery of your codebase as a petri dish. Something starts as a small seed. Then it starts to grow tall, and slowly overtake the entire petri dish. 

<u>Examples</u>:
  Changing coding style, or incorporating a new library into a project, for example, a datetime library, but we don't want to go all-in yet. So we start small, and over time it might take over more and more of our project.


**Undertakings** are more difficult. The imagery is something that is forming underneath the petri-dish, flat-earth. It might be more closely symbolic of a glacier or tectonic plate.

<u>Examples</u>:
- Databases,
- Testing Methodologies

These are essential to our projects, but unlike the examples of Overtakings, they cannot be seen as a small seed that slowly grows. It's more something essential that shakes the earth above it.

One might consider creating a fork, if the change is large enough, or a branch, which will be heavy, and require a heavier merge in the future.

## Additional Interpretation

This framework maps well to several established software engineering concepts:

**Overtakings parallel:**
- **Strangler Fig Pattern**: Gradually replacing legacy systems by wrapping and slowly consuming them
- **Feature Flags**: Starting with a small subset of users before full rollout
- **Adapter Pattern**: Introducing new interfaces that coexist with old ones during transition
- **Progressive Enhancement**: Adding capabilities layer by layer

**Undertakings parallel:**
- **Big Bang Refactoring**: Complete system rewrites that require careful planning
- **Infrastructure as Code**: Foundational changes to deployment and operations
- **Architectural Decision Records (ADRs)**: Documenting consequential choices that affect the entire system
- **Conway's Law**: How organizational structure mirrors system architecture

The key insight is recognizing which type of change you're making. Overtakings allow for reversibility and gradual adoption - you can always prune the growth. Undertakings require commitment and careful planning - once the tectonic plates shift, reversal is costly.

For teams: Overtakings can often be driven by individuals or small groups. Undertakings require organizational buy-in and coordinated effort across the entire team.

For risk management: Overtakings fail gracefully (the seed doesn't grow). Undertakings can cause earthquakes if not properly executed.