from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

import django.contrib.auth.views as djauth

# For adding explicit grouping resource endpoints in API documentation.
from rest_framework_swagger.urlparser import UrlParser

from catmaid.control import (authentication, user, log, message, client, common,
        project, stack, stackgroup, tile, tracing, stats, neuron_annotations as
        annotations, textlabel, label, link, connector, neuron, node, treenode,
        suppressed_virtual_treenode, skeleton, skeletonexport, treenodeexport,
        cropping, data_view, ontology, classification, notifications, roi,
        clustering, volume, flytem, dvid, useranalytics, user_evaluation,
        search, graphexport, graph2, circles, analytics, review,
        wiringdiagram, object, treenodetable)

from catmaid.views import CatmaidView


# A regular expression matching floating point and integer numbers
num = r'[-+]?[0-9]*\.?[0-9]+'
integer = r'[-+]?[0-9]+'
# A regular expression matching lists of integers with comma as delimiter
intlist = r'[0-9]+(,[0-9]+)*'
# A list of words, not containing commas
wordlist= r'\w+(,\w+)*'

app_name = 'catmaid'

# Add the main index.html page at the root:
urlpatterns = [
    url(r'^$', ensure_csrf_cookie(CatmaidView.as_view(template_name='catmaid/index.html')), name="home"),
    url(r'^version$', common.get_catmaid_version)
]

# Authentication and permissions
urlpatterns += [
    url(r'^accounts/login$', authentication.login_user),
    url(r'^accounts/logout$', authentication.logout_user),
    url(r'^accounts/(?P<project_id>\d+)/all-usernames$', authentication.all_usernames),
    url(r'^permissions$', authentication.user_project_permissions),
    url(r'^classinstance/(?P<ci_id>\d+)/permissions$', authentication.get_object_permissions),
    url(r'^register$', authentication.register),
]

# Users
urlpatterns += [
    url(r'^user-list$', user.user_list),
    url(r'^user-table-list$', user.user_list_datatable),
    url(r'^user-profile/update$', user.update_user_profile),
    url(r'^user/password_change/$', user.change_password, {'post_change_redirect': '/'}),
]

# Log
urlpatterns += [
    url(r'^(?P<project_id>\d+)/logs/list$', log.list_logs),
    url(r'^log/(?P<level>(info|error|debug))$', log.log_frontent_event),
]

# Messages
urlpatterns += [
    url(r'^messages/list$', message.list_messages),
    url(r'^messages/mark_read$', message.read_message),
    url(r'^messages/latestunreaddate', message.get_latest_unread_date),
]

# CATMAID client datastore and data access
urlpatterns += [
    url(r'^client/datastores/$', client.ClientDatastoreList.as_view()),
    url(r'^client/datastores/(?P<name>[\w-]+)$', client.ClientDatastoreDetail.as_view()),
    url(r'^client/datastores/(?P<name>[\w-]+)/$', client.ClientDataList.as_view()),
]

# General project model access
urlpatterns += [
    url(r'^projects/$', project.projects),
    url(r'^projects/export$', project.export_projects),
]

# General stack model access
urlpatterns += [
    url(r'^(?P<project_id>\d+)/stacks$', stack.stacks),
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/info$', stack.stack_info),
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/models$', stack.stack_models),
]

# General stack group access
urlpatterns += [
    url(r'^(?P<project_id>\d+)/stackgroup/(?P<stackgroup_id>\d+)/info$', stackgroup.get_stackgroup_info),
]

# Tile access
urlpatterns += [
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/tile$', tile.get_tile),
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/put_tile$', tile.put_tile),
]

# Tracing general
urlpatterns += [
    url(r'^(?P<project_id>\d+)/tracing/setup/rebuild$', tracing.rebuild_tracing_setup_view),
    url(r'^(?P<project_id>\d+)/tracing/setup/test$', tracing.check_tracing_setup_view),
]

