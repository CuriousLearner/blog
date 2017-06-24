Multiple task executions on Celery ETA usage
============================================
:date: 2017-05-07 21:15
:author: Sanyam Khurana
:category: Experience
:slug: celery-eta-broker-transport-options
:tags: celery, python

If you find yourself in a use-case which needs to schedule tasks with celery at given time intervals, then you must read this, before this small tweak causes a havoc to your business.

This behavior occurs when the ETA of a task is greater that the visibility time out set up on your celery app object. Let me explain the case that happened with me.

According to my use case I use to schedule several tasks at different times of the day. There was a task that ran as a cron by celery beat every day at 12 AM to schedule tasks at different times of the day.

I noticed although the main task worked at 12 AM everyday and used to schedule the sub tasks, some of the sub tasks were triggered multiple times.

I was not able to find how was this even happening, until I came across this post: http://giovanni.bajo.it/post/46859364245/celery-and-scheduled-tasks

So, I updated my celery_config using the celery app object like:

.. code-block:: python

    celery.conf.update(
        # This config was overridden to prevent execution of tasks multiple
        # times in case ETA is greater than visibility timeout.
        # http://giovanni.bajo.it/post/46859364245/celery-and-scheduled-tasks
        BROKER_TRANSPORT_OPTIONS={
            'visibility_timeout': 86400
        },  # 1 day
    )

The comments depict exactly the issue and the link to blog post so anyone who is new to the project could know why this snippet was added.

I've just compiled it here so that it may help someone who faces similar issue and might be scratching their head, wondering if they made a logical error in their code.
