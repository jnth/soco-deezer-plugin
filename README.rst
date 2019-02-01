SoCo Deezer plugin
==================

**SoCo Deezer plugin** is design to add Deezer_ tracks and albums into Sonos_ queue with SoCo_
(Sonos Controller).


Installation
------------

Install Soco Deezer plugin::

    python3 -m venv /path/of/venv
    source /path/of/venv/bin/activate
    pip install soco_deezer_plugin-0.1.0-py3-none-any.whl


Usage
-----

Example of use::

    from soco import SoCo
    from soco_deezer_plugin.soco_deezer import DeezerSocoPlugin

    device = SoCo("192.168.255.255")  # ip of your Sonos device
    device.clear_queue()

    dzs = DeezerSocoPlugin(device, username="user@home.com", service_type=519)
    dzs.add_track_to_queue('107028548')  # add track at the end of queue
    dzs.add_album_to_queue('85607212', position=1)  # add album at the begining of queue

We can use the Deezer API to search for an album and add it into Sonos queue::

    import deezer

    client = deezer.Client()
    client.search(query="Beirut", relation="artist")[0]
    artist = client.search(query="Beirut", relation="artist")[0]
    album = artist.get_albums()[0]
    dzs.add_album_to_queue(album.id)



.. _SoCo: https://github.com/SoCo/SoCo
.. _Deezer: https://www.deezer.com
.. _Sonos: https://www.sonos.com