# Statistics
urlpatterns += [
    url(r'^(?P<project_id>\d+)/stats$', TemplateView.as_view(template_name="catmaid/projectstatistics.html")),
    url(r'^(?P<project_id>\d+)/stats/nodecount$', stats.stats_nodecount),
    url(r'^(?P<project_id>\d+)/stats/editor$', stats.stats_editor),
    url(r'^(?P<project_id>\d+)/stats/summary$', stats.stats_summary),
    url(r'^(?P<project_id>\d+)/stats/history$', stats.stats_history),
    url(r'^(?P<project_id>\d+)/stats/user-history$', stats.stats_user_history),
    url(r'^(?P<project_id>\d+)/stats/user-activity$', stats.stats_user_activity),
]

# Annotations
urlpatterns += [
    url(r'^(?P<project_id>\d+)/annotations/$', annotations.list_annotations),
    url(r'^(?P<project_id>\d+)/annotations/query$', annotations.annotations_for_entities),
    url(r'^(?P<project_id>\d+)/annotations/forskeletons$', annotations.annotations_for_skeletons),
    url(r'^(?P<project_id>\d+)/annotations/table-list$', annotations.list_annotations_datatable),
    url(r'^(?P<project_id>\d+)/annotations/add$', annotations.annotate_entities),
    url(r'^(?P<project_id>\d+)/annotations/remove$', annotations.remove_annotations),
    url(r'^(?P<project_id>\d+)/annotations/(?P<annotation_id>\d+)/remove$', annotations.remove_annotation),
    url(r'^(?P<project_id>\d+)/annotations/query-targets$', annotations.query_annotated_classinstances),
]

# Text labels
urlpatterns += [
    url(r'^(?P<project_id>\d+)/textlabel/create$', textlabel.create_textlabel),
    url(r'^(?P<project_id>\d+)/textlabel/delete$', textlabel.delete_textlabel),
    url(r'^(?P<project_id>\d+)/textlabel/update$', textlabel.update_textlabel),
    url(r'^(?P<project_id>\d+)/textlabel/all', textlabel.textlabels),
]

# Treenode labels
urlpatterns += [
    url(r'^(?P<project_id>\d+)/labels/$', label.labels_all),
    url(r'^(?P<project_id>\d+)/labels-for-nodes$', label.labels_for_nodes),
    url(r'^(?P<project_id>\d+)/labels/(?P<node_type>(treenode|location|connector))/(?P<node_id>\d+)/$', label.labels_for_node),
    url(r'^(?P<project_id>\d+)/label/(?P<ntype>(treenode|location|connector))/(?P<location_id>\d+)/update$', label.label_update),
    url(r'^(?P<project_id>\d+)/label/(?P<ntype>(treenode|location|connector))/(?P<location_id>\d+)/remove$', label.remove_label_link),
    url(r'^(?P<project_id>\d+)/label/remove$', label.label_remove),
]

# Links
urlpatterns += [
    url(r'^(?P<project_id>\d+)/link/create$', link.create_link),
    url(r'^(?P<project_id>\d+)/link/delete$', link.delete_link),
]

# Connector access
urlpatterns += [
    url(r'^(?P<project_id>\d+)/connector/create$', connector.create_connector),
    url(r'^(?P<project_id>\d+)/connector/delete$', connector.delete_connector),
    url(r'^(?P<project_id>\d+)/connector/table/list$', connector.list_connector),
    url(r'^(?P<project_id>\d+)/connector/list/graphedge$', connector.graphedge_list),
    url(r'^(?P<project_id>\d+)/connector/list/one_to_many$', connector.one_to_many_synapses),
    url(r'^(?P<project_id>\d+)/connector/list/many_to_many$', connector.many_to_many_synapses),
    url(r'^(?P<project_id>\d+)/connector/list/completed$', connector.list_completed),
    url(r'^(?P<project_id>\d+)/connector/skeletons$', connector.connector_skeletons),
    url(r'^(?P<project_id>\d+)/connector/edgetimes$', connector.connector_associated_edgetimes),
    url(r'^(?P<project_id>\d+)/connector/info$', connector.connectors_info),
    url(r'^(?P<project_id>\d+)/connector/user-info$', connector.connector_user_info),
    url(r'^(?P<project_id>\d+)/connectors/(?P<connector_id>\d+)/$',
        connector.connector_detail),
]

