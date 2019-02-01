#!/usr/bin/env python3
# coding: utf-8

"""Deezer plugin for Sonos."""


from soco.plugins import SoCoPlugin
from soco.music_services import MusicService
from soco.music_services.accounts import Account
from soco.compat import quote_url
from soco.data_structures import (DidlResource, DidlAudioItem, DidlAlbum,
                                  to_didl_string)
import deezer


prefix_id = {
    'track': '00032020',
    'album': '0004206c',
    'user-albums': '1008006c',
}


class DeezerSocoPlugin(SoCoPlugin):
    def __init__(self, soco, username, service_type):
        super(DeezerSocoPlugin, self).__init__(soco)

        account = Account()
        account.username = username
        account.service_type = service_type

        self.__ms = MusicService('Deezer', account=account)
        self.__dz = deezer.Client()

    @property
    def name(self):
        return 'Deezer'

    def __valid_queue_position(self, position):
        if position is None:
            position = len(self.soco.get_queue()) + 1  # at the end...
        elif position < 0:
            position = 1  # at the begining...
        return position

    def __add_uri_to_queue(self, uri, didl, position):
        """Add URI to queue."""
        meta = to_didl_string(didl)
        self.soco.avTransport.AddURIToQueue(
            [('InstanceID', 0),
             ('EnqueuedURI', uri),
             ('EnqueuedURIMetaData', meta),
             ('DesiredFirstTrackNumberEnqueued', position),
             ('EnqueueAsNext', 1)])

    def add_track_to_queue(self, track_id, position=None):
        """Add a track into Sonos queue.

        :param track_id: Deezer track identifier
        :type track_id: str
        :param position: Position into the queue, None to the end of the queue.
        :type position: Optional[int]
        """
        track_id = str(track_id)

        dz_track = self.__dz.get_track(track_id)
        album_id = dz_track.get_album().id

        position = self.__valid_queue_position(position)

        prefix_item_id = prefix_id.get('track')
        prefix_parent_id = prefix_id.get('album')

        item_id = quote_url(f"tr:{track_id}")
        uri = f"x-sonos-http:{item_id}?sid=2&amp;sn=0"

        resource = DidlResource(protocol_info="sonos.com-http:*:audio/mp4:*",
                                uri=uri)

        didl = DidlAudioItem(item_id=f"{prefix_item_id}{item_id}",
                             parent_id=f"{prefix_parent_id}album-{album_id}",
                             title=dz_track.title,
                             desc=self.__ms.desc,
                             resources=[resource, ],
                             restricted=False)
        self.__add_uri_to_queue(uri, didl, position)

    def add_album_to_queue(self, album_id, position=None):
        """Add an album into Sonos queue.

        :param album_id: Deezer album identifier
        :type album_id: str
        :param position: Position into the queue, None to the end of the queue.
        :type position: Optional[int]
        """
        album_id = str(album_id)

        dz_album = self.__dz.get_album(album_id)
        artist_id = dz_album.get_artist().id

        position = self.__valid_queue_position(position)

        prefix_item_id = prefix_id.get('album')
        prefix_parent_id = prefix_id.get('user-albums')

        item_id = f"{prefix_item_id}album-{album_id}"
        uri = f"x-rincon-cpcontainer:{item_id}"

        resource = DidlResource(protocol_info="x-rincon-cpcontainer:*:*:*", uri=uri)

        didl = DidlAlbum(item_id=item_id,
                         parent_id=f"{prefix_parent_id}user-albums-{artist_id}",
                         title=dz_album.title,
                         desc=self.__ms.desc,
                         resources=[resource, ],
                         restricted=False)
        self.__add_uri_to_queue(uri, didl, position)
