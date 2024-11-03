from src.db.controllers import (
    ctrl_user,
    ctrl_role,
    ctrl_permission,
    ctrl_role_permission,
    ctrl_user_role,
)
from src.common.encryption import Password


def seed_database():

    # Create Permissions
    permissions_data = [
        {"name": "read", "description": "Read data"},
        {"name": "edit", "description": "Edit data"},
        {"name": "delete", "description": "Delete data"},
        {"name": "approve", "description": "Approve data"},
    ]

    with ctrl_permission:
        for perm in permissions_data:
            existing_perm = ctrl_permission.get(by="name", value=perm["name"])
            if not existing_perm:
                ctrl_permission.create(data=perm)

    # Create Roles
    roles_data = [
        {
            "name": "ADMIN",
            "description": "Full access with read, edit, delete, and approve permissions.",
        },
        {"name": "TRAINEE", "description": "No access to data viewing."},
        {
            "name": "ASSESSOR",
            "description": "Limited read access to own clients' data.",
        },
    ]

    with ctrl_role:
        for role in roles_data:
            existing_role = ctrl_role.get(by="name", value=role["name"])
            if not existing_role:
                ctrl_role.create(data=role)

    # Assign Permissions to Roles
    role_permissions = {
        "ADMIN": ["read", "edit", "delete", "approve"],
        "ASSESSOR": ["read"],
        # TRAINEE has no permissions
    }

    with ctrl_role:
        for role_name, perms in role_permissions.items():
            role = ctrl_role.get(by="name", value=role_name)
            if role:
                for perm_name in perms:
                    perm = ctrl_permission.get(by="name", value=perm_name)
                    if perm:
                        existing_rp = ctrl_role_permission.get(
                            by=["role_id", "permission_id"],
                            value=[role["id"], perm["id"]],
                        )
                        if not existing_rp:
                            ctrl_role_permission.create(
                                dict(role_id=role["id"], permission_id=perm["id"]),
                            )

    # Create an Admin User
    admin_email = "admin@quark.com.br"
    admin_password = "quark54312"

    existing_admin = ctrl_user.get(by="email", value=admin_email)
    if not existing_admin:
        password = Password(admin_password)
        new_admin = ctrl_user.create(
            dict(
                email=admin_email, name="ADM", password=password.hash(), verified=True
            ),
            returns_object=True,
        )

        # Assign ADMIN role to the new admin user
        admin_role = ctrl_role.get(by="name", value="ADMIN")
        if admin_role:
            ctrl_user_role.create(
                dict(user_id=new_admin["id"], role_id=admin_role["id"])
            )

    # Create Assessors
    assessors = [
        {"email": "ben@quark.com.br", "name": "BEN", "password": "password123"},
        {"email": "giovani@quark.com.br", "name": "GIOVANI", "password": "password123"},
        {"email": "isabela@quark.com.br", "name": "ISABELA", "password": "password123"},
        {"email": "carlos@quark.com.br", "name": "CARLOS", "password": "password123"},
    ]

    with ctrl_user:
        for assessor in assessors:
            existing_assessor = ctrl_user.get(by="email", value=assessor["email"])
            if not existing_assessor:
                password = Password(assessor["password"])
                new_assessor = ctrl_user.create(
                    dict(
                        email=assessor["email"],
                        name=assessor["name"],
                        password=password.hash(),
                        verified=True,
                    ),
                    returns_object=True,
                )
                assessor_role = ctrl_role.get(by="name", value="ASSESSOR")
                if assessor_role:
                    ctrl_user_role.create(
                        dict(user_id=new_assessor["id"], role_id=assessor_role["id"])
                    )


if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully.")