# Neuron access
UrlParser.explicit_root_paths |= set(['{project_id}/neurons'])
urlpatterns += [
    url(r'^(?P<project_id>\d+)/neuron/(?P<neuron_id>\d+)/get-all-skeletons$', neuron.get_all_skeletons_of_neuron),
    url(r'^(?P<project_id>\d+)/neuron/(?P<neuron_id>\d+)/give-to-user$', neuron.give_neuron_to_other_user),
    url(r'^(?P<project_id>\d+)/neuron/(?P<neuron_id>\d+)/delete$', neuron.delete_neuron),
    url(r'^(?P<project_id>\d+)/neurons/(?P<neuron_id>\d+)/rename$', neuron.rename_neuron),
    url(r'^(?P<project_id>\d+)/neurons/from-models$', neuron.get_neuron_ids_from_models),
]

# Node access
UrlParser.explicit_root_paths |= set(['{project_id}/nodes'])
urlpatterns += [
    url(r'^(?P<project_id>\d+)/node/(?P<node_id>\d+)/reviewed$', node.update_location_reviewer),
    url(r'^(?P<project_id>\d+)/node/most_recent$', node.most_recent_treenode),
    url(r'^(?P<project_id>\d+)/node/nearest$', node.node_nearest),
    url(r'^(?P<project_id>\d+)/node/update$', node.node_update),
    url(r'^(?P<project_id>\d+)/node/list$', node.node_list_tuples),
    url(r'^(?P<project_id>\d+)/node/get_location$', node.get_location),
    url(r'^(?P<project_id>\d+)/node/user-info$', node.user_info),
    url(r'^(?P<project_id>\d+)/nodes/find-labels$', node.find_labels),
]

# Treenode access
UrlParser.explicit_root_paths |= set(['{project_id}/treenodes'])
urlpatterns += [
    url(r'^(?P<project_id>\d+)/treenode/create$', treenode.create_treenode),
    url(r'^(?P<project_id>\d+)/treenode/insert$', treenode.insert_treenode),
    url(r'^(?P<project_id>\d+)/treenode/delete$', treenode.delete_treenode),
    url(r'^(?P<project_id>\d+)/treenodes/(?P<treenode_id>\d+)/info$', treenode.treenode_info),
    url(r'^(?P<project_id>\d+)/treenodes/(?P<treenode_id>\d+)/children$', treenode.find_children),
    url(r'^(?P<project_id>\d+)/treenodes/(?P<treenode_id>\d+)/confidence$', treenode.update_confidence),
    url(r'^(?P<project_id>\d+)/treenode/(?P<treenode_id>\d+)/parent$', treenode.update_parent),
    url(r'^(?P<project_id>\d+)/treenode/(?P<treenode_id>\d+)/radius$', treenode.update_radius),
    url(r'^(?P<project_id>\d+)/treenodes/radius$', treenode.update_radii),
    url(r'^(?P<project_id>\d+)/treenodes/(?P<treenode_id>\d+)/previous-branch-or-root$', treenode.find_previous_branchnode_or_root),
    url(r'^(?P<project_id>\d+)/treenodes/(?P<treenode_id>\d+)/next-branch-or-end$', treenode.find_next_branchnode_or_end),
]

# Suppressed virtual treenode access
urlpatterns += [
    url(r'^(?P<project_id>\d+)/treenodes/(?P<treenode_id>\d+)/suppressed-virtual/$',
            suppressed_virtual_treenode.SuppressedVirtualTreenodeList.as_view()),
    url(r'^(?P<project_id>\d+)/treenodes/(?P<treenode_id>\d+)/suppressed-virtual/(?P<suppressed_id>\d+)$',
            suppressed_virtual_treenode.SuppressedVirtualTreenodeDetail.as_view()),
]

