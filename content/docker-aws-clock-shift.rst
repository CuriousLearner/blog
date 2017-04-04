Dockerizing application that use AWS: Lessons learnt
####################################################
:date: 2017-04-04 12:43
:author: Sanyam Khurana
:category: Experience
:slug: docker-aws-clock-drift


I was recently working on containerizing the data pipeline I wrote as part of my work at Zopper. This pipeline uses `Boto3` to connect to Amazon SQS and SNS. While containerizing this pipeline, I managed to run 2 services that power the backward flow of the pipeline in 2 different containers while the forward flow pipeline was breaking because of some issue. I decided to look into it the next day. As usual my Mac got in sleep mode.

The very next day, I did ``docker-compose up``, I was expecting that 2 containers would run and I would start debugging the issue with the forward flow pipeline service; and it wasn't that easy.

As soon as the 2 containers were spawned, they were destroyed. After inspecting the logs, I realized I was getting an error while connecting to Amazon services as: 

.. code:: bash

    Amazon SQS SignatureDoesNotMatch: An error occurred (SignatureDoesNotMatch)
    when calling the GetQueueUrl operation: Signature expired)"

I immediately tried to verify the AWS keys for expiry, but they were correctly working. The services would run separately on a host correctly. So, I realized it has something to do with Docker.

This would happen if you're using any of the Amazon's servies and here is the how I came to know about the problem: I tried to manually run the container and then exec a shell in it; to know the date. I was astonished to see that my container was running at a time lag of around one day.

Amazon allows only a time discrepancy of 15 mins than the actual time. So, the solution to this problem is either match the time of the host to the container while running it. **But this can be a problem if the host's time is not correct**. So, you cannot **always** guarantee that it would work on all your Dev, Stage and Prod environments.

So, I set the TZ variable for running the container, and kept Time Zone as ``Asia/Kolkata`` inside the ``Dockerfile`` like:

.. code:: bash

    ENV TZ=Asia/Kolkata
    RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


This shall ensure that correct time zone reaches the container.

I was pretty close to the solution, but not in the 15 mins discrepancy window that Amazon allows. So, another issue was `clock drift <https://en.wikipedia.org/wiki/Clock_drift>`__. I immediately realized that my Mac was on sleep mode all the time. So, it was clearly ``Clock drift``. I restarted it and then everything was in place.

So, if you're using containers for services that use any Amazon service, ensure to set the Time Zone information explicitly. Let me know if you faced this kind of issue and how you solved it.
