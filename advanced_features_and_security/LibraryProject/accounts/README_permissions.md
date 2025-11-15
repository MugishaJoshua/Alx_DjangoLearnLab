# Django Permissions & Groups Setup

### Custom Permissions
The Book model has custom permissions:
- can_view: Allows viewing book list and details.
- can_create: Allows creating new books.
- can_edit: Allows editing existing books.
- can_delete: Allows deleting books.

### Groups
Groups are created to organize user access:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

### Applying Permissions
Views are protected using Django's @permission_required decorator.

Example:
@permission_required('bookshelf.can_edit', raise_exception=True)

### Testing
Create test users, assign them to groups, and attempt to access views.
