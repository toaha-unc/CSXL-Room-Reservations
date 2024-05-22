### Title & Team

Group Reservation by Team C5 (Keon Marcus, Varun Divi, Kyle Chen, Toaha Siddique)

### Overview

The purpose of the Group Reservation feature is to enable people to checkin simultaneously and ensure collaboration.

### Key Personas

Student, Ambassador

### User Stories

- As Sally Student, I want to reserve a number of seats in SN 156 by registering in the CSXL system and also be able to check in, so that my group can work together whenever they want.

  Subtasks:

        - Sally Student should be able to select a group reservation.
        - Specify the number of members in the group.
        - Provide valid PIDs for each group member.
        - Confirm the group reservation.
        - Cancel the group reservation.
        - Checkout from the checkedin group reservation.

- As Amy Ambassador I want to be able to see the registered and checked-in groups, so that I can keep track of the groups in the CSXL system.

  Subtasks:

        - Amy Ambassador should have access to a list of upcoming and active group reservations.
        - View reservation details, including group members and duration.
        - Ability to check in a group.
        - Ability to checkout a group reservation.

### Wireframe

Figma wireframe:
https://www.figma.com/file/0MOqmCLL9H2Dfs1kqgg5Th/CSXL-group-reg?type=design&node-id=0%3A1&mode=design&t=p5lfu3OqDtEvjOW1-1

In the wireframe we go through the 2 main stories which are the student making the request and the ambassador who will see the reservation request. We also thought about adding a 3rd story which would be from the perspective of a student who will need to accept a request to join a group reservation. This has not been added yet, but is currently in consideration.

For Sally Student, Sally will start on the home page and click on `coworking` to access the coworking page where she will see a single reservation and group reservation tab. After confirming a group reservation, she will use a slider to determine how many members will be apart of the group. After confirming the number of members a window will appear that will allow Sally to add all users PIDs that will be in his group. If the users PID is not in the csxl database an error will be presented. Once it is confirmed and all PIDs are valid the group will be assigned seats automatically. The reservation card will then pop up with reservation details. Sally can confirm of cancel the group reservation, and once checkedin can checkout of the group reservation.

For Amy Ambassador, Amy will start on the home page and click on `XL Ambassador`. Once in the XL Ambassador tab Amy will see the upcoming reservations and the active reservations. In the example given in the wireframe Sally's reservation is in the future so it is listed under upcoming reservation. Amy can see the details of who made the reservation, who the members of the group are and the duration of the reservation. She can also check in a group and checkout a group, or return to the XL Ambassador page. If all reservations are removed there will be no upcoming reservations. If checked in the group will appear under active reservations, and details can still be seen.

### Technical Implementation Opportunities and Planning

Specific areas of the existing code base:

- backend/api/coworking/reservation.py ~ Extending upon the reservations functions
  - We use the draft reservation api endpoint to create a group draft.
  - Ambassadors are able to use the existing change_reservation status endpoint to complete and reservation.
- frontend/src/coworking ~ reservation.service.ts ~ We use the existing reservation service files to make refrences to the reservation api.
- frontend/src/app/coworking/ambassador-home/ambassador-home.component.html ~ We used the existing ambassador page to display checked in groups in a very similar format as an individual check in.
- backend/api/profile.py ~ We utilizes the profile api to retrieve a user profile by their pid in the frontend. This api allowed us to pass in mutliple profiles of the group members which is a necessarry parameter to create a reservation.

Planned page components and widgets:

- frontend/src/coworking/coworking-home ~ We added a new button to the existing reservation drop down card. The button collapses with the card.
- frontend/src/app/coworking/widgets/coworking-reservation-card/coworking-reservation-card.html ~ Expanded on existing code to allow group reservation previews to be displayed is the Who, What, Where
- frontend/src/app/coworking/slider ~ The button from coworking-home routes to a slider component where the user can specifiy the size of the group they want to create.
- frontend/src/app/coworking/group ~ We added a new group component that the user is routed to after selecting 'confirm' on the slider component page.
  - Here, the user is able to specificy the information needed to create a group.

Additional models or changes to existing models:

- backend/entities/group_user_entity.py ~ We created a new group_user entity model to map a 1-to-many relationship between a group and a user. We used foreign keys to make references to this intermediary entity.
- backend/models/group_user.py ~ The group_user model holds the Unique foreign keys of a User and Group.
- backend/entities/group_entity.py ~ The new group entity is how we store our new group model in our database.
- backend/models/group.py ~ The group model holds a unique GID and makes a refrence to group details to get the list of Users. This group model has the information that we pass into our reservation
- backend/models/group_details.py ~ Delegates the storage of Users so that the group model doesnt make a circular import.

Additional Services

- backend/services/group.py ~ A new group service in the backend that defines behavior when interacting with the group API http methods.
- frontend/src/app/coworking/group.service.ts ~ The group service in the frontend communicates with the backend and database via a connection to the backend group service.

Needed API/Routes:

- backend/api/group.py
  - @api.post("", response_model=Group, tags=["Groups"]) ~ A post API that creates the group. The API should create a unique GID upon creation.
  - @api.get("/{gid}", response_model=list[User], tags=["Groups"]) ~ A GET API that should retrieve the list of users in a group. We should pass in the group's unique ID.
  - @api.get("/user/{pid}", response_model=int, tags=["Groups"]) ~ A GET API that should retrieve a User's group id assuming that they are in a group.
  - @api.delete("/{gid}", response_model=None, tags=["Groups"]) ~ A DELETE API that should delete a group id from the database.

Security Concerns:

- When deciding who is able to cancel reservations, ensure that only the users in the reservation and the ambassador have the capability to cancel reservations. This restricted authorization approach will provide the users in the reservation and the ambassador with the necessary control to manage group reservations effectively while preventing unauthorized personnel from canceling reservations. This helps maintain the integrity of the reservation system and ensures that only authorized participants are included in group reservations.

Testing Plan:

Group Testing:

- We first want to make sure that we are succesfully able to create a group including edge case circumstances

Draft Testing:

- Once we know that a group is succesfuly created, we can move on to testing group reservation in reservation draft.
- Complete base then edge case testing.
