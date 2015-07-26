# asiline
Convert command line dumps into formatted asciidoc passthroughs in a very noddy way

Possibly the worst code I have ever written.

I just needed a quickway to transform stuff like:


    ,,,,
    $ docker images --no-trunc | \
        grep $(docker inspect -f "-e {{.Image}}" $(docker ps -q))
    nginx   latest  42a3cf88f...  2 weeks ago  132.8 MB
    debian  latest  41b730702...  2 weeks ago  125.1 MB
    ,,,,

into:

    ++++
    <screen>
    $ <userinput>docker images --no-trunc | \
      grep $(docker inspect -f "-e {{.Image}}" $(docker ps -q))</userinput>
    nginx   latest  42a3cf88f...  2 weeks ago  132.8 MB
    debian  latest  41b730702...  2 weeks ago  125.1 MB
    </screen>
    ++++
