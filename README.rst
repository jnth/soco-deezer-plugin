Archived repository
===================

This plugin is not needed anymore.

Use this now::

    import deezer
    from soco.plugins.sharelink import ShareLinkPlugin
    from soco import SoCo

    dz = deezer.Client()

    albums = dz.search_albums("Ezra Collective")
    selected_album = albums[0]

    speaker = SoCo("192.168.1.17")
    speaker.clear_queue()

    share_link = ShareLinkPlugin(speaker)
    queue_position = share_link.add_share_link_to_queue(selected_album.link)
    speaker.play()


-----


SoCo Deezer plugin
==================

**SoCo Deezer plugin** is design to add Deezer_ tracks and albums into Sonos_ queue with SoCo_
(Sonos Controller).


Installation
------------

Install Soco Deezer plugin::

    python3 -m venv /path/of/venv
    source /path/of/venv/bin/activate
    pip install soco_deezer_plugin-0.3.0-py3-none-any.whl


Usage
-----

Example of use::

    from soco.discovery import any_soco
    from soco_deezer_plugin.soco_deezer import DeezerSocoPlugin

    device = any_soco()
    device.clear_queue()

    dzs = DeezerSocoPlugin(device, username="user@home.com", service_type=519)
    dzs.add_track_to_queue('107028548')  # add track at the end of queue
    dzs.add_album_to_queue('85607212', position=1)  # add album at the begining of queue
    dzs.add_playlist_to_queue('6036493264')  # add playlist

We can use the `deezer-python library`_ to search for an album and add it into Sonos queue::

    import deezer

    client = deezer.Client()
    artist = client.search_artists(query="Beirut")[0]
    album = artist.get_albums()[0]
    dzs.add_album_to_queue(album)


Contributors
------------
 - jnth (`@jnth <https://github.com/jnth>`_)
 - seby54 (`@seby54 <https://github.com/seby54>`_)


.. _SoCo: http://python-soco.com/
.. _Deezer: https://www.deezer.com
.. _Sonos: https://www.sonos.com
.. _deezer-python library: https://github.com/browniebroke/deezer-python
