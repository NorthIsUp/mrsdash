import unittest2

from mrsdash.graphite import Graph
from mrsdash.graphite import Series


class TestGraph(unittest2.TestCase):
    def setUp(self):
        self.config = {'GRAPHITE_BASE_URL': "http://localhost:9090/"}

    def tearDown(self):
        pass

    def test_new_graph(self):
        with self.assertRaises(TypeError):
            Graph()

        with self.assertRaises(AttributeError):
            Graph("1h")

        with self.assertRaises(KeyError):
            Graph({}, "foo")

        g = Graph({'GRAPHITE_BASE_URL': "foo"}, "1h")
        gd = g.get_dashboard(10, 10)
        ed = {'span': 12, 'title': None, 'height': 10, 'width': 10, 'img_src': 'foo/render?width=10&yMin=0&from=-1hour&height=10&', 'legend': ''}
        self.assertDictEqual(ed, gd)

    def test_copy(self):
        g = Graph({'GRAPHITE_BASE_URL': "foo"}, "1h")
        g.add_series("foo.bar")
        p = Graph(g)
        self.assertListEqual([{'target': 'foo.bar'}], p._series)


class TestSeries(unittest2.TestCase):
    """docstring for Series"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_new_series(self):
        s = Series("foo.bar")
        self.assertEqual("foo.bar", s)
        s = Series("foo.bar", ("sumSeries"))
        self.assertEqual("sumSeries(foo.bar)", str(s))
        s = Series("foo.bar", ("alias", "badass"))
        self.assertEqual('alias(foo.bar,"badass")', str(s))

    def test_add_raw_function(self):
        s = Series("foo.bar")
        s.add_raw_function("alias", ("badass"))
        self.assertEquals('alias(foo.bar,"badass")', str(s))
