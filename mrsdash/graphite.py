from urllib import quote
from urllib import urlencode
from time_helpers import parse_time
from helpers import accepts
from copy import deepcopy


class Series(str):
    def __new__(cls, series, *funcs):
        return super(Series, cls).__new__(cls, series)

    def __init__(self, series, *funcs):
        super(Series, self).__init__()
        self._functions = []
        self._applied = series
        for f in funcs:
            if isinstance(f, basestring):
                f = (f,)
            self._add_raw_function(*f)

    def __str__(self):
        return self._applied

    # TODO: add functions from http://graphite.readthedocs.org/en/1.0/functions.html
    def add_raw_function(self, function, *args):
        self._add_raw_function(function, *args)
        self._applied = self.apply_functions()
        return self

    def _add_raw_function(self, function, *args):
        """No verification on adding a raw function"""
        self._functions.append((function, args))
        return self

    def apply_functions(self):
        self._applied = self._apply_functions(*self._functions)
        return self._applied

    def _apply_functions(self, *functions):
        if not functions:
            return self

        recur = self._apply_functions(*functions[0:-1])

        f_name, f_args = functions[-1]
        s_args = ",".join(map(lambda x: '"%s"' % x if isinstance(x, str) else str(x), f_args))
        inner = ",".join(filter(lambda x: True if x else False, (recur, s_args)))

        return "{func}({inner})".format(func=f_name, inner=inner)

s = Series("foo.bar")
print s
s = Series("bar.foo", ("sum", 1))
print s.apply_functions()
print s._functions


class Graph(object):
    """docstring for Graphite"""
    def __init__(self, config, time):
        super(Graph, self).__init__()

        self._base_url = config['GRAPHITE_BASE_URL']
        self._deploys = config['GRAPHITE_DEPLOYS']
        self._hide_grid = False
        self._hide_legend = False
        self._line_mode = None
        self._line_width = None
        self._series = []
        self._pie_chart = False
        self._stacked = False
        self._time = time
        self._title = None
        self._display_title = True
        self._display_vtitle = False
        self._vtitle = None
        self._y_max = None
        self._y_min = 0
        self._time_shift = None
        self._span = 12
        self._threshold = []

    # TODO: add a horizontal line method
    @accepts(int, self=True)
    def add_threshold(self, threshold, label=None, color=None):
        print label, color
        args = ('threshold', filter(lambda x: True if x else False, (label, color)))
        print args
        self.add_series(threshold, *args)
        return self

    def prototype(self):
        return deepcopy(self)

    # TODO add all methods from http://graphite.readthedocs.org/en/1.0/url-api.html
    @accepts(int, self=True)
    def set_span(self, span):
        self._span = span
        return self

    @accepts(str, self=True)
    def set_time(self, time):
        self._time = time
        return self

    @accepts(str, self=True)
    def set_time_shift(self, time):
        self._time_shift = time
        return self

    @accepts(str, self=True)
    def set_title(self, title):
        self._title = title
        return self

    @accepts(str, self=True)
    def set_v_title(self, vtitle):
        self._vtitle = vtitle
        return self

    @accepts(str, self=True)
    def set_line_mode(self, mode):
        self._line_mode = mode
        return self

    @accepts(bool, self=True)
    def hide_legend(self, hide):
        self._hide_legend = bool(hide)
        return self

    @accepts(bool, self=True)
    def hide_grid(self, hide):
        self._hide_grid = bool(hide)
        return self

    @accepts(int, self=True)
    def set_line_width(self, width):
        self._line_width = int(width)
        return self

    @accepts(bool, self=True)
    def display_stacked(self, display):
        self._stacked = bool(display)
        return self

    @accepts(bool, self=True)
    def display_title(self, display):
        self._display_title = bool(display)
        return self

    @accepts(bool, self=True)
    def display_vtitle(self, display):
        self._display_vtitle = bool(display)
        return self

    @accepts(bool, self=True)
    def display_pie_chart(self, display):
        self._pie_chart = bool(display)
        return self

    # Set y_min to 'null' to unlock from zero
    def set_y_min(self, y_min):
        self._y_min = y_min
        return self

    @accepts(int, self=True)
    def set_y_max(self, y_max):
        self._y_max = y_max
        return self

    # Add a metric to the current Graphite object. For Graphite, you can call this
    # method multiple times to stack multiple metrics together in one image.
    def add_series(self, series, *args, **kwargs):
        series = {'target': Series(series, *args).apply_functions()}
        if 'color' in kwargs and kwargs['color']:
            series['color'] = kwargs['color']
        if 'prepend' in kwargs and kwargs['prepend']:
            self._series.insert(0, series)
        else:
            self._series.append(series)
        return self

    # Include vertical deploy lines over any metrics included in the image.
    @accepts(bool, self=True)
    def show_deploys(self, show=True):
        if show:
            for deploy in self._deploys:
                target = "alias(drawAsInfinite(deploy['target']), 'Deploy: deploy['title']')"
                self.add_series(target, deploy['color'], True)
        return self

     # Convert Dashboard time period to a value usable by Graphite URLs.
    def get_time_param(self):
        m = parse_time(self._time)
        return '-' + m[0] + m[1]

    # Get Graphite image URL that will display all of the added metrics and deploy lines.
    def get_image_url(self, width=800, height=600, stand_alone=False):
        p = {
            'from': self.get_time_param(),
            'width': width,
            'height': height,
        }

        if self._display_title and self._title:
            p['title'] = self._title

        if self._display_vtitle and self._vtitle:
            p['vtitle'] = self._vtitle
            p['hideaxes'] = 'false'

        if self._hide_legend and not stand_alone:
            p['hideLegend'] = self._hide_legend

        if self._hide_grid:
            p['hideGrid'] = self._hide_grid

        if self._line_width:
            p['lineWidth'] = self._line_width

        if self._stacked:
            p['areaMode'] = 'stacked'

        if self._y_min is not None:
            p['yMin'] = self._y_min

        if self._y_max is not None:
            p['yMax'] = self._y_max

        if self._line_mode is not None:
            p['lineMode'] = self._line_mode

        if self._pie_chart:
            p['graphType'] = 'pie'

        targets = []
        colors = []

        for m in self._series:
            targets.append('target=' + m['target'])  # shouldn't need to quote this
            if 'color' in m and m['color']:
                colors.append(quote(m['color']))

        fmt = {
            'base_url': self._base_url,
            'query': urlencode(p),
            'targets': '&'.join(targets),
            'colors': '&colorList=' + ','.join(colors) if colors else '',
        }

        ret = "{base_url}/render?{query}&{targets}{colors}".format(**fmt)
        return ret

    def get_dashboard(self, width, height, html_legend=""):
        if html_legend:
            legend = '<p class="html_legend" style="width: {width}px">{html_legend}</p>'.format(width=width, html_legend=html_legend)
        else:
            legend = ""

        fmt = {
            'title': self._title,
            'span': self._span,
            'width': width,
            'height': height,
            'img_src': self.get_image_url(width, height),
            'legend': legend,
        }
        return fmt

    # Return HTML for the current Graphite image, with link to a larger size.
    def get_dashboard_html(self, width, height, html_legend):
        fmt = self.get_dashboard(width, height, html_legend)
        blob = '''<span class="graphiteGraph" style="width:{width}px">
        <a href="{img_url}"><img src="{img_src}" width="{width}" height="{height}"></a>
        {legend}
        </span>'''.format(**fmt)

        return blob
