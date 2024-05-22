> Written by Keon Marcus (https://github.com/KeonM), Toaha Siddique (https://github.com/toaha-unc), Kyle Chen (https://github.com/kyle0509), and Varun Divi (https://github.com/VarunDivi) for group reservation in the csxl lab<br>
> *Last Updated: 12/10/2023*

### Description of models and API

A few new models were added to the backend.
    - group_details.py
        This is simple a class that contains "participants" aka a `list[User]`
    - group_user.py
        This model is used in our sql database to store unique ids of users in a group, the group id
        of the group that a user is in, and the pid of the user that can be used to determine if a 
        user is in the database or in another group
    - group.py
        This only contains a group id 

Here are the API routes that were added.
    - create_group
        Creates a group using a list of pids
    - get_group
        Searchs for a group based on a users pid, returns a `list[User]` in group
    - get_user_groups
        Returns a `list[int]` which are the group id of all groups User pid is in
        (This may not be used in the future)
    - delete_group
        Deletes a group based on group id
    - get_all_groups
        Retrieves a list of all group ids

### Database desrciption

Two new entities
    - group_user_entity.py
        This is the table that saves the data required to make a valid group (id, gid, and pid) as well as relationships from group_entity.py and user_entity.py. This file also has a from and to model.
    - group_entity.py
        Only contains a gid parameter, and a relationship to group_user_entity.py. This file also has a from and to model, as well as a to_details_model to get the information of a User.

user_entity.py is modifed so that it has a relationship with the group table

### Technical / user trade-offs

- Technical trade off
    The original thought was to use `User` and create a group of `User` however this was not generating correct functionality. Instead, it was decided that the use of pids from users would be a more effective method for creating groups. 

- User experience trade off
    In the current group reservation implementation a group must come in together and check out at the same time. What if a user wants to leave but the rest of the group doesn't? How can this be fixed in the future?

### Development concerns 

- Getting started
    The files that will be needed to understand the group reservation feature are the following...
    + backend/entities/group_entity.py, group_user_entity.py, user_entity.py
        Here is generally where the sql table is created that is used to store groups.
    + backend/api/group.py
        This is where methods are called, such as `get_all_groups` that will be connected to the frontend.
    + backend/models/group_details.py, group_user.py, group.py, user.py
        These are the models that out entities are built off of.
    + backend/services/group.py
        This where methods are created that the api will implement.
    + frontend/src/app/coworking, navigation
    Where it is decided what specific types of users can see and do.

### How group reservations work

#### Student view
    
- Sally student wants to use the xl lab with a few friends but they don't all want to checkin. Sally will make a group reservation

    + Sally will click "Click here for Group Reservation" where she will then see the following:
    ![Slider](https://github.com/comp423-23f/csxl-c5/blob/fullstack3/docs/images/group-slider-page.PNG)

    + After selecting a number of students that she wants (lets say 2), she is led to a page that logs her pid and asks for all members pids. They must be unique and exists in the database
    ![Select users](https://github.com/comp423-23f/csxl-c5/blob/fullstack3/docs/images/group-pid-page.PNG)

    + After confirming the valid pids she will be led back to confirm page with a similar look to solo reservations. Here she can confirm or cancel the reservation.
    ![Confirm](https://github.com/comp423-23f/csxl-c5/blob/fullstack3/docs/images/group-confirm-page.PNG)

#### Admin/ambassador view

- Amy ambassador wants to check in Sally's group reservation. 

    + First Amy will go to the XL Ambassador tab amy will see the following
    ![Check in](https://github.com/comp423-23f/csxl-c5/blob/fullstack3/docs/images/group-ambass-check.PNG)

    + After clicking 'check in' Amy wil be checked in and the number of seats that the group takes up will be removed from available seating
    ![Check in](https://github.com/comp423-23f/csxl-c5/blob/fullstack3/docs/images/group-ambass-checked.PNG)