Authenticating And Getting Info From Explara API
################################################
:date: 2016-01-13 00:53
:author: Sanyam Khurana
:category: Experience
:slug: authenticating-and-getting-info-from-explara-api

PyDelhi is organizing a mini PyCon this year with the name PyDelhi Conf.
And we all are having a great time working behind the scenes to make it
a success. I'm contributing to building up the website for the confrence
(conference.pydelhi.org).

So, there was this task of fetching the no. of tickets left for the
conference from explara and displaying it on the website. I picked it up
and had a look at Explara API. And Bingo! I noticed the tickets
end-point, which would contain the remaining tickets in the JSON format.

| I got into reading about accessing api. There are two methods, one is for user access and another one is for app access.

|  Since user access is good enough for the kind of work we're thinking to do, I decided to go by first method and generated the access token from my personal account and made a test event for testing purpose.

After several tries and errors, I was not able to authenticate the API.
It was either giving me 401 or 403. Then after a day, I contacted
Anuvrat & Saurabh on IRC. Also, I reached to Rishabh. Rishabh told me
that he was able to authenticate for the app method which uses OAuth2.
Then he tried for the user method and told me. And there I am.

Doing a blunder. The Authorization token in the header would be
preceeded by 'Bearer' so the header would be:

| Key: Authorization
|  Value: Bearer <YOUR\_API\_KEY>

And then voila, it was authorized. Soon to my surprise, it was giving me
E007 which is a custom status code of explara which implies that eventId
is incorrect. I just clicked on edit on my event and in the url I found
something like

eid/116168

And I thought, yeah, that's the eventId I started passing it. But always
I was getting E007. Rishabh was also trying but he was also not able to
get the response 200.

At around 12.30 AM Rishabh told me that he's going to sleep, and would
try tomorrow. But I decided to try more. I googled on how to find the
eventId of explara event, but no concrete answer. I kept on trying, and
then decided to have a look at other methods API is offering.

| There was an endpoint to get all events which require no parameters to be passed. I hit that end-point and there I was.
|  I got the event details as JSON and find the eventId of the event I created.

| Now I took that eventId and hit the ticket end point to get the details, but there was always E007 error. I tried different methods to pass eventId parameter. I tried to pass it in a JSON body, but no success.
|  Then I tried x-www-form-urlencoded and then the error code changed. I quickly searched, and got to know that I need to change the content-type of my request in the header.

I changed the header and added:

|  Key: Content-Type
|  Value: application/x-www-form-urlencoded

and bingo! I got the ticket status

| Now I just wrote a simple flask script to issue the request and then display the tickets left in JSON format.
|  And here it is:

https://github.com/CuriousLearner/explara-ticket-status
|  Also forked to PyDelhi:
https://github.com/PyDelhi/explara-ticket-status

At 3:05 AM the task was completed, and I was pretty much happy about it.
A good learning experience and I hope that someone would find it useful
while working with explara api. Lack of examples caused more time on
this than was really needed.
