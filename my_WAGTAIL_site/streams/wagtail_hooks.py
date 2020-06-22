import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import \
    InlineStyleElementHandler
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_code_styling(features):

    feature_name = "code"
    type_ = "CODE"
    tag = "code"

    control = {"type": type_, "label": '</>', "description": 'Стиль коду'}

    features.register_editor_plugin(
        "draftail", feature_name,
        draftail_features.InlineStyleFeature(control))

    db_conversion = {
        "from_database_format": {
            tag: InlineStyleElementHandler(type_)
        },
        "to_database_format": {
            'style_map': {
                type_: {
                    "element": tag
                }
            }
        }
    }

    features.register_converter_rule("contentstate", feature_name,
                                     db_conversion)

    # This will register the feature accross all richtext editors  by default
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_center_text_feature(features):
    """ <div style='text-align: center;'> </div> """

    feature_name = "center"
    type_ = "CENTER"
    tag = "div"

    control = {
        "type": type_,
        "label": "[ Цитата ]",
        "description": 'Додати цитату',
        "style": {
            "display": "block",
            "text-align": "center",
        },
    }

    features.register_editor_plugin(
        "draftail", feature_name,
        draftail_features.InlineStyleFeature(control))

    db_conversion = {
        "from_database_format": {
            tag: InlineStyleElementHandler(type_)
        },
        "to_database_format": {
            'style_map': {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "d-block text-center",
                        "style": "background-color: grey;"
                    }
                }
            }
        }
    }

    features.register_converter_rule("contentstate", feature_name,
                                     db_conversion)

    # This will register the feature accross all richtext editors  by default
    features.default_features.append(feature_name)