# General skeleton access
urlpatterns += [
    url(r'^(?P<project_id>\d+)/skeletons/$', skeleton.list_skeletons),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/node_count$', skeleton.node_count),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/neuronname$', skeleton.neuronname),
    url(r'^(?P<project_id>\d+)/skeleton/neuronnames$', skeleton.neuronnames),
    url(r'^(?P<project_id>\d+)/skeleton/node/(?P<treenode_id>\d+)/node_count$', skeleton.node_count),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/review/reset-own$', skeleton.reset_own_reviewer_ids),
    url(r'^(?P<project_id>\d+)/skeletons/connectivity$', skeleton.skeleton_info_raw),
    url(r'^(?P<project_id>\d+)/skeleton/connectivity_matrix$', skeleton.connectivity_matrix),
    url(r'^(?P<project_id>\d+)/skeletons/review-status$', skeleton.review_status),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/statistics$', skeleton.skeleton_statistics),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/contributor_statistics$', skeleton.contributor_statistics),
    url(r'^(?P<project_id>\d+)/skeleton/contributor_statistics_multiple$', skeleton.contributor_statistics_multiple),
    url(r'^(?P<project_id>\d+)/skeletons/(?P<skeleton_id>\d+)/find-labels$', skeleton.find_labels),
    url(r'^(?P<project_id>\d+)/skeletons/(?P<skeleton_id>\d+)/open-leaves$', skeleton.open_leaves),
    url(r'^(?P<project_id>\d+)/skeletons/(?P<skeleton_id>\d+)/root$', skeleton.root_for_skeleton),
    url(r'^(?P<project_id>\d+)/skeleton/split$', skeleton.split_skeleton),
    url(r'^(?P<project_id>\d+)/skeleton/ancestry$', skeleton.skeleton_ancestry),
    url(r'^(?P<project_id>\d+)/skeleton/join$', skeleton.join_skeleton),
    url(r'^(?P<project_id>\d+)/skeleton/reroot$', skeleton.reroot_skeleton),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/permissions$', skeleton.get_skeleton_permissions),
    url(r'^(?P<project_id>\d+)/skeleton/annotationlist$', skeleton.annotation_list),
    url(r'^(?P<project_id>\d+)/skeletons/within-spatial-distance$', skeleton.within_spatial_distance),
    url(r'^(?P<project_id>\d+)/skeletongroup/adjacency_matrix$', skeleton.adjacency_matrix),
    url(r'^(?P<project_id>\d+)/skeletongroup/skeletonlist_subgraph', skeleton.skeletonlist_subgraph),
    url(r'^(?P<project_id>\d+)/skeletongroup/all_shared_connectors', skeleton.all_shared_connectors),
]

# Skeleton export
urlpatterns += [
    url(r'^(?P<project_id>\d+)/neuroml/neuroml_level3_v181$', skeletonexport.export_neuroml_level3_v181),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/swc$', skeletonexport.skeleton_swc),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/neuroml$', skeletonexport.skeletons_neuroml),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/json$', skeletonexport.skeleton_with_metadata),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/compact-json$', skeletonexport.skeleton_for_3d_viewer),
    url(r'^(?P<project_id>\d+)/(?P<skeleton_id>\d+)/(?P<with_connectors>\d)/(?P<with_tags>\d)/compact-skeleton$', skeletonexport.compact_skeleton),
    url(r'^(?P<project_id>\d+)/(?P<skeleton_id>\d+)/(?P<with_nodes>\d)/(?P<with_connectors>\d)/(?P<with_tags>\d)/compact-arbor$', skeletonexport.compact_arbor),
    url(r'^(?P<project_id>\d+)/(?P<skeleton_id>\d+)/(?P<with_nodes>\d)/(?P<with_connectors>\d)/(?P<with_tags>\d)/compact-arbor-with-minutes$', skeletonexport.compact_arbor_with_minutes),
    url(r'^(?P<project_id>\d+)/skeletons/(?P<skeleton_id>\d+)/review$', skeletonexport.export_review_skeleton),
    url(r'^(?P<project_id>\d+)/skeleton/(?P<skeleton_id>\d+)/reviewed-nodes$', skeletonexport.export_skeleton_reviews),
    url(r'^(?P<project_id>\d+)/skeletons/measure$', skeletonexport.measure_skeletons),
    url(r'^(?P<project_id>\d+)/skeleton/connectors-by-partner$', skeletonexport.skeleton_connectors_by_partner),
    url(r'^(?P<project_id>\d+)/skeletons/partners-by-connector$', skeletonexport.partners_by_connector),
]

