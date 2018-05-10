#!/usr/bin/env python
"""Run tests on a selection of https://w3id.org/arm redirects."""

import argparse
import logging
import requests
import unittest
from urllib.parse import urljoin

BASE = 'http://localhost:8080'
W3ID = 'https://w3id.org'
LD4P = 'https://ld4p.github.io'


class TestRedirects(unittest.TestCase):

    def req(self, path, accept=None, code=None, redirect=None):
        """Request BASE/path."""
        headers = {}
        if accept is not None:
            headers['accept'] = accept
        uri = urljoin(BASE, path)
        r = requests.head(uri, headers=headers, allow_redirects=False)
        status_code = r.status_code
        if 'location' in r.headers:
            location = r.headers['location']
        else:
            location = None
        logging.info("Request %s --%d--> %s" % (uri, status_code, location))
        if code is not None:
            self.assertEqual(status_code, code)
        if redirect is not None:
            self.assertEqual(location, redirect)


    def test_bad(self):
        self.req('/arm/BAD',
                 code=404)

    def test_generic(self):
        self.req('/arm/',
                 redirect=urljoin(LD4P,'/arm/'))

    def test_award(self):
        # Unversioned URIs --> versioned URIs
        self.req('/arm/award/ontology',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/award/ontology/0.1/'))
        self.req('/arm/award/ontology/award.rdf',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/award.html',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/award/ontology/0.1/award.html'))
        # Versioned URIs -> content
        self.req('/arm/award/ontology/0.1/award.rdf',
                 redirect=urljoin(LD4P, '/arm/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/0.1/award.html',
                 redirect=urljoin(LD4P, '/arm/award/ontology/0.1/doc/lode/award.html'))
        self.req('/arm/award/ontology/0.1/',
                 code=303,
                 redirect=urljoin(LD4P, '/arm/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/0.1/', accept='application/xml+rdf',
                 code=303,
                 redirect=urljoin(LD4P, '/arm/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/0.1/', accept='text/html',
                 code=303,
                 redirect=urljoin(LD4P, '/arm/award/ontology/0.1/doc/lode/award.html'))

    def test_core(self):
        self.req('/arm/core/ontology',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/core/ontology/0.1/'))

    def test_activity(self):
        # WIERD PATTERN!
        self.req('/arm/core/activity',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/core/activity/0.1/'))
        self.req('/arm/core/activity/0.1/activity.rdf',
                 redirect=urljoin(LD4P, '/arm/core/ontology/0.1/activity.rdf'))
        self.req('/arm/core/activity/0.1/activity.html',
                 redirect=urljoin(LD4P, '/arm/core/ontology/0.1/doc/lode/activity.html'))

    def test_origin(self):
        self.req('/arm/core/vocabularies/origin/0.1/',
                 redirect=urljoin(LD4P, '/arm/core/vocabularies/origin/0.1/origin.rdf'))


parser = argparse.ArgumentParser(description='Test ARMredirects.')
parser.add_argument('--live', '-l', action='store_true',
                    help='run against live site instead of %s' % BASE)
parser.add_argument('--verbose', '-v', action='store_true',
                    help='show requests and responses')
args = parser.parse_args()
if args.live:
    BASE = 'https://w3id.org'
logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)
unittest.main()

