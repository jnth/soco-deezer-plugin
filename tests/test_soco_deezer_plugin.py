#!/usr/bin/env python3
# coding: utf-8

"""Test of this plugin."""

import unittest
import deezer
from soco.discovery import discover
from soco_deezer_plugin.soco_deezer import DeezerSocoPlugin


def get_coordinator_device():
    return [device for device in discover() if device.is_coordinator][0]


class TestSocoDeezerPlugin(unittest.TestCase):

    def setUp(self):
        self.device = get_coordinator_device()
        self.device.clear_queue()
        self.dzs = DeezerSocoPlugin(self.device, username="user@home.com",
                                    service_type=519)

    def test_with_ids(self):
        self.dzs.add_track_to_queue('107028548')  # add track at the end of queue
        self.dzs.add_album_to_queue('85607212', position=1)  # add album at the begining
        self.dzs.add_playlist_to_queue('6036493264')  # add playlist

    def test_with_deezer_python_objects(self):
        client = deezer.Client()
        artist = client.search_artists(query="Beirut")[0]
        album = artist.get_albums()[0]
        self.dzs.add_album_to_queue(album)

        track = client.search(artist="Lou Doillon", album="Soliloquy", track="Widows")[0]
        self.dzs.add_track_to_queue(track)

        playlist = client.get_playlist(6036493264)
        self.dzs.add_playlist_to_queue(playlist)


if __name__ == '__main__':
    unittest.main()
