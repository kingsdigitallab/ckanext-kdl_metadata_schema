import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def kdl_project_status():
    create_kdl_project_status()
    try:
        tag_list = toolkit.get_action('tag_list')
        return tag_list(data_dict={'vocabulary_id': 'kdl_project_status'})
    except toolkit.ObjectNotFound:
        return None


def create_kdl_project_status():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}

    try:
        data = {'id': 'kdl_project_status'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'kdl_project_status'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'Completed', u'Ongoing'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)


class KDLMetadataSchemaPlugin(
        plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'kdl_metadata_schema')

    def get_helpers(self):
        return {'kdl_project_status': kdl_project_status}

    def _modify_package_schema(self, schema):
        schema.update({
            'kdl_project_url': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_validator('url_validator'),
                toolkit.get_converter('convert_to_extras')
            ],
            'kdl_project_pi': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ],
            'kdl_project_team': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ],
            'kdl_project_start_date': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ],
            'kdl_project_end_date': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ],
            'kdl_project_status': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('kdl_project_status')
            ],
            'kdl_project_funder': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ],
            'kdl_project_citation': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ],
        })
        return schema

    def show_package_schema(self):
        schema = super(KDLMetadataSchemaPlugin, self).show_package_schema()

        schema['tags']['__extras'].append(
            toolkit.get_converter('free_tags_only'))

        schema.update({
            'kdl_project_url': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('url_validator'),
                toolkit.get_validator('ignore_missing')
            ],
            'kdl_project_pi': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ],
            'kdl_project_team': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ],
            'kdl_project_start_date': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ],
            'kdl_project_end_date': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ],
            'kdl_project_status': [
                toolkit.get_converter(
                    'convert_from_tags')('kdl_project_status'),
                toolkit.get_validator('ignore_missing')
            ],
            'kdl_project_funder': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ],
            'kdl_project_citation': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ],
        })
        return schema

    def create_package_schema(self):
        schema = super(KDLMetadataSchemaPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(KDLMetadataSchemaPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