# Treenode and Connector image stack archive export
urlpatterns += [
    url(r'^(?P<project_id>\d+)/connectorarchive/export$', treenodeexport.export_connectors),
    url(r'^(?P<project_id>\d+)/treenodearchive/export$', treenodeexport.export_treenodes),
]

# Cropping
urlpatterns += [
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_ids>%s)/crop/(?P<x_min>%s),(?P<x_max>%s)/(?P<y_min>%s),(?P<y_max>%s)/(?P<z_min>%s),(?P<z_max>%s)/(?P<zoom_level>\d+)/(?P<single_channel>[0|1])/$' % (intlist, num, num, num, num, num, num), cropping.crop),
    url(r'^crop/download/(?P<file_path>.*)/$', cropping.download_crop)
]

# Tagging
urlpatterns += [
    url(r'^(?P<project_id>\d+)/tags/list$', project.list_project_tags),
    url(r'^(?P<project_id>\d+)/tags/clear$', project.update_project_tags),
    url(r'^(?P<project_id>\d+)/tags/(?P<tags>.*)/update$', project.update_project_tags),
]
urlpatterns += [
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/tags/list$', stack.list_stack_tags),
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/tags/clear$', stack.update_stack_tags),
    url(r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/tags/(?P<tags>.*)/update$', stack.update_stack_tags),
]

# Data views
urlpatterns += [
    url(r'^dataviews/list$', data_view.get_available_data_views),
    url(r'^dataviews/default$', data_view.get_default_properties),
    url(r'^dataviews/show/(?P<data_view_id>\d+)$', data_view.get_data_view),
    url(r'^dataviews/show/default$', data_view.get_default_data_view),
    url(r'^dataviews/type/comment$', data_view.get_data_view_type_comment),
    url(r'^dataviews/type/(?P<data_view_id>\d+)$', data_view.get_data_view_type),
]

# Ontologies
urlpatterns += [
    url(r'^ontology/knownroots$', ontology.get_known_ontology_roots),
    url(r'^(?P<project_id>%s)/ontology/list$' % (integer), ontology.list_ontology),
    url(r'^(?P<project_id>%s)/ontology/relations$' % (integer), ontology.get_available_relations),
    url(r'^(?P<project_id>%s)/ontology/relations/add$' % (integer), ontology.add_relation_to_ontology),
    url(r'^(?P<project_id>%s)/ontology/relations/rename$' % (integer), ontology.rename_relation),
    url(r'^(?P<project_id>%s)/ontology/relations/remove$' % (integer), ontology.remove_relation_from_ontology),
    url(r'^(?P<project_id>%s)/ontology/relations/removeall$' % (integer), ontology.remove_all_relations_from_ontology),
    url(r'^(?P<project_id>%s)/ontology/relations/list$' % (integer), ontology.list_available_relations),
    url(r'^(?P<project_id>%s)/ontology/classes$' % (integer), ontology.get_available_classes),
    url(r'^(?P<project_id>%s)/ontology/classes/add$' % (integer), ontology.add_class_to_ontology),
    url(r'^(?P<project_id>%s)/ontology/classes/rename$' % (integer), ontology.rename_class),
    url(r'^(?P<project_id>%s)/ontology/classes/remove$' % (integer), ontology.remove_class_from_ontology),
    url(r'^(?P<project_id>%s)/ontology/classes/removeall$' % (integer), ontology.remove_all_classes_from_ontology),
    url(r'^(?P<project_id>%s)/ontology/classes/list$' % (integer), ontology.list_available_classes),
    url(r'^(?P<project_id>%s)/ontology/links/add$' % (integer), ontology.add_link_to_ontology),
    url(r'^(?P<project_id>%s)/ontology/links/remove$' % (integer), ontology.remove_link_from_ontology),
    url(r'^(?P<project_id>%s)/ontology/links/removeselected$' % (integer), ontology.remove_selected_links_from_ontology),
    url(r'^(?P<project_id>%s)/ontology/links/removeall$' % (integer), ontology.remove_all_links_from_ontology),
    url(r'^(?P<project_id>%s)/ontology/restrictions/add$' % (integer), ontology.add_restriction),
    url(r'^(?P<project_id>%s)/ontology/restrictions/remove$' % (integer), ontology.remove_restriction),
    url(r'^(?P<project_id>%s)/ontology/restrictions/(?P<restriction>[^/]*)/types$' % (integer), ontology.get_restriction_types),
]

# Classification
urlpatterns += [
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/number$'.format(integer),
        classification.get_classification_number),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/show$'.format(integer),
        classification.show_classification_editor),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/show/(?P<link_id>\d+)$'.format(integer),
        classification.show_classification_editor),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/select$'.format(integer),
        classification.select_classification_graph, name='select_classification_graph'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/setup/test$'.format(integer),
        classification.check_classification_setup_view, name='test_classification_setup'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/setup/rebuild$'.format(integer),
        classification.rebuild_classification_setup_view, name='rebuild_classification_setup'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/new$'.format(integer),
        classification.add_classification_graph, name='add_classification_graph'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/list$'.format(integer),
        classification.list_classification_graph, name='list_classification_graph'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/list/(?P<link_id>\d+)$'.format(integer),
        classification.list_classification_graph, name='list_classification_graph'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/(?P<link_id>\d+)/remove$'.format(integer),
        classification.remove_classification_graph, name='remove_classification_graph'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/instance-operation$'.format(integer),
        classification.classification_instance_operation, name='classification_instance_operation'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/(?P<link_id>\d+)/autofill$'.format(integer),
        classification.autofill_classification_graph, name='autofill_classification_graph'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/link$'.format(integer),
        classification.link_classification_graph, name='link_classification_graph'),
    url(r'^(?P<project_id>{0})/classification/(?P<workspace_pid>{0})/stack/(?P<stack_id>{0})/linkroi/(?P<ci_id>{0})/$'.format(integer),
        classification.link_roi_to_classification, name='link_roi_to_classification'),
    url(r'^classification/(?P<workspace_pid>{0})/export$'.format(integer),
        classification.export, name='export_classification'),
    url(r'^classification/(?P<workspace_pid>{0})/export/excludetags/(?P<exclusion_tags>{1})/$'.format(integer, wordlist),
        classification.export, name='export_classification'),
    url(r'^classification/(?P<workspace_pid>{0})/search$'.format(integer),
        classification.search, name='search_classifications'),
    url(r'^classification/(?P<workspace_pid>{0})/export_ontology$'.format(integer),
        classification.export_ontology, name='export_ontology'),
]

