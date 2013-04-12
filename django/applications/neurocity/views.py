from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from django.shortcuts import render_to_response
from django.template import RequestContext

from neurocity.control.segment import get_random_segment

def language_view(request):
    return render_to_response('neurocity/setlanguage.html', {},
                          context_instance=RequestContext(request))

class SegmentDecisionView(TemplateView):
    """ This view returns a page to decide on the correctness of a segment.
    """
    template_name = "neurocity/segmentdecision.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        # TODO: segmentid
        context['origin_section'] = 0
        context['origin_sliceid'] = 123
        context['target_section'] = 0
        return context

class NeurocityHomeView(TemplateView):

    template_name = "neurocity/home.html"

    def get_context_data(self, **kwargs):
        context = super(NeurocityHomeView, self).get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context

class LearnView(TemplateView):

    template_name = "neurocity/learn.html"

    def get_context_data(self, **kwargs):
        context = super(LearnView, self).get_context_data(**kwargs)
        return context

class DashboardView(TemplateView):

    template_name = "neurocity/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context

class ContributeView(TemplateView):

    template_name = "neurocity/contribute.html"

    def get_context_data(self, **kwargs):
        context = super(ContributeView, self).get_context_data(**kwargs)
        segment = get_random_segment()

        context['originsection'] = segment.origin_section
        context['targetsection'] = segment.target_section
        context['segmentid'] = segment.segmentid
        context['cost'] = segment.cost
        
        return context
