# 4. Create a decorator named authentication_required and apply it to view_profile() and update_profile().

from functools import wraps


def authentication_required(function):

    @wraps(function)
    def wrapper(user):

        if user["logged_in"]:
            return function(user)

        print("Access Denied")

    return wrapper


@authentication_required
def view_profile(user):
    print(f"Viewing profile of {user['name']}")


@authentication_required
def update_profile(user):
    print(f"Updating profile of {user['name']}")


def main():
    username= input("enter your name : ")
    user = {
        "name": username,
        "logged_in": True
    }

    view_profile(user)
    update_profile(user)


if __name__ == "__main__":
    main()