# Notifications
urlpatterns += [
    url(r'^(?P<project_id>\d+)/notifications/list$', notifications.list_notifications),
    url(r'^(?P<project_id>\d+)/changerequest/approve$', notifications.approve_change_request),
    url(r'^(?P<project_id>\d+)/changerequest/reject$', notifications.reject_change_request),
]

# Regions of interest
urlpatterns += [
    url(r'^(?P<project_id>{0})/roi/(?P<roi_id>{0})/info$'.format(integer), roi.get_roi_info, name='get_roi_info'),
    url(r'^(?P<project_id>{0})/roi/link/(?P<relation_id>{0})/stack/(?P<stack_id>{0})/ci/(?P<ci_id>{0})/$'.format(integer),
        roi.link_roi_to_class_instance, name='link_roi_to_class_instance'),
    url(r'^(?P<project_id>{0})/roi/(?P<roi_id>{0})/remove$'.format(integer), roi.remove_roi_link, name='remove_roi_link'),
    url(r'^(?P<project_id>{0})/roi/(?P<roi_id>{0})/image$'.format(integer), roi.get_roi_image, name='get_roi_image'),
    url(r'^(?P<project_id>{0})/roi/add$'.format(integer), roi.add_roi, name='add_roi'),
]

# Clustering
urlpatterns += [
    url(r'^clustering/(?P<workspace_pid>{0})/setup$'.format(integer),
        clustering.setup_clustering, name="clustering_setup"),
    url(r'^clustering/(?P<workspace_pid>{0})/show$'.format(integer),
        TemplateView.as_view(template_name="catmaid/clustering/display.html"),
        name="clustering_display"),
]

