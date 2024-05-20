### Todo
[] Create variety of thumbnails using genai
[] Post it 
[] Create Poll
[] Read and Write replicas
[] Use websocket and scale it
[] Join the services using a api gateway
[] Connect a logging and metrics dashboard

# Dividing the auth and user service
* We can separate the auth and user service. Auth for only authentication and user for managing details.
* Whenerver a new user signed in , publish an event and user will catch it and store it in the database.
* Expose crud endpoints from user, so that it can be consumed for mutating the details

# Dividing the thubmnail service
* In thumbnail service, we are doing two tasks
    * CRUD
    * Thumbnail Generation using GenAI which is a long running task
* We can implement the whole this in two ways ->
    * Dividing it into two service -> CRUD and Generation(long running). CRUD will take care of the user side and generation will complete and make internal service to service calls to the
    CRUD service
    * Same service but using celery workers.
* Using the same service pattern using celery
