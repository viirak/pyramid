import unittest

from zope.component.testing import PlacelessSetup

class Base(PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _zcmlConfigure(self):
        import repoze.bfg
        import zope.configuration.xmlconfig
        zope.configuration.xmlconfig.file('configure.zcml', package=repoze.bfg)

    def _getTemplatePath(self, name):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(here, 'fixtures', name)
        
class RenderTemplateTests(unittest.TestCase, Base):
    def setUp(self):
        Base.setUp(self)

    def tearDown(self):
        Base.tearDown(self)

    def _getFUT(self):
        from repoze.bfg.template import render_template
        return render_template

    def test_it(self):
        self._zcmlConfigure()
        minimal = self._getTemplatePath('minimal.pt')
        render = self._getFUT()
        result = render(minimal)
        self.failUnless(isinstance(result, str))
        self.assertEqual(result, '<div>\n</div>\n')

class RenderTemplateToResponseTests(unittest.TestCase, Base):
    def setUp(self):
        Base.setUp(self)

    def tearDown(self):
        Base.tearDown(self)

    def _getFUT(self):
        from repoze.bfg.template import render_template_to_response
        return render_template_to_response

    def test_it(self):
        self._zcmlConfigure()
        minimal = self._getTemplatePath('minimal.pt')
        render = self._getFUT()
        result = render(minimal)
        from webob import Response
        self.failUnless(isinstance(result, Response))
        self.assertEqual(result.app_iter, ['<div>\n</div>\n'])
        self.assertEqual(result.status, '200 OK')
        self.assertEqual(len(result.headerlist), 2)

class GetTemplateTests(unittest.TestCase, Base):
    def setUp(self):
        Base.setUp(self)

    def tearDown(self):
        Base.tearDown(self)

    def _getFUT(self):
        from repoze.bfg.template import get_template
        return get_template

    def test_nonabs_registered(self):
        self._zcmlConfigure()
        from zope.component import getGlobalSiteManager
        from zope.component import queryUtility
        from repoze.bfg.chameleon_zpt import ZPTTemplateFactory
        from repoze.bfg.interfaces import ITemplate
        minimal = self._getTemplatePath('minimal.pt')
        utility = ZPTTemplateFactory(minimal)
        gsm = getGlobalSiteManager()
        gsm.registerUtility(utility, ITemplate, name=minimal)
        get = self._getFUT()
        result = get(minimal)
        self.assertEqual(result.filename, minimal)
        self.assertEqual(queryUtility(ITemplate, minimal), utility)
        
    def test_nonabs_unregistered(self):
        self._zcmlConfigure()
        from zope.component import getGlobalSiteManager
        from zope.component import queryUtility
        from repoze.bfg.chameleon_zpt import ZPTTemplateFactory
        from repoze.bfg.interfaces import ITemplate
        minimal = self._getTemplatePath('minimal.pt')
        self.assertEqual(queryUtility(ITemplate, minimal), None)
        utility = ZPTTemplateFactory(minimal)
        gsm = getGlobalSiteManager()
        gsm.registerUtility(utility, ITemplate, name=minimal)
        get = self._getFUT()
        result = get(minimal)
        self.assertEqual(result.filename, minimal)
        self.assertEqual(queryUtility(ITemplate, minimal), utility)

