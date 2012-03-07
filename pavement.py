from paver.easy import *
import pkg_resources
from itertools import chain


@task
def kpyc():
    sh('find . -iname "*.pyc" -delete')


@task
@needs(['kpyc'])
def clean():
    print "rming the build dir and *.egg-info"
    delete = (
        (path(__file__).dirname().joinpath("build"), ),
        path(__file__).dirname().glob("*.egg-info"),
        )

    for d in chain(*delete):
        path(d).rmtree()


@task
@needs(['clean'])
@cmdopts([
    ('module=', 'm', 'module to get the version from')
])
def publish(options):
    """Publish <module> to the disqus pip cheeze thingy"""
    if not hasattr(options, 'module'):
        print "module is not an option, it is required"

    sh("python setup.py build")
    sh("python setup.py install")

    VERSION = sh("python -c 'import pkg_resources; print pkg_resources.get_distribution(\"%s\").version'" % options.module, capture=True)
    print VERSION

    print "creating tag " + VERSION
    sh("git tag " + VERSION, ignore_error=True)

    print "pushing tag"
    sh("git push origin " + VERSION)

    manifest = path('MANIFEST')
    if manifest.exists():
        print "removing manifest file"
        manifest.remove()

    print "uploading package."
    sh("python setup.py sdist upload -r disqus")

    clean()
