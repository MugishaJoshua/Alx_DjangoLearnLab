from django.contrib.auth.models import Group, Permission

def run():
    permissions = {
        "Viewers": ["can_view"],
        "Editors": ["can_view", "can_create", "can_edit"],
        "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
    }

    for group_name, perms in permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for perm in perms:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)

    print("Groups and permissions created successfully!")
