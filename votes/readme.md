# How the voting gonna happend and how we are avoiding multiple db calls at once and how we will retrieve data fast?
Let's consider we can spin multiple servers.

A peron comes and vote . We can't make continuos db calls as it would exhaust the db. We will product one message in the queue and consumer will make the changes.
And for faster retrieval we will use redis and we will cache the items their.
We can use a in memory structure but in case of multiple servers, the cache will not get shared then. So we will be using distributed caching. Where one server will cache results in the redis and multiple servers can also use it.

Basically making the whole design stateless. Even if server crashes , it will not delete the cache.

### how redis can benifit here more?
Even if we maintain an inmemory object for storing cache, suppose we have multiple servers and the admin and voter are logged in. Voting will be visible to admin in realtime. So what if voter and admin join to different servers? Different servers means they will not know the websocket client ids and in which client to send the ids so admin will not be able to see.
An easy approach here is leverage the redis pubsub. Every websockets will publish to the redis pubsub and admin will receive all the updates.

Redis
server A ws server -> voter1, voter2, admin
server B ws server -> voter3, voter5

# But why are we using in memory structure? A stateful server
I know redis is something more than a cache. But since a single server is their and it is not launched for usage by people thats why I am using an in memory object for maintaining the cache. When the sever will crash we can recreate the vote object from the database.
Here we don't need the pubsub as well since all the voter will join to single ws instance

### Goal
[] Consume project ready payload 
[] On vote add user_id to the cache and produce event for adding to database
[] Check whether an user voted or not
[] Bringing vote in the cache