# Async request data gathering

There are times it is needed to define some tasks in a run forever async loop
and the cumulative result of all these tasks is needed. We had such a problem
to implement bale bots here in SADAD. In these situations the loop.run_until_complete()
is not practical because the loop can not be stopped. 
Here I suggest a way to accomplish   such task by gathering the data in a bound method of an object.
Take a look at test_async_request to understand the problem. Of course here the
loop is stoped in the sake of the test. However in the real-world situations the
loop can not be stoped. To implement the situation here, I use a flask HTTP mockup
server and finally I write the result of all the requests to this server to an
excel file. 

