import unittest2

from mrsdash.lib.graphite import Graph
from mrsdash.lib.graphite import Deploy
from mrsdash.lib.graphite import Series


class TestGraph(unittest2.TestCase):
    def setUp(self):
        self.config = {'GRAPHITE_BASE_URL': "http://localhost:9090/"}

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


class TestDeploly(unittest2.TestCase):
    def test_new_series(self):
        s = Deploy("foo.bar")
        se = 'color(lineWidth(drawAsInfinite(alias(foo.bar,"Deploy")),2),"blue")'
        self.assertEqual(se, str(s))
        s = Deploy("foo.bar", ("sumSeries"))
        se = 'color(lineWidth(drawAsInfinite(alias(sumSeries(foo.bar),"Deploy")),2),"blue")'
        self.assertEqual(se, str(s))
        s = Deploy("foo.bar", ("alias", "badass"))
        se = 'color(lineWidth(drawAsInfinite(alias(alias(foo.bar,"badass"),"Deploy")),2),"blue")'
        self.assertEqual(se, str(s))

    def test_add_raw_function(self):
        #TODO: should this fail if a function like alias is applied twice?
        s = Deploy("foo.bar")
        s.add_raw_function("alias", ("badass"))
        se = 'alias(color(lineWidth(drawAsInfinite(alias(foo.bar,"Deploy")),2),"blue"),"badass")'
        self.assertEquals(se, str(s))
