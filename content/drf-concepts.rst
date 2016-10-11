Learning Django REST Framework
##############################
:date: 2016-10-03 12:27
:author: Sanyam Khurana
:category: learning
:slug: drf-concepts
:tags: django, python, drf


I'm currently reading the documentation of Django REST Framework; and in this post I'll mention few terms I've encountered and quick summary of what is it about so that I can refer to this later.

Note: I'm making these with reference to mostly JSON data format for ease of understanding. But your RESTful API may support other data formats.

Django REST Framework
---------------------

Serialization
-------------

It is the process of converting complex data type (Objects) to primitive data type (``dict``/``list``) so that it can be passed as ``JSON``. Notice that it is not about converting object to ``JSON`` format, but objects to a primitive data type such as ``dict``/``list``.

Renderers
---------

Once you have the primitive data type (``dict``/``list``), it is the responsibility of renderer to dump it as ``JSON`` to the client. ( or in whatever data format the client wants data which is depicted by ``Accept`` header). It is intermediate representation of template & contenxt; and converts final byte stream that is served to the client.

Parsers
-------

When you receive a request on your API, the parser converts the ``request.data`` into primitive data type (such as ``dict``/``list``) which then can be deserialized as an object. The content that your API permits is depicted by ``Content-Type`` header and then appropriate Parser class can be used.

Content Negotiation
-------------------

It is the process of selecting the best representation format depending on the Rederers available in your API. This phase is partly client driven; and partly server-driven.
The renderer is selected based on client's ``Accept`` header and also by the priority order in which Renderers are available in your API.


I'll update this post later with more important things :)