# Volumes
urlpatterns += [
   url(r'^(?P<project_id>\d+)/volumes/$', volume.volume_collection),
   url(r'^(?P<project_id>\d+)/volumes/add$', volume.add_volume),
   url(r'^(?P<project_id>\d+)/volumes/(?P<volume_id>\d+)/$', volume.volume_detail),
   url(r'^(?P<project_id>\d+)/volumes/(?P<volume_id>\d+)/intersect$', volume.intersects),
]

# Front-end tests
urlpatterns += [
    url(r'^tests$', login_required(CatmaidView.as_view(template_name="catmaid/tests.html")), name="frontend_tests"),
]

# Collection of various parts of the CATMAID API. These methods are usually
# one- or two-liners and having them in a separate statement would not improve
# readability. Therefore, they are all declared in this general statement.
urlpatterns += [
    # User analytics and proficiency
    url(r'^useranalytics$', useranalytics.plot_useranalytics),
    url(r'^(?P<project_id>\d+)/userproficiency$', user_evaluation.evaluate_user),

    url(r'^(?P<project_id>\d+)/graphexport/json$', graphexport.export_jsongraph),

    # Graphs
    url(r'^(?P<project_id>\d+)/skeletons/confidence-compartment-subgraph', graph2.skeleton_graph),

    # Circles
    url(r'^(?P<project_id>\d+)/graph/circlesofhell', circles.circles_of_hell),
    url(r'^(?P<project_id>\d+)/graph/directedpaths', circles.find_directed_paths),

    # Analytics
    url(r'^(?P<project_id>\d+)/skeleton/analytics$', analytics.analyze_skeletons),

    # Review
    url(r'^(?P<project_id>\d+)/user/reviewer-whitelist$', review.reviewer_whitelist),

    # Search
    url(r'^(?P<project_id>\d+)/search$', search.search),

    # Wiring diagram export
    url(r'^(?P<project_id>\d+)/wiringdiagram/json$', wiringdiagram.export_wiring_diagram),
    url(r'^(?P<project_id>\d+)/wiringdiagram/nx_json$', wiringdiagram.export_wiring_diagram_nx),

    # Annotation graph export
    url(r'^(?P<project_id>\d+)/annotationdiagram/nx_json$', object.convert_annotations_to_networkx),

    # Treenode table
    url(r'^(?P<project_id>\d+)/treenode/table/(?P<skid>\d+)/content$', treenodetable.treenode_table_content),
]

# Patterns for FlyTEM access
from catmaid.control.flytem import (project as flytemproject,
        review as flytemreview, stack as flytemstack)
urlpatterns += [
    url(r'^flytem/projects/$', flytemproject.projects),
    url(r'^(?P<project_id>.+)/user/reviewer-whitelist$', flytemreview.reviewer_whitelist),
    url(r'^flytem/(?P<project_id>.+)/stack/(?P<stack_id>.+)/info$', flytem.stack.stack_info),
    url(r'^flytem/(?P<project_id>.+)/stacks$', flytemstack.stacks),
]

# Patterns for DVID access
from catmaid.control.dvid import (project as dvidproject,
        review as dvidreview, stack as dvidstack)
urlpatterns += [
    url(r'^dvid/projects/$', dvidproject.projects),
    url(r'^(?P<project_id>.+)/user/reviewer-whitelist$', dvidreview.reviewer_whitelist),
    url(r'^dvid/(?P<project_id>.+)/stack/(?P<stack_id>.+)/info$', dvidstack.stack_info),
    url(r'^dvid/(?P<project_id>.+)/stacks$', dvidstack.stacks),
]
