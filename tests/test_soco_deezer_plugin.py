#!/usr/bin/env python3
# coding: utf-8

"""Test of this plugin."""

import os
import unittest
import vcr
import deezer
from soco import SoCo
from soco_deezer_plugin.soco_deezer import DeezerSocoPlugin


def mkpath(name):
    rootdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(rootdir, 'requests', name)


class TestSocoDeezerPlugin(unittest.TestCase):

    @vcr.use_cassette(mkpath("setup.yaml"))
    def setUp(self):
        self.device = SoCo("192.168.1.18")
        self.device.clear_queue()
        self.dzs = DeezerSocoPlugin(self.device, username="user@home.com",
                                    service_type=519)

    @vcr.use_cassette(mkpath("test_with_ids.yaml"))
    def test_with_ids(self):
        self.dzs.add_track_to_queue('107028548')  # add track at the end of queue
        self.dzs.add_album_to_queue('85607212', position=1)  # add album at the begining

    @vcr.use_cassette(mkpath("test_with_deezer_python_objects.yaml"))
    def test_with_deezer_python_objects(self):
        client = deezer.Client()
        artist = client.search(query="Beirut", relation="artist")[0]
        album = artist.get_albums()[0]
        self.dzs.add_album_to_queue(album)

        track = client.advanced_search({'artist': "Lou Doillon", 'album': "Soliloquy",
                                        'track': "Widows"}, relation="track")[0]
        self.dzs.add_track_to_queue(track)


if __name__ == '__main__':
    unittest.main()
