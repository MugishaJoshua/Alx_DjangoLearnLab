from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def run():
    """
    Create groups and assign permissions safely.
    """
    # Groups and permission types you want to assign
    group_permissions_map = {
        "Admins": ["add", "change", "delete", "view"],
        "Editors": ["add", "change"],
        "Viewers": ["view"],
    }

    # Apps to include
    apps_to_include = ["accounts", "bookshelf"]

    for group_name, perms in group_permissions_map.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        all_permissions = []

        for app_label in apps_to_include:
            for model in apps.get_app_config(app_label).get_models():
                ct = ContentType.objects.get_for_model(model)
                for perm_type in perms:
                    codename = f"{perm_type}_{model._meta.model_name}"
                    # Use filter() instead of get()
                    permission_qs = Permission.objects.filter(codename=codename, content_type=ct)
                    for permission in permission_qs:
                        all_permissions.append(permission)

        # Assign all collected permissions to the group
        group.permissions.set(all_permissions)
        group.save()
        print(f"Group '{group_name}' updated with {len(all_permissions)} permissions.")

    print("All groups and permissions have been created successfully!")
