import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import connection

from catmaid.control.authentication import *
from catmaid.control.common import *

import operator
from collections import defaultdict

@requires_user_role([UserRole.Annotate, UserRole.Browse])
def get_all_annotations_of_neuron(request, project_id=None, neuron_id=None):
    p = get_object_or_404(Project, pk=project_id)
    neuron = get_object_or_404(ClassInstance,
        pk=neuron_id,
        class_column__class_name='neuron',
        project=p)
    qs = ClassInstance.objects.filter(
        project=p,
        cici_via_a__relation__relation_name='annotated_with',
        cici_via_a__class_instance_b=neuron)
    return HttpResponse(json.dumps([x.id for x in qs]), mimetype="text/json")