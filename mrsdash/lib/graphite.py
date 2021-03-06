from urllib import urlencode
from mrsdash.lib.time_helpers import parse_time
from mrsdash.lib.helpers import accepts
from copy import deepcopy


class Graphite(object):
    """a way to interact with a graphite server"""
    def __init__(self, name, host, port):
        super(Graphite, self).__init__()
        self.host = host
        self.port = port

    # use stats here for the rest
    def graphite_mark(action="deploy"):
        # send_graphite('%s.%s.%s 1 %d' % (action, env.name, env.host.split('.')[0], int(time.time()),))
        pass


class Series(str):
    def __new__(cls, series, *funcs, **kwargs):
        return super(Series, cls).__new__(cls, series)

    def __init__(self, series, *funcs):
        super(Series, self).__init__()
        self._functions = []
        self._applied = series
        for f in funcs:
            if isinstance(f, basestring):
                f = (f,)
            self._add_raw_function(*f)
        self._applied = self.apply_functions()

    def __str__(self):
        return self._applied

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

    ## functions! doing these explicitly instead of dynamically
    def alias(self, alias):
        self.add_raw_function("alias", alias)
        return self

    def second_y_axis(self):
        self.add_raw_function("secondYAxis")
        return self

    def draw_as_infinite(self):
        self.add_raw_function("drawAsInfinite")
        return self

    @accepts(str, self=True)
    def color(self, color):
        self.add_raw_function("color", color)
        return self

    @accepts(int, self=True)
    def line_width(self, width):
        self.add_raw_function("lineWidth", width)
        return self

    # TODO: add the rest of the functions from http://graphite.readthedocs.org/en/1.0/functions.html


class Deploy(Series):
    """A special case for deployments"""
    def __init__(self, series, *funcs, **kwargs):
        super(Deploy, self).__init__(series, *funcs)

        name = kwargs.get('name', 'Deploy')
        color = kwargs.get('color', 'blue')
        line_width = kwargs.get('line_width', 2)

        self.draw_as_infinite()
        self.line_width(line_width)
        self.color(color)
        self.alias(name)


class Graph(object):
    @classmethod
    def set_config(cls, config):
        """
        Set the config for the whole class. This will remove it as a requirement
        for the init function
        """
        assert("GRAPHITE_BASE_URL" in config)

        cls._config = {
            "GRAPHITE_BASE_URL": config.get("GRAPHITE_BASE_URL"),
            "GRAPHITE_DEPLOYS": config.get('GRAPHITE_DEPLOYS', [])
        }

    def __new__(cls, *args):
        """Copy constructor"""
        if len(args) == 1 and isinstance(args[0], cls):
            return deepcopy(args[0])
        else:
            return super(Graph, cls).__new__(cls, *args)

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], self.__class__):
            pass
        elif len(args) == 1 and isinstance(args[0], basestring):
            if not hasattr(self.__class__, "_config"):
                raise AttributeError("You must use Graph.set_config() to use this constructor")
            self.__init__(self.__class__._config, args[0])
        elif len(args) == 2:
            config, time = args
            self._area_mode = None
            self._base_url = config['GRAPHITE_BASE_URL']
            self._deploys = config.get('GRAPHITE_DEPLOYS', [])
            self._display_title = True
            self._display_vtitle = False
            self._hide_grid = False
            self._hide_legend = False
            self._line_mode = None
            self._line_width = None
            self._pie_chart = False
            self._series = []
            self._show_deploys = True
            self._show_deploys_in_legend = True
            self._span = 12
            self._stacked = False
            self._template = None
            self._threshold = []
            self._time = time
            self._time_shift = None
            self._title = None
            self._vtitle = None
            self._y_max = None
            self._y_min = None
        else:
            raise TypeError("__init__() takes either 1 or 2 arguments %d given" % len(args))

    # TODO: add a horizontal line method
    @accepts(int, self=True)
    def add_threshold(self, threshold, label=None, color=None):
        args = ('threshold', filter(lambda x: True if x else False, (label, color)))
        self.add_series(threshold, *args)
        return self

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
    def template(self, template):
        self._template = template
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

    @accepts(str, self=True)
    def area_mode(self, mode):
        self._area_mode = mode
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

    def add_hw_bands(self, series, period='w', *args):
        self.show_deploys(False)
        self.add_series(Series(series, ('timeShift', '-2%s' % period), *args).alias("Last %s" % period).line_width(0.5))
        self.add_series(Series(series, *args).alias("This %s" % period).line_width(0.5))
        self.add_series(Series(series, ('holtWintersConfidenceBands'), *args).line_width(0.5))

        # holtWintersForecast
        self._time = '-2%s' % period
        return self

    # Include vertical deploy lines over any metrics included in the image.
    @accepts(bool, self=True)
    def show_deploys(self, show=True):
        self._show_deploys = show
        return self

    @accepts(bool, self=True)
    def show_deploys_in_legend(self, show=True):
        self._show_deploys_in_legend = show
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

        if self._area_mode:
            p['areaMode'] = self._area_mode

        if self._template:
            p['template'] = self._template

        if self._show_deploys:
            for deploy in self._deploys:
                d = Series(deploy)
                if not self._show_deploys_in_legend:
                    d.alias('')
                self.add_series(d)

        targets = []
        colors = []

        for m in self._series:
            targets.append('target=' + m['target'])  # shouldn't need to quote this
            if 'color' in m and m['color']:
                colors.append(m['color'])

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
